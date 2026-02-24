# which channel does what (email = Mailgun, in-app = log for now)
import logging

import config
from send.email_sender import send_email

logger = logging.getLogger(__name__)


def send_via_email(to_email: str, subject: str, body_text: str) -> tuple[bool, str | None]:
    return send_email(to_email=to_email, subject=subject, body_text=body_text)


def send_via_in_app(user_id: str, subject: str, body_text: str) -> tuple[bool, str | None]:
    logger.info("In-app notification user_id=%s subject=%s", user_id, subject)
    return True, None


def deliver(
    channel: str,
    *,
    user_id: str,
    to_email: str | None,
    subject: str,
    body_text: str,
) -> tuple[bool, str | None]:
    if channel == "email":
        if not to_email:
            return False, "email channel needs 'email' in request body"
        return send_via_email(to_email=to_email, subject=subject, body_text=body_text)
    if channel == "in-app":
        return send_via_in_app(user_id=user_id, subject=subject, body_text=body_text)
    return False, f"unknown channel: {channel}"
