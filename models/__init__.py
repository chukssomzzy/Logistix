from os import getenv
from typing import Optional
from dotenv import load_dotenv
from models.engine.async_db_engine import AsyncDBStorageEngine

load_dotenv()
engine: Optional[AsyncDBStorageEngine] = None

if getenv("DB_TYPE") == "ASYNC_MYSQL":
    engine = AsyncDBStorageEngine()
