from datetime import datetime
from pydantic import BaseModel


class MailDTO(BaseModel):
    id: int
    subject: str
    sender: str
    received_at: datetime
    attachment_summary: str

    model_config = {"from_attributes": True}
