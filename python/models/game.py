from sqlalchemy import String, Column, Integer

from python.models.base import Base


class Game(Base):
    __tablename__ = "game"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

