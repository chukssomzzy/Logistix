#!/usr/bin/python3

"""Package History Model"""

from typing import Dict, Optional

from sqlalchemy import Column, ForeignKey, Index, Table
from sqlalchemy.orm import Mapped, mapped_column

from models.addresses import Address
from models.base import Base
from models.packages import PackageStatus, relationship

packages_history_association = (
    Table("packages_histories",
          Base.metadata,
          Column("package_id", ForeignKey("packages.id"), primary_key=True),
          Column("package_history_id", ForeignKey("package_histories.id"),
                 primary_key=True)
          )
)


class PackageHistory(Base):
    """Defines package history class"""
    __tablename__ = "package_histories"
    location_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("addresses.id"))
    status: Mapped[PackageStatus] = mapped_column(
        default=PackageStatus.pending)
    location: Mapped[Optional[Address]] = relationship()

    __table_args__ = (
        Index("i_location_id", "location_id", "status"),
        Index("i_created_at", "created_at"),
        Index("i_updated-at", "updated_at"),
    )

    def to_dict(self) -> Dict:
        """Return the serializable form PackageHistory instance"""
        dict_copy = super().to_dict()
        if "status" in dict_copy:
            dict_copy["status"] = dict_copy["status"].value()
        if "location" in dict_copy:
            dict_copy["location"] = dict_copy["location"].to_dict()
        return dict_copy
