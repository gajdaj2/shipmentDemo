from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models.shipment import ShipmentStatus


class TrackingEventSchema(BaseModel):
    status: ShipmentStatus
    location: str
    description: str
    timestamp: datetime

    model_config = {"from_attributes": True}


class ShipmentCreate(BaseModel):
    sender_name: str = Field(..., min_length=1, max_length=100)
    sender_address: str = Field(..., min_length=1, max_length=250)
    recipient_name: str = Field(..., min_length=1, max_length=100)
    recipient_address: str = Field(..., min_length=1, max_length=250)
    weight_kg: float = Field(..., gt=0, le=1000)
    description: str = Field(default="", max_length=500)

    @field_validator("weight_kg")
    @classmethod
    def round_weight(cls, v: float) -> float:
        return round(v, 3)


class ShipmentUpdate(BaseModel):
    sender_name: str | None = Field(default=None, min_length=1, max_length=100)
    sender_address: str | None = Field(default=None, min_length=1, max_length=250)
    recipient_name: str | None = Field(default=None, min_length=1, max_length=100)
    recipient_address: str | None = Field(default=None, min_length=1, max_length=250)
    weight_kg: float | None = Field(default=None, gt=0, le=1000)
    description: str | None = Field(default=None, max_length=500)

    @field_validator("weight_kg")
    @classmethod
    def round_weight(cls, v: float | None) -> float | None:
        return round(v, 3) if v is not None else v


class TrackingUpdate(BaseModel):
    status: ShipmentStatus
    location: str = Field(..., min_length=1, max_length=250)
    description: str = Field(..., min_length=1, max_length=500)


class ShipmentResponse(BaseModel):
    id: str
    tracking_number: str
    sender_name: str
    sender_address: str
    recipient_name: str
    recipient_address: str
    weight_kg: float
    description: str
    status: ShipmentStatus
    created_at: datetime
    updated_at: datetime
    tracking_history: list[TrackingEventSchema]

    model_config = {"from_attributes": True}


class ShipmentSummary(BaseModel):
    id: str
    tracking_number: str
    sender_name: str
    recipient_name: str
    status: ShipmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
