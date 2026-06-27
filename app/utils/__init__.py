"""
LexGuard AI — Application Factory
Production-ready Flask app using modular blueprint architecture.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# ── Extension singletons (imported by models/services) ────────────────────────
db           = SQLAlchemy()
login_manager = LoginManager()


def create_app(env: str = None) -> Flask:
    """Create and configure the Flask application."""
    from app.config.settings import config_map

    flask_app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # ── Config ─────────────────────────────────────────────────────────────
    env = env or os.getenv("FLASK_ENV", "development")
    flask_app.config.from_object(config_map.get(env, config_map["default"]))

    # ── Ensure required directories exist ──────────────────────────────────
    os.makedirs(flask_app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(flask_app.config["CORPUS_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(flask_app.config["UPLOAD_FOLDER"], "lawyers"), exist_ok=True)

    # ── Initialise extensions ──────────────────────────────────────────────
    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    login_manager.login_view         = "auth.login"
    login_manager.login_message      = "Please log in to access LexGuard AI."
    login_manager.login_message_category = "warning"

    # ── Register blueprints ────────────────────────────────────────────────
    with flask_app.app_context():
        from app.routes.auth         import auth_bp
        from app.routes.dashboard    import dashboard_bp
        from app.routes.scanner      import scanner_bp
        from app.routes.legal_advisor import legal_bp
        from app.routes.cases        import cases_bp
        from app.routes.lawyers      import lawyers_bp
        from app.routes.protect      import protect_bp
        from app.routes.api          import api_bp
        from app.routes.admin        import admin_bp

        flask_app.register_blueprint(auth_bp,      url_prefix="/auth")
        flask_app.register_blueprint(dashboard_bp)
        flask_app.register_blueprint(scanner_bp,   url_prefix="/scanner")
        flask_app.register_blueprint(legal_bp,     url_prefix="/legal-advisor")
        flask_app.register_blueprint(cases_bp,     url_prefix="/cases")
        flask_app.register_blueprint(lawyers_bp,   url_prefix="/lawyers")
        flask_app.register_blueprint(protect_bp,   url_prefix="/protect")
        flask_app.register_blueprint(api_bp,       url_prefix="/api")
        flask_app.register_blueprint(admin_bp,     url_prefix="/admin")

        # ── Create database tables ─────────────────────────────────────────
        from app.models.user            import User            # noqa: F401
        from app.models.document        import Document, ClauseAnalysis  # noqa: F401
        from app.models.legal_case      import LegalCase       # noqa: F401
        from app.models.lawyer          import Lawyer          # noqa: F401
        from app.models.emergency_alert import EmergencyAlert  # noqa: F401
        db.create_all()

        # ── Load IPC retrieval corpus ──────────────────────────────────────
        from app.utils.ipc_retrieval import IPCRetriever
        flask_app.ipc_retriever = IPCRetriever(flask_app.config["IPC_FILE"])

    return flask_app
