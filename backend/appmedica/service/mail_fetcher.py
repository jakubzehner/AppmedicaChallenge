import asyncio
import imaplib
import email
from typing import cast
from email.utils import parsedate_to_datetime
from email.header import decode_header
from email.message import Message

from sqlmodel import Session, select

import appmedica.config as config
from appmedica.database import get_session
from appmedica.database.mail import MailModel
from appmedica.logger import get_logger
from appmedica.service.gemini import describe_file

logger = get_logger("service.mail_fetcher")

FULL_MESSAGE = "(RFC822)"
SUPPORTED_ATTACHMENT_TYPES = ["application/pdf", "image/jpeg", "image/png"]
MAX_ATTACHMENT_SIZE = 20 * 1024 * 1024  # 20 MB


async def mail_fetcher():
    while True:
        try:
            db = next(get_session())
            logger.debug("Fetching unread emails...")
            _fetch_unread_emails(db)
        except Exception as e:
            logger.error("Error while fetching emails: %s", e)
        await asyncio.sleep(10)


def _decode_mime_header(value: str | None) -> str:
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


def _describe_attachment(msg: Message, message_id: str) -> str:
    found_too_large_correct_attachment = False
    logger.debug(f"Describing attachment for message {message_id}...")
    for part in msg.walk():
        content_disposition = part.get("Content-Disposition", "")
        if "attachment" not in content_disposition:
            logger.debug(f"Skipping non-attachment part in message {message_id}.")
            continue

        content_type = part.get_content_type()
        if content_type not in SUPPORTED_ATTACHMENT_TYPES:
            logger.debug(
                f"Skipping unsupported attachment type {content_type} in message {message_id}."
            )
            continue

        payload = part.get_payload(decode=True)
        if not isinstance(payload, (bytes, bytearray)):
            logger.debug(
                f"Attachment payload in message {message_id} is not bytes (got {type(payload)}). Skipping."
            )
            continue

        file_size = len(payload)
        if file_size > MAX_ATTACHMENT_SIZE:
            found_too_large_correct_attachment = True
            logger.warning(
                f"Attachment in message {message_id} exceeds 20MB ({file_size / (1024 * 1024):.2f} MB). Skipping."
            )
            continue

        return describe_file(content_type, payload, message_id)

    if found_too_large_correct_attachment:
        return "Załącznik przekracza limit 20MB."
    return "Brak załącznika w obsługiwanym formacie."


def _fetch_unread_emails(db: Session):
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
        msg_id = msg.get("Message-ID", "")

        # if the email is already in the database, skip it
        query = select(MailModel).where(MailModel.message_id == msg_id)
        existing_mail = db.exec(query).first()
        if existing_mail:
            logger.warning(f"Email with Message-ID {msg_id} already exists. Skipping.")
            continue

        mail = MailModel(
            message_id=msg_id,
            subject=_decode_mime_header(msg.get("Subject")),
            sender=_decode_mime_header(msg.get("From")),
            received_at=parsedate_to_datetime(msg.get("Date", "")),
            attachment_summary=_describe_attachment(msg, msg_id),
        )

        db.add(mail)
        db.commit()

        imap.store(idx, "+FLAGS", "\\Seen")
        logger.info(f"Fetched and stored email with Message-ID {msg_id}.")

    imap.close()
    imap.logout()
