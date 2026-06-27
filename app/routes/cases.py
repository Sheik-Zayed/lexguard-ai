"""Cases routes."""
from flask import Blueprint, render_template
from app.services.case_service import get_all_courts, get_year_range

cases_bp = Blueprint("cases", __name__)


@cases_bp.route("/")
def index():
    courts = get_all_courts()
    year_range = get_year_range()
    return render_template("cases.html", courts=courts, year_range=year_range)
