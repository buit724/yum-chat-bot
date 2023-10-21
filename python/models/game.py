from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from python.models.base import Base


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
