"""Emergency / protect service — SOS SMS and alert persistence."""
import os
import requests
from datetime import datetime
from flask import current_app
from app import db
from app.models.emergency_alert import EmergencyAlert


def send_sos(user_id: int, lat: float, lng: float) -> dict:
    """
    1. Persist alert to DB
    2. Send SMS via Twilio
    3. Update alert status
    """
    alert = EmergencyAlert(
        user_id=user_id,
        latitude=lat,
        longitude=lng,
        timestamp=datetime.utcnow(),
        status="pending",
    )
    db.session.add(alert)
    db.session.flush()

    twilio_sid = current_app.config["TWILIO_SID"]
    twilio_auth = current_app.config["TWILIO_AUTH"]
    twilio_phone = current_app.config["TWILIO_PHONE"]
    target_phone = current_app.config["SOS_TARGET_PHONE"]

    if not twilio_sid or not twilio_auth:
        alert.status = "failed"
        db.session.commit()
        return {"success": False, "error": "Twilio credentials not configured.", "alert_id": alert.id}

    maps_url = f"https://maps.google.com/?q={lat},{lng}"
    body = f"🚨 LEXGUARD EMERGENCY!\nI need help. My location:\n{maps_url}"

    url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
    try:
        response = requests.post(
            url,
            data={"To": target_phone, "From": twilio_phone, "Body": body},
            auth=(twilio_sid, twilio_auth),
            timeout=10,
        )
        if response.status_code == 201:
            sid = response.json().get("sid", "")
            alert.status = "sent"
            alert.twilio_sid = sid
            db.session.commit()
            return {"success": True, "alert_id": alert.id, "twilio_sid": sid}
        else:
            alert.status = "failed"
            db.session.commit()
            return {"success": False, "error": response.text, "alert_id": alert.id}
    except Exception as e:
        alert.status = "failed"
        db.session.commit()
        return {"success": False, "error": str(e), "alert_id": alert.id}


def save_audio(user_id: int, audio_file, alert_id: int = None) -> dict:
    """Save audio evidence file, link to alert if provided."""
    from datetime import datetime
    filename = datetime.utcnow().strftime("Evidence_%Y%m%d%H%M%S.webm")
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    audio_file.save(path)

    if alert_id:
        alert = EmergencyAlert.query.get(alert_id)
        if alert and alert.user_id == user_id:
            alert.audio_file = path
            db.session.commit()

    return {"success": True, "filename": filename}


def get_alert_history(user_id: int) -> list:
    """Return alert history for a user, newest first."""
    alerts = EmergencyAlert.query.filter_by(user_id=user_id).order_by(EmergencyAlert.timestamp.desc()).all()
    return [a.to_dict() for a in alerts]
