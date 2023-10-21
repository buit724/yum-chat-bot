from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from python.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
