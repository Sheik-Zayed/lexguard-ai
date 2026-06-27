"""Protect / emergency routes."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.protect_service import get_alert_history

protect_bp = Blueprint("protect", __name__)


@protect_bp.route("/")
@login_required
def index():
    history = get_alert_history(current_user.id)
    return render_template("protect.html", history=history)
