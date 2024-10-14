import os
import sys
sys.path.append(os.getcwd())
from sqlalchemy.orm import DeclarativeBase
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from queries.setting import load_config

engine = create_async_engine(load_config(), echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

