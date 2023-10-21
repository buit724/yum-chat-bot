import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from python.models.base import Base


class UserMomentAssoc(Base):
    __tablename__ = "user_moment_assoc"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    moment_id: Mapped[int] = mapped_column(Integer, ForeignKey("moment.id"), nullable=False)
    claimed_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

