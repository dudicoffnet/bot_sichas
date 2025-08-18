from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Integer, Boolean, Text, DateTime, ForeignKey, func
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    interests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo_file_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    last_seen: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ts: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    actor_tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    action: Mapped[str] = mapped_column(String(64))
    target_tg_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

class Ban(Base):
    __tablename__ = "bans"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    banned_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    ts: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class SearchPref(Base):
    __tablename__ = "search_prefs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)
    age_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    age_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    city_filter: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # None/'' -> любой
