from fastapi import HTTPException, status


def check_shipment_requirements(shipment_data):
    if "weight" not in shipment_data or "content" not in shipment_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Shipment data must contain 'weight' and 'content' fields",
        )
    if shipment_data["weight"] > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight cannot exceed 25 kg",
        )
