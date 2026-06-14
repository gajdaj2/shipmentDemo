from models.shipment_model import ShipmentModel


shipment_records: dict[int, ShipmentModel] = {
    6: ShipmentModel(weight=3.7, content="leather sofa", status="In transit"),
    7: ShipmentModel(weight=0.8, content="cotton pillow", status="Delivered"),
    8: ShipmentModel(weight=7.5, content="iron gate", status="In transit"),
    9: ShipmentModel(weight=1.0, content="silver frame", status="Delivered"),
    10: ShipmentModel(weight=4.2, content="oak bookcase", status="In transit"),
    11: ShipmentModel(weight=2.0, content="plastic bucket", status="Delivered"),
    12: ShipmentModel(weight=9.0, content="marble statue", status="In transit"),
    13: ShipmentModel(weight=0.3, content="glass bottle", status="Delivered"),
    14: ShipmentModel(weight=6.5, content="steel ladder", status="In transit"),
    15: ShipmentModel(weight=1.8, content="wooden frame", status="Delivered"),
    1: ShipmentModel(weight=1.2, content="wooden table", status="In transit"),
    2: ShipmentModel(weight=0.5, content="plastic chair", status="Delivered"),
    3: ShipmentModel(weight=10.0, content="metal shelf", status="In transit"),
    4: ShipmentModel(weight=5.0, content="glass vase", status="Delivered"),
    5: ShipmentModel(weight=2.5, content="ceramic mug", status="In transit"),
}
