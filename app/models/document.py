"""Document & ClauseAnalysis models"""
from app import db
from datetime import datetime


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(80), default="contract")
    risk_score = db.Column(db.Float, default=0.0)   # 0–100 overall risk
    risk_label = db.Column(db.Enum("LOW", "MEDIUM", "HIGH"), default="LOW")
    clause_count = db.Column(db.Integer, default=0)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)

    clauses = db.relationship("ClauseAnalysis", backref="document", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "original_name": self.original_name,
            "document_type": self.document_type,
            "risk_score": self.risk_score,
            "risk_label": self.risk_label,
            "clause_count": self.clause_count,
            "upload_time": self.upload_time.strftime("%d %b %Y, %I:%M %p"),
        }

    def __repr__(self):
        return f"<Document {self.original_name} [{self.risk_label}]>"


class ClauseAnalysis(db.Model):
    __tablename__ = "clause_analysis"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"), nullable=False)
    clause_number = db.Column(db.Integer, default=1)
    clause_text = db.Column(db.Text, nullable=False)
    clause_type = db.Column(db.String(80), default="general")
    risk_level = db.Column(db.Enum("LOW", "MEDIUM", "HIGH"), default="LOW")
    explanation = db.Column(db.Text)
    suggested_fix = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "clause_number": self.clause_number,
            "clause_text": self.clause_text,
            "clause_type": self.clause_type,
            "risk_level": self.risk_level,
            "explanation": self.explanation,
            "suggested_fix": self.suggested_fix,
        }
