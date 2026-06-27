"""Scanner routes."""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.scanner_service import scan_document, get_document_history, get_document_detail

scanner_bp = Blueprint("scanner", __name__)


@scanner_bp.route("/")
@login_required
def index():
    return render_template("scanner.html")


@scanner_bp.route("/history")
@login_required
def history():
    docs = get_document_history(current_user.id)
    return render_template("history.html", documents=docs)


@scanner_bp.route("/detail/<int:doc_id>")
@login_required
def detail(doc_id):
    result = get_document_detail(doc_id, current_user.id)
    if not result["success"]:
        return render_template("scanner.html", error=result["error"])
    return render_template("scanner_detail.html", document=result["document"], clauses=result["clauses"])
