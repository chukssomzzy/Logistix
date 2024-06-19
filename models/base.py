#!/usr/bin/python3

"""Model Base Class for generalization"""
import copy
import random
import string
from datetime import datetime
from time import time
from typing import Dict
from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """Defines Async Base Class For the Model"""
    _class_atr = {"id": uuid4, "updated_at": datetime.fromisoformat,
                  "created_at":  datetime.fromisoformat}
    _class_abr = "BSE"
    _repr_arg = ["id", "created_at", "updated_at"]
    id: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.utcnow)

    def __init__(self, *args, **kwargs) -> None:
        """Initializes the base class from kwargs"""
        if kwargs:
            for k, v in kwargs:
                if k not in Base._class_atr:
                    setattr(self, k, v)
                else:
                    setattr(self, k, Base._class_atr[k](v))
        else:
            self.id = self.__gen_id()
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __gen_id(self) -> str:
        """Generate id for a class"""
        timestamp = time()
        rand_char = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{self._class_abr}{str(timestamp)}{rand_char}"

    def __str__(self) -> str:
        """Get the string representation of an object"""
        return f"[{self.__class__.__name__}.{self.id!s}]({self.__dict__!s})"

    def __repr__(self) -> str:
        """convert a object to its string representation"""
        repr_arg = self._repr_arg.extend(Base._repr_arg)
        repr_str = f"{self.__class__.__name__}("
        if repr_arg:
            repr_arg = set(repr_arg)
            for i, arg in enumerate(repr_arg):
                repr_str += f"{arg}={getattr(self, arg)!r}"
                if i != (len(repr_arg) - 1):
                    repr_str += ", "
        repr_str += ")"
        return repr_str

    def update(self, *args, **kwargs) -> None:
        """Update a model object properties"""
        for k, v in kwargs.items():
            if k not in self._class_atr:
                setattr(self, k, v)
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict:
        """Convert object to a json serializable form"""
        dict_copy = copy.deepcopy(self.__dict__)

        if "created_at" in dict_copy:
            dict_copy["created_at"] = dict_copy["created_at"].isoformat()
        if "updated_at" in dict_copy:
            dict_copy["updated_at"] = dict_copy["updated_at"].isoformat()

        if "__class__" in dict_copy:
            dict_copy["__class__"] = self.__class__.__name__
        return dict_copy
