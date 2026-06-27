"""Legal advisor routes."""
from flask import Blueprint, render_template

legal_bp = Blueprint("legal", __name__)


@legal_bp.route("/")
def index():
    return render_template("legal_advisor.html")
