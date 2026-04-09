from sqlalchemy import Column, Integer, String
from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    file_id = Column(String)

# Create table
Base.metadata.create_all(bind=engine)
