from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

engine = create_engine("sqlite:///shipments.db",echo=True,connect_args={"check_same_thread": False})

def create_db_and_tables():
    from .model import Shipment
    SQLModel.metadata.create_all(bind=engine)




def get_db():
    with Session(engine, autocommit=False) as session:
        yield session
