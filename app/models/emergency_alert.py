"""EmergencyAlert model"""
from app import db
from datetime import datetime


class EmergencyAlert(db.Model):
    __tablename__ = "emergency_alerts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum("sent", "failed", "pending"), default="pending")
    twilio_sid = db.Column(db.String(100))
    audio_file = db.Column(db.String(500))

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.strftime("%d %b %Y, %I:%M %p"),
            "status": self.status,
            "maps_url": f"https://maps.google.com/?q={self.latitude},{self.longitude}" if self.latitude else None,
        }
