import asyncio
import re

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr

from config.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


REGULAR_COMP = re.compile(r"((?<=[a-z\d])[A-Z]|(?!^)[A-Z](?=[a-z]))")


def camel_to_snake(camel_string):
    return REGULAR_COMP.sub(r"_\1", camel_string).lower()


def get_db_url() -> str:
    return (
        f"postgresql+asyncpg://"
        f"{DB_USER}:"
        f"{DB_PASS}@"
        f"{DB_HOST}:"
        f"{DB_PORT}/"
        f"{DB_NAME}"
    )


class ClsBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    def as_dict(self, *exclude_fields: str):
        """Возвращает данные в виде словаря"""
        exclude_fields = list(exclude_fields)
        exclude_fields.append("_sa_instance_state")
        return {
            name: value
            for name, value in self.__dict__.items()
            if name not in exclude_fields
        }


engine = create_async_engine(
    get_db_url(),
    echo=False,
)
Base = declarative_base(cls=ClsBase)
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def create_db(delete: bool = False):
    async with engine.begin() as conn:
        if delete:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
