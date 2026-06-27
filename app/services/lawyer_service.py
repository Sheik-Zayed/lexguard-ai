"""
Admin Lawyer Service — full CRUD + photo upload for the admin dashboard.
"""
import os
import uuid
from typing import Dict, List
from werkzeug.utils import secure_filename
from flask import current_app
from app import db
from app.models.lawyer import Lawyer

ALLOWED_PHOTO_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


# ─── Public Directory ─────────────────────────────────────────────────────────

def find_lawyers(city: str = None, specialization: str = None,
                 min_rating: float = 0.0, search: str = None) -> Dict:
    """Filter lawyers from database with optional name search."""
    q = Lawyer.query

    if search and search.strip():
        q = q.filter(Lawyer.name.ilike(f"%{search.strip()}%"))

    if city and city.strip():
        q = q.filter(Lawyer.location.ilike(f"%{city.strip()}%"))

    if specialization and specialization.strip():
        q = q.filter(Lawyer.specialization.ilike(f"%{specialization.strip()}%"))

    if min_rating and min_rating > 0:
        q = q.filter(Lawyer.rating >= min_rating)

    lawyers = q.order_by(Lawyer.rating.desc()).all()
    return {
        "success": True,
        "count": len(lawyers),
        "lawyers": [l.to_dict() for l in lawyers],
    }


def get_specializations() -> List[str]:
    """Distinct specializations for filter dropdown."""
    rows = Lawyer.query.with_entities(Lawyer.specialization).distinct().all()
    return sorted({r[0] for r in rows if r[0]})


def get_cities() -> List[str]:
    """Distinct cities for filter dropdown."""
    rows = Lawyer.query.with_entities(Lawyer.location).distinct().all()
    return sorted({r[0] for r in rows if r[0]})


# ─── Admin CRUD ───────────────────────────────────────────────────────────────

def admin_list_lawyers(search: str = None, city: str = None,
                       specialization: str = None) -> List[Lawyer]:
    """Return filtered list of all lawyers for admin table."""
    q = Lawyer.query

    if search and search.strip():
        q = q.filter(Lawyer.name.ilike(f"%{search.strip()}%"))
    if city and city.strip():
        q = q.filter(Lawyer.location.ilike(f"%{city.strip()}%"))
    if specialization and specialization.strip():
        q = q.filter(Lawyer.specialization.ilike(f"%{specialization.strip()}%"))

    return q.order_by(Lawyer.name).all()


def admin_get_lawyer(lawyer_id: int) -> Lawyer | None:
    return Lawyer.query.get(lawyer_id)


def admin_create_lawyer(form_data: dict, photo_file=None) -> Dict:
    """Create a new lawyer record, optionally saving a profile photo."""
    try:
        lawyer = Lawyer(
            name             = form_data.get("name", "").strip(),
            specialization   = form_data.get("specialization", "").strip(),
            location         = form_data.get("location", "").strip(),
            contact          = form_data.get("contact", "").strip(),
            email            = form_data.get("email", "").strip(),
            rating           = float(form_data.get("rating", 4.0)),
            experience_years = int(form_data.get("experience_years", 1)),
            bio              = form_data.get("bio", "").strip(),
            bar_council_no   = form_data.get("bar_council_no", "").strip(),
            languages        = form_data.get("languages", "").strip(),
            fee_per_hour     = int(form_data.get("fee_per_hour", 0)),
            is_verified      = bool(form_data.get("is_verified")),
            avatar_initials  = form_data.get("name", "")[:2].upper(),
        )
        if photo_file:
            filename = _save_photo(photo_file)
            if filename:
                lawyer.photo_filename = filename

        db.session.add(lawyer)
        db.session.commit()
        return {"success": True, "id": lawyer.id}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}


def admin_update_lawyer(lawyer_id: int, form_data: dict, photo_file=None) -> Dict:
    """Update an existing lawyer record."""
    lawyer = Lawyer.query.get(lawyer_id)
    if not lawyer:
        return {"success": False, "error": "Lawyer not found."}
    try:
        lawyer.name             = form_data.get("name", lawyer.name).strip()
        lawyer.specialization   = form_data.get("specialization", lawyer.specialization).strip()
        lawyer.location         = form_data.get("location", lawyer.location).strip()
        lawyer.contact          = form_data.get("contact", lawyer.contact or "").strip()
        lawyer.email            = form_data.get("email", lawyer.email or "").strip()
        lawyer.rating           = float(form_data.get("rating", lawyer.rating))
        lawyer.experience_years = int(form_data.get("experience_years", lawyer.experience_years))
        lawyer.bio              = form_data.get("bio", lawyer.bio or "").strip()
        lawyer.bar_council_no   = form_data.get("bar_council_no", lawyer.bar_council_no or "").strip()
        lawyer.languages        = form_data.get("languages", lawyer.languages or "").strip()
        lawyer.fee_per_hour     = int(form_data.get("fee_per_hour", lawyer.fee_per_hour or 0))
        lawyer.is_verified      = bool(form_data.get("is_verified"))
        lawyer.avatar_initials  = lawyer.name[:2].upper()

        if photo_file:
            # Delete old photo
            if lawyer.photo_filename:
                _delete_photo(lawyer.photo_filename)
            filename = _save_photo(photo_file)
            if filename:
                lawyer.photo_filename = filename

        db.session.commit()
        return {"success": True}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}


def admin_delete_lawyer(lawyer_id: int) -> Dict:
    """Delete a lawyer and their profile photo."""
    lawyer = Lawyer.query.get(lawyer_id)
    if not lawyer:
        return {"success": False, "error": "Lawyer not found."}
    try:
        if lawyer.photo_filename:
            _delete_photo(lawyer.photo_filename)
        db.session.delete(lawyer)
        db.session.commit()
        return {"success": True}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}


# ─── Photo Helpers ────────────────────────────────────────────────────────────

def _save_photo(file) -> str | None:
    """Save uploaded photo to uploads/lawyers/ and return filename."""
    try:
        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_PHOTO_EXTENSIONS:
            return None
        unique_name = f"lawyer_{uuid.uuid4().hex}.{ext}"
        folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "lawyers")
        os.makedirs(folder, exist_ok=True)
        file.save(os.path.join(folder, unique_name))
        return unique_name
    except Exception:
        return None


def _delete_photo(filename: str):
    """Delete a photo file from disk."""
    try:
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], "lawyers", filename)
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
