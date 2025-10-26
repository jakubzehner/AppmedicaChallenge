from fastapi import Depends
from sqlmodel import Session, select
from appmedica.database import get_session
from appmedica.database.mail import MailModel


def get_mail_service(db: Session = Depends(get_session)):
    return MailService(db)


class MailService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_mails(self) -> list[MailModel]:
        query = select(MailModel)
        results = self.db.exec(query).all()
        return list(results)
