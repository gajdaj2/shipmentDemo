from contextlib import asynccontextmanager
from enum import Enum
import logging
import sys
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from scalar_fastapi import get_scalar_api_reference
from check_shipment_field import check_shipment_field
from check_shipment_requirements import check_shipment_requirements
import db
from models.shipment_model import ShipmentModel
from loguru import logger
from db import CRUDDatabase

db: CRUDDatabase | None = None


def validate_shipment_exists(id, shipment):
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found",
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    db = CRUDDatabase()
    app.state.db = db
    yield


app = FastAPI(lifespan=lifespan)


logger.remove()  # usuń domyślny handler

logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> - <white>{message}</white>",
    colorize=True,
)

logger.add(
    "logs/app.log",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} - {message}",
    rotation="10 MB",  # nowy plik po 10 MB
    retention="7 days",  # usuń logi starsze niż 7 dni
    compression="zip",  # archiwizuj stare pliki
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} ({duration:.3f}s)"
    )
    return response



@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    assert db is not None
    check_shipment_field(field, id)
    return {field: getattr(db.get_shipment(id), field)}


@app.patch("/shipment/{field}", status_code=status.HTTP_200_OK)
def patch_shipment_field(field: str, id: int, value: Any) -> dict[str, Any]:
    assert db is not None
    shipment = db.get_shipment(id)
    setattr(shipment, field, value)
    db.update_shipment(id, shipment)
    return {field: getattr(shipment, field)}


@app.patch(
    "/shipment/{id}", status_code=status.HTTP_200_OK, response_model=ShipmentModel
)
def shipment_update_status(id: int, new_status: str) -> ShipmentModel:
    assert db is not None
    shipment = db.get_shipment(id)
    validate_shipment_exists(id, shipment)
    shipment.status = new_status
    db.update_shipment(id, shipment)
    return shipment




def delete_shipment(id: int) -> dict[str, Any]:
    assert db is not None
    shipment = db.get_shipment(id)
    validate_shipment_exists(id, shipment)
    db.delete_shipment(id)
    return {"message": f"Shipment with id {id} deleted", "shipment": shipment}

@app.get("/shipments", status_code=status.HTTP_200_OK, description="Get all shipments")
def get_all_shipments() -> list[ShipmentModel]:
    assert db is not None
    return db.get_all_shipments()
    

@app.get("/shipment", status_code=status.HTTP_200_OK)
def get_shipment(id: int | None = None) -> ShipmentModel:
    assert db is not None
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required query parameter: id",
        )
    return db.get_shipment(id)


@app.put("/shipment/{id}", status_code=status.HTTP_200_OK)
def shipment_update(id: int, shipment_data: ShipmentModel) -> ShipmentModel:
    assert db is not None
    validate_shipment_exists(id, db.get_shipment(id))
    updated_shipment = db.update_shipment(id, shipment_data)
    return updated_shipment


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def submit_shipment(shipment_data: ShipmentModel) -> ShipmentModel:
    logger.info(f"Received shipment data: {shipment_data}")
    assert db is not None
    created_shipment = db.create_shipment(shipment_data)
    logger.info(f"Created shipment: {created_shipment}")
    return created_shipment


@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        title="Shipment API",
    )
