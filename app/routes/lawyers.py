"""Lawyers routes."""
from flask import Blueprint, render_template
from app.services.lawyer_service import get_specializations, get_cities

lawyers_bp = Blueprint("lawyers", __name__)


@lawyers_bp.route("/")
def index():
    specializations = get_specializations()
    cities = get_cities()
    return render_template("lawyers.html", specializations=specializations, cities=cities)
