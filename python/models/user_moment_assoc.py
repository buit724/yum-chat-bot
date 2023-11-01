import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime, Column
from sqlalchemy.orm import Mapped, mapped_column

from python.models.base import Base


class UserMomentAssoc(Base):
    __tablename__ = "user_moment_assoc"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("user.id"), nullable=False)
    moment_id: int = Column(Integer, ForeignKey("moment.id"), nullable=False)
    claimed_time: datetime.datetime = Column(DateTime, nullable=False)

    def __init__(self, user_id: int, moment_id: int, claimed_time):
        self.user_id = user_id
        self.moment_id = moment_id
        self.claimed_time = claimed_time
