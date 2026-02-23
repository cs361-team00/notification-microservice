# which channel does what (in-app only for now)
import logging

import config

logger = logging.getLogger(__name__)


def send_via_in_app(
    user_id: str,
    subject: str,
    body_text: str,
) -> tuple[bool, str | None]:
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
    if channel == "in-app":
        return send_via_in_app(user_id=user_id, subject=subject, body_text=body_text)
    return False, f"unknown channel: {channel}"
