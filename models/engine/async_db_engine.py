#!/usr/bin/python3

"""DBengine for mysql database"""

from asyncio import current_task
from os import getenv
from typing import Dict, List, Type, Union
from sqlalchemy import select

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_scoped_session, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import selectinload

from models.addresses import Address
from models.base import Base
from models.package_histories import PackageHistory
from models.packages import Package
from models.users import User


class AsyncDBStorageEngine():
    """Defines a facade class to access the models classes"""
    __classes = {
        "Address": Address,
        "Package": Package,
        "PackageHistory": PackageHistory,
        "User": User
    }
    __engine: AsyncEngine
    __Session: async_scoped_session[AsyncSession]

    async def __init__(self) -> None:
        """Initializes AsyncDBStorageEngine"""
        db_user = getenv("DB_USER")
        db_pass = getenv("DB_PASS")
        db_host = getenv("DB_HOST") or "localhost"
        db_name = getenv("DB_NAME")
        assert db_user
        assert db_pass
        assert db_name
        self.__engine = create_async_engine(
            f"mysql+aiomysql://{db_user}:{db_pass}{db_host}/{db_name}"
        )
        async with self.__engine.begin() as conn:
            if getenv("DEV") == "TEST":
                await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @property
    def session(self) -> AsyncSession:
        """Get a scoped session for the current async task"""
        async_session_factory = async_sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__Session = async_scoped_session(
            async_session_factory,
            scopefunc=current_task
        )
        return self.__Session()

    async def delete(self, *args: List[object]) -> None:
        """delete an object for the database session
        Args:
            args (List[object]): array of object to delete
                from the current session
        """
        for arg in args:
            await self.session.delete(arg)

    async def new(self, *args: List[object]) -> None:
        """Add model object to async session
        Args:
            args (List[Object]): array of object to add
                to the async session
        Return:
            None
        """
        self.session.add_all(args)

    def create(
        self,
        cls: Union[Base, str],
        *args: List[None],
        **kwargs: Dict
    ) -> Union[Base, None]:
        """Create a model class instance
        Args:
            cls (Union[str, Base]): contains the name of a Model class
                or a Model class
            args (List[None]): normally not considered
            kwargs (Dict[str, Any]): contains the attribute of the
                class to create
        Return:
            newly created class object
        """
        cls_object: Union[Base, None] = None

        if cls is str and cls in self.__classes:
            u_cls = self.__classes[cls]
            cls_object = u_cls(**kwargs)
        elif isinstance(cls, type) and issubclass(Base, cls):
            cls_object = cls(**kwargs)
        return cls_object

    async def get(
        self,
        cls: Union[Base, str],
        id: Union[str, int],
        *args
    ) -> Union[Base, None]:
        """Get the object of  'cls' with 'id' from session
        Args:
            cls (str): the class to find the object
            id (Union[str, int]): id of the class
            args (str): list of attribute to load
        Return:
            return an object which is subclass of Base
        """
        u_cls: Union[Type[Base], None] = None
        obj: Union[Base, None] = None

        if cls is str and cls in self.__classes:
            u_cls = self.__classes[cls]
        if u_cls:
            stmt = select(u_cls).where(u_cls.id == id).options(
                selectinload(*args)
            )
            result = await self.session.execute(stmt)
            obj = result.scalars().one()
        return obj
