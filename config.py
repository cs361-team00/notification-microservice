import os

# Mailgun (set these in .env for email to work)
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", "")
MAILGUN_BASE_URL = os.environ.get("MAILGUN_BASE_URL", "https://api.mailgun.net/v3").rstrip("/")

# retry a few times so we don't drop emails on first failure
MAILGUN_RETRY_COUNT = 3
MAILGUN_RETRY_BACKOFF_SECONDS = 0.5
SEND_TIMEOUT_SECONDS = 4

# channels we support
SUPPORTED_CHANNELS = {"email", "in-app"}
