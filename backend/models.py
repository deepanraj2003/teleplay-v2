from sqlalchemy import Column, Integer, String
from backend.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    file_id = Column(String)
