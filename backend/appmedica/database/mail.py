from datetime import datetime

from sqlmodel import Field, SQLModel


class MailModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    message_id: str = Field(unique=True, nullable=False, index=True)
    subject: str = Field(nullable=False)
    sender: str = Field(nullable=False)
    received_at: datetime = Field(nullable=False)
    attachment_summary: str = Field(nullable=False)
