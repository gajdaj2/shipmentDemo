from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentResponse,
    ShipmentSummary,
    ShipmentUpdate,
    TrackingUpdate,
)
from app.services.shipment_service import (
    InvalidStatusTransitionError,
    ShipmentNotFoundError,
    ShipmentService,
)

router = APIRouter(prefix="/shipments", tags=["shipments"])


def get_service() -> ShipmentService:
    from app.main import shipment_service
    return shipment_service


def _to_response(shipment) -> ShipmentResponse:
    from app.schemas.shipment import TrackingEventSchema

    history = [
        TrackingEventSchema(
            status=e.status,
            location=e.location,
            description=e.description,
            timestamp=e.timestamp,
        )
        for e in shipment.tracking_history
    ]
    return ShipmentResponse(
        id=shipment.id,
        tracking_number=shipment.tracking_number,
        sender_name=shipment.sender_name,
        sender_address=shipment.sender_address,
        recipient_name=shipment.recipient_name,
        recipient_address=shipment.recipient_address,
        weight_kg=shipment.weight_kg,
        description=shipment.description,
        status=shipment.status,
        created_at=shipment.created_at,
        updated_at=shipment.updated_at,
        tracking_history=history,
    )


@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(
    data: ShipmentCreate,
    service: ShipmentService = Depends(get_service),
) -> ShipmentResponse:
    shipment = service.create(data)
    return _to_response(shipment)


@router.get("/", response_model=list[ShipmentSummary])
def list_shipments(service: ShipmentService = Depends(get_service)) -> list[ShipmentSummary]:
    shipments = service.list_all()
    return [
        ShipmentSummary(
            id=s.id,
            tracking_number=s.tracking_number,
            sender_name=s.sender_name,
            recipient_name=s.recipient_name,
            status=s.status,
            created_at=s.created_at,
            updated_at=s.updated_at,
        )
        for s in shipments
    ]


@router.get("/track/{tracking_number}", response_model=ShipmentResponse)
def track_shipment(
    tracking_number: str,
    service: ShipmentService = Depends(get_service),
) -> ShipmentResponse:
    try:
        shipment = service.get_by_tracking_number(tracking_number)
    except ShipmentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return _to_response(shipment)


@router.get("/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(
    shipment_id: str,
    service: ShipmentService = Depends(get_service),
) -> ShipmentResponse:
    try:
        shipment = service.get(shipment_id)
    except ShipmentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return _to_response(shipment)


@router.patch("/{shipment_id}", response_model=ShipmentResponse)
def update_shipment(
    shipment_id: str,
    data: ShipmentUpdate,
    service: ShipmentService = Depends(get_service),
) -> ShipmentResponse:
    try:
        shipment = service.update(shipment_id, data)
    except ShipmentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return _to_response(shipment)


@router.post("/{shipment_id}/tracking", response_model=ShipmentResponse)
def add_tracking_event(
    shipment_id: str,
    event: TrackingUpdate,
    service: ShipmentService = Depends(get_service),
) -> ShipmentResponse:
    try:
        shipment = service.add_tracking_event(shipment_id, event)
    except ShipmentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidStatusTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc
    return _to_response(shipment)


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(
    shipment_id: str,
    service: ShipmentService = Depends(get_service),
) -> None:
    try:
        service.delete(shipment_id)
    except ShipmentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
