"""Lawyer model — extended with photo_filename field"""
import os
from app import db


class Lawyer(db.Model):
    __tablename__ = "lawyers"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(150), nullable=False)
    specialization    = db.Column(db.String(150), nullable=False)
    location          = db.Column(db.String(150), nullable=False)
    contact           = db.Column(db.String(200))
    email             = db.Column(db.String(200))
    rating            = db.Column(db.Float, default=4.0)
    experience_years  = db.Column(db.Integer, default=1)
    bio               = db.Column(db.Text)
    photo_filename    = db.Column(db.String(255))        # uploaded profile photo
    avatar_initials   = db.Column(db.String(3))          # fallback "RK"
    is_verified       = db.Column(db.Boolean, default=False)
    bar_council_no    = db.Column(db.String(100))        # Bar Council registration
    languages         = db.Column(db.String(255))        # comma-separated
    fee_per_hour      = db.Column(db.Integer, default=0) # INR

    def to_dict(self):
        return {
            "id":                self.id,
            "name":              self.name,
            "specialization":    self.specialization,
            "location":          self.location,
            "contact":           self.contact,
            "email":             self.email,
            "rating":            self.rating,
            "experience_years":  self.experience_years,
            "bio":               self.bio,
            "photo_filename":    self.photo_filename,
            "avatar_initials":   self.avatar_initials or self.name[:2].upper(),
            "is_verified":       self.is_verified,
            "bar_council_no":    self.bar_council_no,
            "languages":         self.languages or "",
            "fee_per_hour":      self.fee_per_hour,
        }
