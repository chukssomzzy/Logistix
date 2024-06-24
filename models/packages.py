#!/usr/bin/python3
"""Packages Model"""

from enum import Enum
from typing import Dict
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.addresses import Address
from models.base import Base
from datetime import date


class PackageStatus(Enum):
    """Enum class 'package_status'"""
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    returned = "returned"
    lost = "lost"


class Package(Base):
    """Defines the implementation for packages"""
    __tablename__ = "packages"
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(30))
    weight: Mapped[float]
    pickup_location_id = mapped_column(ForeignKey("addresses.id"))
    pickup_date:  Mapped[date]
    status: Mapped[PackageStatus] = mapped_column(
        default=PackageStatus.pending)
    pickup_address: Mapped[Address] = relationship()

    __table_args__ = (
        Index("i_user_status_pickup", "user_id", "status", "pickup_date"),
        Index("i_user_id_updated_status", "user_id", "updated_at", "status"),
        Index("i_id_weight", "id", "weight", unique=True),
        Index("i_pickup_location_id", "pickup_location_id"),
        Index("i_pickup_date", "pickup_date"),
        Index("i_id_created_at", "id", "created_at"),
    )

    def to_dict(self) -> Dict:
        """Return serializable Package instance"""
        dict_copy = super().to_dict()
        if "pickup_address" in dict_copy:
            dict_copy["pickup_address"] = dict_copy["pickup_address"].to_dict()
        return dict_copy
