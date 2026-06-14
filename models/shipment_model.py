from enum import Enum

from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    IN_TRANSIT = "In transit"
    DELIVERED = "Delivered"
    PENDING = "Pending"
    CANCELLED = "Cancelled"


class ShipmentModel(BaseModel):
    """
    A Pydantic model representing a shipment.
    """

    weight: float | int = Field(
        gt=0, le=1000, description="Weight of the shipment in kilograms"
    )
    content: str = Field(
        min_length=1, max_length=100, description="Description of the shipment content"
    )
    status: str | None = Field(
        min_length=1,
        max_length=50,
        default=ShipmentStatus.IN_TRANSIT.value,
        description="Current status of the shipment",
        
    )
