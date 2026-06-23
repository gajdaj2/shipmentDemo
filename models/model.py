from sqlmodel import SQLModel, Field
from sqlalchemy import create_engine


class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"
    id: int | None = Field(default=None, primary_key=True)
    status: str
    weight: float = Field(default=0.0, le=25)
    content: str
