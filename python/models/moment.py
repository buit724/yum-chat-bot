from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime, Column
from sqlalchemy.orm import mapped_column

from python.models.base import Base


class Moment(Base):
    __tablename__ = "moment"

    id: id = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    game_id: id = Column(Integer, ForeignKey("game.id"), nullable=False)
    start_time: datetime = Column(DateTime, nullable=False)
    end_time: datetime = Column(DateTime, nullable=False)

    def __init__(self, name: str, game_id: int, start_time: datetime, end_time: datetime):
        self.name = name
        self.description = "N/A"
        self.game_id = game_id
        self.start_time = start_time
        self.end_time = end_time
