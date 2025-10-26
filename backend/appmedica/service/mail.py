from typing import cast
from fastapi import Depends
from sqlalchemy import ColumnElement
from sqlmodel import Session, desc, select
from appmedica.database import get_session
from appmedica.database.mail import MailModel


def get_mail_service(db: Session = Depends(get_session)):
    return MailService(db)


class MailService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_mails(self, skip: int, limit: int) -> list[MailModel]:
        query = (
            select(MailModel)
            .order_by(desc(cast(ColumnElement, MailModel.received_at)))
            .offset(skip)
            .limit(limit)
        )
        results = self.db.exec(query).all()
        return list(results)
