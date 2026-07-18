import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def _normalize_sqlite_url(url: str) -> str:
    if not url.startswith("sqlite:///"):
        return url
    sqlite_path = url[len("sqlite:///"):]
    if not sqlite_path or os.path.isabs(sqlite_path):
        return url
    absolute_path = os.path.join(BASE_DIR, sqlite_path)
    return f"sqlite:///{absolute_path}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        database_url = _normalize_sqlite_url(database_url)
    SQLALCHEMY_DATABASE_URI = (
        database_url
        or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024
    ALLOWED_UPLOAD_EXTENSIONS = {"pdf"}
    WTF_CSRF_ENABLED = True
