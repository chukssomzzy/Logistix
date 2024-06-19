#!/usr/bin/python3
"""Packages Model"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Package(Base):
    """Defines the implementation for packages"""
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("users.id"))
    name:
