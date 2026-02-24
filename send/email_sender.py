# send via Mailgun, with retries
import logging
import time
import requests

import config

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, body_text: str, from_email: str | None = None) -> tuple[bool, str | None]:
    if not config.MAILGUN_API_KEY or not config.MAILGUN_DOMAIN:
        msg = "MAILGUN_API_KEY and MAILGUN_DOMAIN must be set for email"
        logger.warning(msg)
        return False, msg

    sender = from_email or f"noreply@{config.MAILGUN_DOMAIN}"
    url = f"{config.MAILGUN_BASE_URL}/{config.MAILGUN_DOMAIN}/messages"
    auth = ("api", config.MAILGUN_API_KEY)
    data = {"from": sender, "to": to_email, "subject": subject, "text": body_text}
    last_error = None

    for attempt in range(1, config.MAILGUN_RETRY_COUNT + 1):
        try:
            logger.info("Mailgun send attempt %s for to=%s", attempt, to_email)
            r = requests.post(url, auth=auth, data=data, timeout=config.SEND_TIMEOUT_SECONDS)
            if r.ok:
                logger.info("Mailgun delivery success to=%s", to_email)
                return True, None
            last_error = f"Mailgun HTTP {r.status_code}: {r.text[:200]}"
            logger.warning("attempt %s failed: %s", attempt, last_error)
        except requests.RequestException as e:
            last_error = str(e)
            logger.warning("attempt %s error: %s", attempt, last_error)
        if attempt < config.MAILGUN_RETRY_COUNT:
            time.sleep(config.MAILGUN_RETRY_BACKOFF_SECONDS)

    return False, last_error
