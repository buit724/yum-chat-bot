from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column

from python.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer,primary_key=True)
    display_name: str = Column(String, nullable=False)
    
    def __init__(self, id: int, display_name: str):
        self.id = id
        self.display_name = display_name
        
