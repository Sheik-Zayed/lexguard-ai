"""REST API routes — JSON endpoints for all features."""
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_login import login_required, current_user
from app.services.scanner_service import scan_document
from app.services.legal_service import get_legal_advice
from app.services.case_service import find_similar_cases
from app.services.lawyer_service import find_lawyers
from app.services.protect_service import send_sos, save_audio

api_bp = Blueprint("api", __name__)


@api_bp.route("/upload-document", methods=["POST"])
@login_required
def upload_document():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided."}), 400
    result = scan_document(request.files["file"], current_user.id)
    status = 200 if result["success"] else 400
    return jsonify(result), status


@api_bp.route("/legal-query", methods=["POST"])
def legal_query():
    data = request.get_json(silent=True) or {}
    result = get_legal_advice(data.get("question", ""))
    return jsonify(result)


@api_bp.route("/find-cases", methods=["POST"])
def find_cases():
    data = request.get_json(silent=True) or {}
    result = find_similar_cases(
        query=data.get("query", ""),
        year=data.get("year"),
        court=data.get("court"),
    )
    return jsonify(result)


@api_bp.route("/find-lawyers", methods=["POST"])
def find_lawyers_api():
    data = request.get_json(silent=True) or {}
    result = find_lawyers(
        city=data.get("city", ""),
        specialization=data.get("specialization", ""),
        min_rating=float(data.get("min_rating", 0)),
        search=data.get("search", ""),
    )
    return jsonify(result)


@api_bp.route("/send-alert", methods=["POST"])
@login_required
def send_alert():
    data = request.get_json(silent=True) or {}
    lat = data.get("lat", 0)
    lng = data.get("lng", 0)
    result = send_sos(current_user.id, lat, lng)
    status = 200 if result["success"] else 500
    return jsonify(result), status


@api_bp.route("/save-audio", methods=["POST"])
@login_required
def save_audio_api():
    if "audio" not in request.files:
        return jsonify({"success": False, "error": "No audio file provided."}), 400
    alert_id = request.form.get("alert_id")
    result = save_audio(
        current_user.id,
        request.files["audio"],
        int(alert_id) if alert_id else None
    )
    return jsonify(result)


@api_bp.route("/sync-location", methods=["POST"])
@login_required
def sync_location():
    data = request.get_json(silent=True) or {}
    alert_id = data.get("alert_id")
    lat = data.get("lat")
    lng = data.get("lng")
    
    if not alert_id or lat is None or lng is None:
        return jsonify({"success": False, "error": "Missing data"}), 400
        
    from app.models.emergency_alert import EmergencyAlert
    from app import db
    alert = EmergencyAlert.query.get(alert_id)
    if alert and alert.user_id == current_user.id:
        alert.latitude = lat
        alert.longitude = lng
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Alert not found or unauthorized"}), 404


@api_bp.route("/audio/<filename>")
def serve_audio(filename):
    """Serve audio evidence files so they can be accessed via SOS SMS link."""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@api_bp.route("/dashboard-stats", methods=["GET"])
@login_required
def dashboard_stats():
    from app.models.document import Document
    from app.models.emergency_alert import EmergencyAlert
    docs = Document.query.filter_by(user_id=current_user.id).all()
    risk_data = {
        "LOW": sum(1 for d in docs if d.risk_label == "LOW"),
        "MEDIUM": sum(1 for d in docs if d.risk_label == "MEDIUM"),
        "HIGH": sum(1 for d in docs if d.risk_label == "HIGH"),
    }
    alerts = EmergencyAlert.query.filter_by(user_id=current_user.id).count()
    return jsonify({
        "total_documents": len(docs),
        "risk_distribution": risk_data,
        "total_alerts": alerts,
    })
