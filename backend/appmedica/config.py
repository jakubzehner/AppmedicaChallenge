import os

# NOTE: Default to DEBUG level, 20 is INFO
LOGGER_LEVEL = int(os.getenv("LOGGER_LEVEL", "10"))

DATABASE_URL = os.environ.get("DATABASE_URL", "")

IMAP_SERVER = os.environ.get("IMAP_SERVER", "")
IMAP_PORT = int(os.environ.get("IMAP_PORT", 993))
EMAIL_ACCOUNT = os.environ.get("EMAIL_ACCOUNT", "")
APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD", "")
