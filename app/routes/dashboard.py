"""Dashboard routes."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.document import Document
from app.models.emergency_alert import EmergencyAlert
from app.models.legal_case import LegalCase

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    # Stats for the current user
    total_docs = Document.query.filter_by(user_id=current_user.id).count()
    high_risk = Document.query.filter_by(user_id=current_user.id, risk_label="HIGH").count()
    alerts_sent = EmergencyAlert.query.filter_by(user_id=current_user.id, status="sent").count()
    total_cases = LegalCase.query.count()

    # Recent documents
    recent_docs = (
        Document.query
        .filter_by(user_id=current_user.id)
        .order_by(Document.upload_time.desc())
        .limit(5)
        .all()
    )

    # Risk distribution for chart
    risk_counts = {
        "LOW": Document.query.filter_by(user_id=current_user.id, risk_label="LOW").count(),
        "MEDIUM": Document.query.filter_by(user_id=current_user.id, risk_label="MEDIUM").count(),
        "HIGH": Document.query.filter_by(user_id=current_user.id, risk_label="HIGH").count(),
    }

    return render_template(
        "dashboard.html",
        total_docs=total_docs,
        high_risk=high_risk,
        alerts_sent=alerts_sent,
        total_cases=total_cases,
        recent_docs=recent_docs,
        risk_counts=risk_counts,
    )
