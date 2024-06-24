#!./venv/bin/python3

import asyncio
from typing import List

from sqlalchemy import event, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import Session

engine = create_async_engine(
    "mysql+aiomysql://somzzy:somzzy@localhost/test_async_event"
)


def use_inspector(conn: DBAPIConnection) -> List[str]:
    """Get table names in database"""
    inspector = inspect(conn)
    print(inspector.get_view_names())

    return inspector.get_table_names()


async def async_main():
    async with engine.connect() as conn:
        tables = await conn.run_sync(use_inspector)
        print(tables)
    await engine.dispose()

asyncio.run(async_main())
