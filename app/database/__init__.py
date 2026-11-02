    
from app.database.connection import Base, engine
from app.database import models  # Registers the database models


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
