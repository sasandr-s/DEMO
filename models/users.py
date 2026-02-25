from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class UserORM(Base):
    __tablename__ = "users" 
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255), default="user")