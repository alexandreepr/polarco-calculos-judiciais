from sqlalchemy import Column, Integer, String
from .base import BaseModel

class Client(BaseModel):
    __tablename__ = "clients"

    name = Column(String(255), nullable=False, unique=True)