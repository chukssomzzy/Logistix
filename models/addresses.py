#!/usr/bin/python3

"""Address class"""

from typing import Optional
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Address(Base):
    """Defines the implementation of Addresses class"""
    __tablename__ = "addresses"
    address: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    country_code: Mapped[str] = mapped_column(String(5))
    postal_code: Mapped[Optional[str]] = mapped_column(String(20))

    __table_args__ = (
        Index("i_country_postal", "country_code", "postal_code"),
        Index("i_state_city", "state", "city"),
    )
