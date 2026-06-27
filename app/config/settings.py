"""
LexGuard AI — Configuration Settings
Reads from .env automatically.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Project root = lexguard-ai/  (two levels up from this file: app/config/settings.py)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _build_db_uri() -> str:
    """
    Auto-selects the database:
    - MySQL  → when DB_PASSWORD is set to a real value in .env
    - SQLite → fallback when DB_PASSWORD is blank or still the placeholder
    """
    password = os.getenv("DB_PASSWORD", "")
    is_placeholder = password in ("", "your_mysql_password")

    if is_placeholder:
        db_path = os.path.join(_PROJECT_ROOT, "lexguard_dev.db")
        print(f"[LexGuard] DB: SQLite -> {db_path}")
        return f"sqlite:///{db_path}"
    else:
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        name = os.getenv("DB_NAME", "lexguard_db")
        user = os.getenv("DB_USER", "root")
        print(f"[LexGuard] DB: MySQL -> {user}@{host}:{port}/{name}")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


class Config:
    """Base configuration — loaded from .env."""

    SECRET_KEY = os.getenv("SECRET_KEY", "lexguard-dev-secret-key-change-in-production")
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # File uploads (stored at project root/uploads/)
    UPLOAD_FOLDER = os.path.join(_PROJECT_ROOT, "uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", 10)) * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

    # Legal corpus (stored at project root/legal_corpus/)
    CORPUS_FOLDER = os.path.join(_PROJECT_ROOT, "legal_corpus")
    IPC_FILE = os.path.join(_PROJECT_ROOT, "legal_corpus", "ipc_sections_full.json")
    IPC_FILE_FULL = os.path.join(_PROJECT_ROOT, "legal_corpus", "ipc_sections_full.json")

    # LLM API keys (RAG pipeline)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Twilio SOS
    TWILIO_SID   = os.getenv("TWILIO_SID", "")
    TWILIO_AUTH  = os.getenv("TWILIO_AUTH", "")
    TWILIO_PHONE = os.getenv("TWILIO_PHONE", "")
    SOS_TARGET_PHONE = os.getenv("SOS_TARGET_PHONE", "")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development":  DevelopmentConfig,
    "production":   ProductionConfig,
    "default":      DevelopmentConfig,
}
