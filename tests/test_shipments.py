import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.shipment_service import ShipmentService


@pytest.fixture(autouse=True)
def reset_service():
    """Reset the in-memory store before each test to ensure isolation."""
    import app.main as main_module
    main_module.shipment_service = ShipmentService()
    yield


@pytest.fixture
def client():
    return TestClient(app)


VALID_PAYLOAD = {
    "sender_name": "Alice Smith",
    "sender_address": "123 Main St, Springfield, IL 62701",
    "recipient_name": "Bob Jones",
    "recipient_address": "456 Oak Ave, Chicago, IL 60601",
    "weight_kg": 2.5,
    "description": "Electronics",
}


class TestHealthCheck:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestCreateShipment:
    def test_create_returns_201(self, client):
        resp = client.post("/shipments/", json=VALID_PAYLOAD)
        assert resp.status_code == 201

    def test_create_response_fields(self, client):
        resp = client.post("/shipments/", json=VALID_PAYLOAD)
        body = resp.json()
        assert body["sender_name"] == VALID_PAYLOAD["sender_name"]
        assert body["recipient_name"] == VALID_PAYLOAD["recipient_name"]
        assert body["status"] == "pending"
        assert body["weight_kg"] == 2.5
        assert len(body["tracking_history"]) == 1
        assert body["tracking_history"][0]["status"] == "pending"

    def test_create_generates_tracking_number(self, client):
        resp = client.post("/shipments/", json=VALID_PAYLOAD)
        body = resp.json()
        assert body["tracking_number"].startswith("SHP-")
        assert len(body["tracking_number"]) == 14  # "SHP-" + 10 hex chars

    def test_create_missing_required_field(self, client):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "sender_name"}
        resp = client.post("/shipments/", json=payload)
        assert resp.status_code == 422

    def test_create_invalid_weight_zero(self, client):
        resp = client.post("/shipments/", json={**VALID_PAYLOAD, "weight_kg": 0})
        assert resp.status_code == 422

    def test_create_invalid_weight_negative(self, client):
        resp = client.post("/shipments/", json={**VALID_PAYLOAD, "weight_kg": -1})
        assert resp.status_code == 422

    def test_create_weight_rounded(self, client):
        resp = client.post("/shipments/", json={**VALID_PAYLOAD, "weight_kg": 1.23456})
        assert resp.json()["weight_kg"] == 1.235


class TestGetShipment:
    def test_get_existing(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        resp = client.get(f"/shipments/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_not_found(self, client):
        resp = client.get("/shipments/nonexistent-id")
        assert resp.status_code == 404


class TestListShipments:
    def test_list_empty(self, client):
        resp = client.get("/shipments/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_summaries(self, client):
        client.post("/shipments/", json=VALID_PAYLOAD)
        client.post("/shipments/", json={**VALID_PAYLOAD, "recipient_name": "Carol White"})
        resp = client.get("/shipments/")
        assert resp.status_code == 200
        body = resp.json()
        assert len(body) == 2
        assert "tracking_history" not in body[0]

    def test_list_ordered_newest_first(self, client):
        first = client.post("/shipments/", json=VALID_PAYLOAD).json()
        second = client.post("/shipments/", json={**VALID_PAYLOAD, "recipient_name": "Carol"}).json()
        body = client.get("/shipments/").json()
        assert body[0]["id"] == second["id"]
        assert body[1]["id"] == first["id"]


class TestUpdateShipment:
    def test_patch_sender_name(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        resp = client.patch(f"/shipments/{created['id']}", json={"sender_name": "New Name"})
        assert resp.status_code == 200
        assert resp.json()["sender_name"] == "New Name"

    def test_patch_not_found(self, client):
        resp = client.patch("/shipments/nonexistent-id", json={"sender_name": "X"})
        assert resp.status_code == 404

    def test_patch_does_not_change_unspecified_fields(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        client.patch(f"/shipments/{created['id']}", json={"sender_name": "Updated"})
        updated = client.get(f"/shipments/{created['id']}").json()
        assert updated["recipient_name"] == VALID_PAYLOAD["recipient_name"]


class TestTrackingEvents:
    def test_add_valid_tracking_event(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        resp = client.post(
            f"/shipments/{created['id']}/tracking",
            json={"status": "picked_up", "location": "Warehouse A", "description": "Parcel collected"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "picked_up"
        assert len(body["tracking_history"]) == 2

    def test_invalid_transition_raises_422(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        resp = client.post(
            f"/shipments/{created['id']}/tracking",
            json={"status": "delivered", "location": "Home", "description": "Left at door"},
        )
        assert resp.status_code == 422

    def test_full_happy_path(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        sid = created["id"]

        steps = [
            ("picked_up", "Depot", "Collected from sender"),
            ("in_transit", "Sorting Hub", "In sorting facility"),
            ("out_for_delivery", "Local Branch", "Out with courier"),
            ("delivered", "Recipient Address", "Left at front door"),
        ]
        for status_val, location, desc in steps:
            resp = client.post(
                f"/shipments/{sid}/tracking",
                json={"status": status_val, "location": location, "description": desc},
            )
            assert resp.status_code == 200

        final = client.get(f"/shipments/{sid}").json()
        assert final["status"] == "delivered"
        assert len(final["tracking_history"]) == 5

    def test_tracking_event_not_found(self, client):
        resp = client.post(
            "/shipments/bad-id/tracking",
            json={"status": "picked_up", "location": "X", "description": "Y"},
        )
        assert resp.status_code == 404


class TestTrackByTrackingNumber:
    def test_track_valid(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        tracking_number = created["tracking_number"]
        resp = client.get(f"/shipments/track/{tracking_number}")
        assert resp.status_code == 200
        assert resp.json()["tracking_number"] == tracking_number

    def test_track_not_found(self, client):
        resp = client.get("/shipments/track/SHP-NOTEXIST00")
        assert resp.status_code == 404


class TestDeleteShipment:
    def test_delete_existing(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        resp = client.delete(f"/shipments/{created['id']}")
        assert resp.status_code == 204

    def test_delete_then_get_returns_404(self, client):
        created = client.post("/shipments/", json=VALID_PAYLOAD).json()
        client.delete(f"/shipments/{created['id']}")
        resp = client.get(f"/shipments/{created['id']}")
        assert resp.status_code == 404

    def test_delete_not_found(self, client):
        resp = client.delete("/shipments/nonexistent-id")
        assert resp.status_code == 404
