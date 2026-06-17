from sqlalchemy import create_engine
from sqlmodel import SQLModel



def create_db_and_tables():
    engine = create_engine("sqlite:///shipments.db",echo=True,connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(bind=engine)



