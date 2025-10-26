import typing as t

from sqlalchemy import Engine, create_engine
from sqlmodel import Session, SQLModel

import appmedica.config as config
from appmedica.database.mail import MailModel

_engine: t.Optional[Engine] = None


def setup_database() -> Engine:
    global _engine
    if _engine:
        return _engine

    _engine = create_engine(config.DATABASE_URL)
    SQLModel.metadata.create_all(_engine)

    return _engine


def get_session():
    global _engine

    with Session(_engine) as session:
        yield session


models = [MailModel]

__all__ = ["setup_database", "get_session", "models"]
