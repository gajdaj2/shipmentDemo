from datetime import UTC, datetime
from enum import Enum


class ShipmentStatus(str, Enum):
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED_DELIVERY = "failed_delivery"
    RETURNED = "returned"


class TrackingEvent:
    def __init__(self, status: ShipmentStatus, location: str, description: str, timestamp: datetime | None = None):
        self.status = status
        self.location = location
        self.description = description
        self.timestamp = timestamp or datetime.now(UTC)


class Shipment:
    def __init__(
        self,
        id: str,
        tracking_number: str,
        sender_name: str,
        sender_address: str,
        recipient_name: str,
        recipient_address: str,
        weight_kg: float,
        description: str = "",
    ):
        self.id = id
        self.tracking_number = tracking_number
        self.sender_name = sender_name
        self.sender_address = sender_address
        self.recipient_name = recipient_name
        self.recipient_address = recipient_address
        self.weight_kg = weight_kg
        self.description = description
        self.status = ShipmentStatus.PENDING
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        self.tracking_history: list[TrackingEvent] = [
            TrackingEvent(
                status=ShipmentStatus.PENDING,
                location=sender_address,
                description="Shipment created and awaiting pickup",
            )
        ]
