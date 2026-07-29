import time
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, JSON, ForeignKey, Text

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="developer")
    organization_id: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[float] = mapped_column(Float, default=time.time)

class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="v1.0.0")
    model: Mapped[str] = mapped_column(String(100), default="gpt-4o")
    environment: Mapped[str] = mapped_column(String(50), default="production")
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    created_at: Mapped[float] = mapped_column(Float, default=time.time)

class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    severity: Mapped[str] = mapped_column(String(20), default="HIGH")
    description: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="MITIGATED")
    created_at: Mapped[float] = mapped_column(Float, default=time.time)
