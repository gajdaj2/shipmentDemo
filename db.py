import json

import sqlite3

from models.shipment_model import ShipmentModel


def initialize_database():
    with open("shipments.json", "r") as json_file:
        connection = sqlite3.connect("shipments.db")
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS shipments
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL,
                    weight REAL NOT NULL,
                    content TEXT NOT NULL)""")

        if cursor.execute("SELECT COUNT(*) FROM shipments").fetchone()[0] == 0:
            shipment_data = json.load(json_file)
            for shipment in shipment_data:
                cursor.execute(
                    "INSERT INTO shipments (status, weight, content) VALUES (?, ?, ?)",
                    (shipment["status"], shipment["weight"], shipment["content"]),
                )
                connection.commit()
            connection.close()


class CRUDDatabase:
    def __init__(self):
        self.shipment_records = {}
        
        
    def get_all_shipments(self) -> list[ShipmentModel]:
        connection = sqlite3.connect("shipments.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shipments")
        rows = cursor.fetchall()
        connection.close()
        return [
            ShipmentModel(status=row[1], weight=row[2], content=row[3]) for row in rows
        ]

    def load_shipments(self):
        connection = sqlite3.connect("shipments.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shipments")
        rows = cursor.fetchall()
        for row in rows:
            id, status, weight, content = row
            self.shipment_records[id] = ShipmentModel(
                status=status, weight=weight, content=content
            )
        connection.close()
        
    def get_shipment(self, id: int) -> ShipmentModel:
        connection = sqlite3.connect("shipments.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shipments WHERE id = ?", (id,))
        row = cursor.fetchone()
        connection.close()
        if row is None:
            raise ValueError(f"Shipment with id {id} not found")
        id, status, weight, content = row
        return ShipmentModel(status=status, weight=weight, content=content)



    def create_shipment(self, shipment_data: ShipmentModel) -> ShipmentModel:
        connection = sqlite3.connect("shipments.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO shipments (status, weight, content) VALUES (?, ?, ?)",
            (shipment_data.status, shipment_data.weight, shipment_data.content),
        )
        connection.commit()
        id = cursor.rowcount + 1
        connection.close()
        self.shipment_records[id] = shipment_data
        return shipment_data

    def update_shipment(self, id: int, shipment_data: ShipmentModel) -> ShipmentModel:
        if id not in self.shipment_records:
            raise ValueError(f"Shipment with id {id} not found")
        connection = sqlite3.connect("shipments.db")
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE shipments SET status = ?, weight = ?, content = ? WHERE id = ?",
            (shipment_data.status, shipment_data.weight, shipment_data.content, id),
        )
        connection.commit()
        connection.close()
        self.shipment_records[id] = shipment_data
        return shipment_data

    def delete_shipment(self, id: int) -> dict[str, ShipmentModel]:
        if id not in self.shipment_records:
            raise ValueError(f"Shipment with id {id} not found")
        connection = sqlite3.connect("shipments.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM shipments WHERE id = ?", (id,))
        connection.commit()
        connection.close()
        deleted_shipment = self.shipment_records.pop(id)
        return {"deleted_shipment": deleted_shipment}
