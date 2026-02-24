import logging
from datetime import datetime, timezone

import config
import preferences.impl as preferences
from send.channels import deliver

logger = logging.getLogger(__name__)


def _build_message(notification_type: str, activity_id: str) -> tuple[str, str]:
    subject = f"Notification: {notification_type}"
    body = f"Activity {activity_id} – {notification_type}. You can check your dashboard for details."
    return subject, body


def send_notification(
    user_id: str,
    activity_id: str,
    notification_type: str,
    channel_hint: list[str] | None = None,
    to_email: str | None = None,
) -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    base = {
        "user_id": user_id,
        "activity_id": activity_id,
        "notification_type": notification_type,
        "timestamp": ts,
    }

    enabled = set(preferences.get_enabled_channels(str(user_id)))
    if channel_hint:
        channels = [c for c in channel_hint if c in config.SUPPORTED_CHANNELS and c in enabled]
    else:
        channels = [c for c in enabled if c in config.SUPPORTED_CHANNELS]
    if not channels:
        logger.info("No channels to send for user_id=%s", user_id)
        return {**base, "status": "success", "error_message": None}

    subject, body_text = _build_message(notification_type, str(activity_id))
    any_success = False
    last_error = None

    for ch in channels:
        ok, err = deliver(
            channel=ch,
            user_id=str(user_id),
            to_email=to_email,
            subject=subject,
            body_text=body_text,
        )
        if ok:
            any_success = True
        else:
            last_error = err
            logger.warning("Channel %s failed for user_id=%s: %s", ch, user_id, err)

    status = "success" if any_success else "failure"
    error_message = None if any_success else last_error
    return {**base, "status": status, "error_message": error_message}
