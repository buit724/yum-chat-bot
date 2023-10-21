import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from python.models.base import Base


class Moment(Base):
    __tablename__ = "moment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str]
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("game.id"), nullable=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

