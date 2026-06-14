# shipmentDemo

A demo shipment-tracking REST API built with **FastAPI** and **Python 3.12**.  
This repository is intended to showcase clean Python architecture, REST API design, input validation, and testing practices.

---

## Features

| Capability | Detail |
|---|---|
| Create shipment | Auto-generates a unique tracking number (`SHP-XXXXXXXXXX`) |
| List shipments | Returns all shipments ordered by creation date (newest first) |
| Get shipment | Retrieve full details including the tracking history |
| Track by number | Public tracking endpoint — no internal ID required |
| Update shipment | Partial updates (PATCH) for sender/recipient details and weight |
| Tracking events | Append events with status transitions enforced by a state machine |
| Delete shipment | Remove a shipment record |
| Health check | `GET /health` — useful for load-balancer probes |

### Shipment Status State Machine

```
PENDING → PICKED_UP → IN_TRANSIT → OUT_FOR_DELIVERY → DELIVERED
                                 ↘ RETURNED          ↘ FAILED_DELIVERY → OUT_FOR_DELIVERY
                                                                        ↘ RETURNED
```

---

## Project Structure

```
shipmentDemo/
├── app/
│   ├── main.py               # FastAPI application factory
│   ├── models/
│   │   └── shipment.py       # Domain model (plain Python classes + Enum)
│   ├── schemas/
│   │   └── shipment.py       # Pydantic request/response schemas
│   ├── routers/
│   │   └── shipments.py      # API route handlers
│   └── services/
│       └── shipment_service.py  # Business logic & in-memory store
├── tests/
│   └── test_shipments.py     # Pytest test suite (25 tests)
├── requirements.txt
└── requirements-dev.txt
```

---

## Quick Start

### Prerequisites

* Python 3.12+

### Installation

```bash
# Clone the repository
git clone https://github.com/gajdaj2/shipmentDemo.git
cd shipmentDemo

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install runtime dependencies
pip install -r requirements.txt
```

### Run the API

```bash
uvicorn app.main:app --reload
```

The API is now available at **http://127.0.0.1:8000**.  
Interactive docs (Swagger UI): **http://127.0.0.1:8000/docs**  
Alternative docs (ReDoc): **http://127.0.0.1:8000/redoc**

---

## API Reference

### Create a Shipment

```http
POST /shipments/
Content-Type: application/json

{
  "sender_name": "Alice Smith",
  "sender_address": "123 Main St, Springfield, IL 62701",
  "recipient_name": "Bob Jones",
  "recipient_address": "456 Oak Ave, Chicago, IL 60601",
  "weight_kg": 2.5,
  "description": "Electronics"
}
```

### List All Shipments

```http
GET /shipments/
```

### Get a Shipment

```http
GET /shipments/{shipment_id}
```

### Track by Tracking Number

```http
GET /shipments/track/{tracking_number}
```

### Update a Shipment

```http
PATCH /shipments/{shipment_id}
Content-Type: application/json

{
  "recipient_address": "789 Elm St, Chicago, IL 60602"
}
```

### Add a Tracking Event

```http
POST /shipments/{shipment_id}/tracking
Content-Type: application/json

{
  "status": "picked_up",
  "location": "Warehouse A",
  "description": "Parcel collected from sender"
}
```

### Delete a Shipment

```http
DELETE /shipments/{shipment_id}
```

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Expected output: **25 passed**.

---

## Design Decisions

* **In-memory store** — keeps the demo dependency-free. Swap `ShipmentService._store` for a database repository without changing any router or schema code.
* **Pydantic v2 schemas** — strict input validation with clear error messages.
* **State machine** — `VALID_TRANSITIONS` dict in `shipment_service.py` makes allowed status changes explicit and easy to extend.
* **Separation of concerns** — models, schemas, services, and routers are intentionally kept in separate layers.
