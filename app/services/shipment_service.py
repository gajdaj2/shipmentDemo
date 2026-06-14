import uuid
from datetime import UTC, datetime

from app.models.shipment import Shipment, ShipmentStatus, TrackingEvent
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate, TrackingUpdate


def _generate_tracking_number() -> str:
    return f"SHP-{uuid.uuid4().hex[:10].upper()}"


class ShipmentNotFoundError(Exception):
    pass


class InvalidStatusTransitionError(Exception):
    pass


VALID_TRANSITIONS: dict[ShipmentStatus, set[ShipmentStatus]] = {
    ShipmentStatus.PENDING: {ShipmentStatus.PICKED_UP},
    ShipmentStatus.PICKED_UP: {ShipmentStatus.IN_TRANSIT},
    ShipmentStatus.IN_TRANSIT: {ShipmentStatus.OUT_FOR_DELIVERY, ShipmentStatus.RETURNED},
    ShipmentStatus.OUT_FOR_DELIVERY: {ShipmentStatus.DELIVERED, ShipmentStatus.FAILED_DELIVERY},
    ShipmentStatus.FAILED_DELIVERY: {ShipmentStatus.OUT_FOR_DELIVERY, ShipmentStatus.RETURNED},
    ShipmentStatus.DELIVERED: set(),
    ShipmentStatus.RETURNED: set(),
}


class ShipmentService:
    def __init__(self) -> None:
        self._store: dict[str, Shipment] = {}

    def create(self, data: ShipmentCreate) -> Shipment:
        shipment_id = str(uuid.uuid4())
        shipment = Shipment(
            id=shipment_id,
            tracking_number=_generate_tracking_number(),
            sender_name=data.sender_name,
            sender_address=data.sender_address,
            recipient_name=data.recipient_name,
            recipient_address=data.recipient_address,
            weight_kg=data.weight_kg,
            description=data.description,
        )
        self._store[shipment_id] = shipment
        return shipment

    def get(self, shipment_id: str) -> Shipment:
        shipment = self._store.get(shipment_id)
        if shipment is None:
            raise ShipmentNotFoundError(f"Shipment '{shipment_id}' not found")
        return shipment

    def get_by_tracking_number(self, tracking_number: str) -> Shipment:
        for shipment in self._store.values():
            if shipment.tracking_number == tracking_number:
                return shipment
        raise ShipmentNotFoundError(f"Shipment with tracking number '{tracking_number}' not found")

    def list_all(self) -> list[Shipment]:
        return sorted(self._store.values(), key=lambda s: s.created_at, reverse=True)

    def update(self, shipment_id: str, data: ShipmentUpdate) -> Shipment:
        shipment = self.get(shipment_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(shipment, field, value)
        shipment.updated_at = datetime.now(UTC)
        return shipment

    def add_tracking_event(self, shipment_id: str, event_data: TrackingUpdate) -> Shipment:
        shipment = self.get(shipment_id)

        allowed = VALID_TRANSITIONS.get(shipment.status, set())
        if event_data.status not in allowed:
            raise InvalidStatusTransitionError(
                f"Cannot transition from '{shipment.status}' to '{event_data.status}'. "
                f"Allowed transitions: {[s.value for s in allowed]}"
            )

        event = TrackingEvent(
            status=event_data.status,
            location=event_data.location,
            description=event_data.description,
        )
        shipment.tracking_history.append(event)
        shipment.status = event_data.status
        shipment.updated_at = datetime.now(UTC)
        return shipment

    def delete(self, shipment_id: str) -> None:
        if shipment_id not in self._store:
            raise ShipmentNotFoundError(f"Shipment '{shipment_id}' not found")
        del self._store[shipment_id]
