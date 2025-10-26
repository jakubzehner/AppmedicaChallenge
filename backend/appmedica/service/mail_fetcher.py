import asyncio
import imaplib
import email
from typing import cast
from email.utils import parsedate_to_datetime
from email.header import decode_header

from sqlmodel import Session, select

import appmedica.config as config
from appmedica.database import get_session
from appmedica.database.mail import MailModel
from appmedica.logger import get_logger

logger = get_logger("service.mail_fetcher")

FULL_MESSAGE = "(RFC822)"


async def mail_fetcher():
    while True:
        try:
            db = next(get_session())
            logger.debug("Fetching unread emails...")
            fetch_unread_emails(db)
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
        await asyncio.sleep(10)


def decode_mime_header(value: str | None) -> str:
    if not value:
        return ""

    decoded_parts = decode_header(value)
    decoded_str = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_str += part.decode(encoding or "utf-8", errors="replace")
        else:
            decoded_str += part

    return decoded_str


def fetch_unread_emails(db: Session):
    logger.debug("Connecting to email server...")
    imap = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
    imap.login(config.EMAIL_ACCOUNT, config.APP_PASSWORD)
    imap.select("inbox")

    logger.debug("Searching for unseen emails...")
    status, messages = imap.search(None, "(UNSEEN)")
    if status != "OK":
        logger.error("Failed to search for unseen emails.")
        imap.close()
        imap.logout()
        return

    email_ids = messages[0].split()
    logger.debug(f"Found {len(email_ids)} unseen emails.")

    for idx in email_ids:
        status, msg_data = imap.fetch(idx, FULL_MESSAGE)

        if status != "OK":
            logger.error(f"Failed to fetch email with ID {idx.decode()}.")
            continue

        msg_data = cast(list[tuple[bytes, bytes]], msg_data)
        msg = email.message_from_bytes(msg_data[0][1])

        # if the email is already in the database, skip it
        query = select(MailModel).where(
            MailModel.message_id == msg.get("Message-ID", "")
        )
        existing_mail = db.exec(query).first()
        if existing_mail:
            logger.warning(
                f"Email with Message-ID {msg.get('Message-ID', '')} already exists. Skipping."
            )
            continue

        mail = MailModel(
            message_id=msg.get("Message-ID", ""),
            subject=decode_mime_header(msg.get("Subject")),
            sender=decode_mime_header(msg.get("From")),
            received_at=parsedate_to_datetime(msg.get("Date", "")),
            attachment_summary="Brak załącznika w obsługiwanym formacie.",
        )

        db.add(mail)
        db.commit()

        imap.store(idx, "+FLAGS", "\\Seen")
        logger.info(
            f"Fetched and stored email with Message-ID {msg.get('Message-ID', '')}."
        )

    imap.close()
    imap.logout()
