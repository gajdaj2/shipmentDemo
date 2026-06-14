import db


from fastapi import  HTTPException, status


def check_shipment_field(field: str, id: int):
    """
    Validates the existence of a shipment record and a specific field within it.

    Args:
        field (str): The name of the field to check within the shipment record.
        id (int): The unique identifier of the shipment record to look up.

    Raises:
        HTTPException: 404 Not Found if the shipment with the given `id` does not
            exist in the database.
        HTTPException: 404 Not Found if the specified `field` does not exist within
            the shipment record identified by `id`.
    """
    if id not in db.shipment_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found",
        )
    if field not in db.shipment_records[id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Field {field} not found in shipment with id {id}",
        )
