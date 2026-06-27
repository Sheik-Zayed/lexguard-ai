"""LegalCase model"""
from app import db


class LegalCase(db.Model):
    __tablename__ = "legal_cases"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    act_name = db.Column(db.String(200))
    section = db.Column(db.String(80))
    year = db.Column(db.Integer)
    court = db.Column(db.String(150))
    summary = db.Column(db.Text)
    judgement_text = db.Column(db.Text)
    keywords = db.Column(db.Text)  # comma-separated keywords for search

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "act_name": self.act_name,
            "section": self.section,
            "year": self.year,
            "court": self.court,
            "summary": self.summary,
            "judgement_text": self.judgement_text,
        }
