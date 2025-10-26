import os

DATABASE_URL = os.environ.get("DATABASE_URL", "")

IMAP_SERVER = os.environ.get("IMAP_SERVER", "")
IMAP_PORT = int(os.environ.get("IMAP_PORT", 993))
EMAIL_ACCOUNT = os.environ.get("EMAIL_ACCOUNT", "")
APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD", "")
