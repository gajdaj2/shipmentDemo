from fastapi import FastAPI

from app.routers import shipments
from app.services.shipment_service import ShipmentService

app = FastAPI(
    title="Shipment Tracking API",
    description=(
        "A RESTful API for managing and tracking shipments. "
        "Supports full CRUD operations and a step-by-step tracking event workflow."
    ),
    version="1.0.0",
)

shipment_service = ShipmentService()

app.include_router(shipments.router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
