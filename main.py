from enum import Enum
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from check_shipment_field import check_shipment_field
from check_shipment_requirements import check_shipment_requirements
import db
from models.shipment_model import ShipmentModel

app = FastAPI()





@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    check_shipment_field(field, id)
    return {field: getattr(db.shipment_records[id], field)}


@app.patch("/shipment/{field}", status_code=status.HTTP_200_OK)
def patch_shipment_field(field: str, id: int, value: Any) -> dict[str, Any]:
    db.shipment_records[id] = db.shipment_records[id].model_copy(update={field: value})
    return {field: getattr(db.shipment_records[id], field)}


@app.patch("/shipment/{id}", status_code=status.HTTP_200_OK)
def shipment_update_status(id: int, new_status: str) -> ShipmentModel:
    if id not in db.shipment_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found",
        )
    db.shipment_records[id].status = new_status
    return db.shipment_records[id]


def delete_shipment(id: int) -> dict[str, Any]:
    if id not in db.shipment_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found",
        )
    deleted_shipment = db.shipment_records.pop(id)
    return {"id": id, "deleted_shipment": deleted_shipment}


@app.get("/shipments", status_code=status.HTTP_200_OK, description="Get all shipments")
def get_all_shipments() -> list[ShipmentModel]:
    return list(map(lambda x: db.shipment_records[x], db.shipment_records))


@app.get("/shipment", status_code=status.HTTP_200_OK)
def get_shipment(id: int | None = None) -> ShipmentModel:
    if id is None:
        id = max(db.shipment_records.keys())
        return db.shipment_records[id]
    if id not in db.shipment_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found",
        )
    return db.shipment_records[id]


@app.put("/shipment/{id}", status_code=status.HTTP_200_OK)
def shipment_update(id: int, shipment_data: ShipmentModel) -> ShipmentModel:
    if id not in db.shipment_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found",
        )
    db.shipment_records[id] = shipment_data
    return db.shipment_records[id]


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def submit_shipment(shipment_data: ShipmentModel) -> ShipmentModel:
    id = max(db.shipment_records.keys()) + 1
    shipments = {
        "weight": shipment_data.weight,
        "content": shipment_data.content,
    }
    db.shipment_records[id] = ShipmentModel(**shipments)
    return db.shipment_records[id]


@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        title="Shipment API",
    )
