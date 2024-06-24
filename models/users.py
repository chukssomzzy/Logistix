#!/usr/bin/python3

"""A User model"""
from __future__ import annotations

from typing import Dict, Optional, List

import aiobcrypt
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.addresses import Address
from models.packages import Package
from models.base import Base


class User(Base):
    """Defines the user model"""
    __tablename__ = "users"
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    _password_hash: Mapped[str] = mapped_column(String(255))
    address_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey('addresses.id'))
    address: Mapped[Optional[Address]] = relationship()
    packages: Mapped[Optional[List[Package]]] = relationship()
    __table_args__ = (
        Index("i_email_first_last", "email_address", "first_name", "last_name",
              unique=True),
        Index("i_created_at", "created_at"),
        Index("i_updated_at", "updated_at"),
        Index("i_id_created_updated", "id", "created_at", "updated_at",
              unique=True),
    )

    async def __init__(self, *args, **kwargs):
        """Initializes user object"""
        if kwargs:
            if "password" in kwargs:
                self._password_hash = str(await aiobcrypt.hashpw(
                    bytes(kwargs["password"], "utf-8"),
                    await aiobcrypt.gensalt()))
                del kwargs["password"]
        super().__init__(*args, **kwargs)

    async def check_password(self, password) -> bool:
        """Check if the users password is correct"""
        return await aiobcrypt.checkpw(password,
                                       bytes(self._password_hash, "utf-8"))

    @property
    def password(self):
        """Get the value of password"""
        return None

    @password.setter
    async def password(self, password):
        """Set the password value on an object"""
        self._password_hash = str(await aiobcrypt.hashpw(
            bytes(password, "utf-8"), await aiobcrypt.gensalt()))

    def to_dict(self) -> Dict:
        """Create a serializable user object"""
        dict_copy = super().to_dict()
        if "password_hash" in dict_copy:
            del dict_copy["_password_hash"]
        if "address" in dict_copy:
            dict_copy["address"] = dict_copy["address"].to_dict()
        if "packages" in dict_copy:
            packages = []
            for package in dict_copy["packages"]:
                packages.append(package.to_dict())
        return dict_copy
