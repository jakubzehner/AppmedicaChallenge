from fastapi import APIRouter, Depends

from appmedica.api.dto.mail import MailDTO
from appmedica.service.mail import get_mail_service, MailService

mail_router = APIRouter(prefix="/mail", tags=["mail"])


@mail_router.get("", response_model=list[MailDTO], status_code=200)
async def get_all_mails(
    skip: int = 0,
    limit: int = 10,
    mail_service: MailService = Depends(get_mail_service),
):
    mails = mail_service.get_all_mails(skip=skip, limit=limit)
    return [MailDTO.model_validate(mail) for mail in mails]
