from db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime
from datetime import datetime

class RequestORM(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    location: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(255),default="Новая")
    pay: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime] = mapped_column(DateTime)
    user: Mapped["UserORM"] = relationship(lazy="joined")
