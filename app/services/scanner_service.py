"""Scanner service — orchestrates PDF extraction, risk analysis, and DB persistence."""
import os
import uuid
from flask import current_app
from app import db
from app.models.document import Document, ClauseAnalysis
from app.utils.pdf_extractor import extract_text, split_into_clauses
from app.utils.risk_analyzer import analyze_clause, compute_document_risk


ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file) -> str:
    """Save uploaded file securely, return file path."""
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, unique_name)
    file.save(file_path)
    return file_path, unique_name


def scan_document(file, user_id: int) -> dict:
    """
    Full pipeline:
    1. Save file
    2. Extract text
    3. Split clauses
    4. Analyze each clause
    5. Persist to DB
    6. Return structured result
    """
    if not file or not allowed_file(file.filename):
        return {"success": False, "error": "Only PDF files are supported."}

    try:
        file_path, unique_name = save_uploaded_file(file)
    except Exception as e:
        return {"success": False, "error": f"File save failed: {e}"}

    try:
        text = extract_text(file_path)
    except Exception as e:
        return {"success": False, "error": f"PDF extraction failed: {e}"}

    if not text.strip():
        return {"success": False, "error": "Could not extract text from the PDF. Try a text-based PDF."}

    clauses = split_into_clauses(text)
    # Limit to 20 clauses for performance
    clauses = clauses[:20]

    analyzed_clauses = [analyze_clause(i, c) for i, c in enumerate(clauses)]
    risk_score, risk_label = compute_document_risk(analyzed_clauses)

    # Persist to DB
    doc = Document(
        user_id=user_id,
        file_path=file_path,
        original_name=file.filename,
        document_type=_detect_doc_type(text),
        risk_score=risk_score,
        risk_label=risk_label,
        clause_count=len(analyzed_clauses),
    )
    db.session.add(doc)
    db.session.flush()  # get doc.id before committing

    for c in analyzed_clauses:
        clause = ClauseAnalysis(
            document_id=doc.id,
            clause_number=c["clause_number"],
            clause_text=c["clause_text"],
            clause_type=c["clause_type"],
            risk_level=c["risk_level"],
            explanation=c["explanation"],
            suggested_fix=c["suggested_fix"],
        )
        db.session.add(clause)

    db.session.commit()

    heatmap = {
        "high": sum(1 for c in analyzed_clauses if c["risk_level"] == "HIGH"),
        "medium": sum(1 for c in analyzed_clauses if c["risk_level"] == "MEDIUM"),
        "low": sum(1 for c in analyzed_clauses if c["risk_level"] == "LOW"),
    }

    return {
        "success": True,
        "document_id": doc.id,
        "document_name": file.filename,
        "risk_score": risk_score,
        "risk_label": risk_label,
        "clause_count": len(analyzed_clauses),
        "heatmap": heatmap,
        "clauses": analyzed_clauses,
    }


def get_document_history(user_id: int) -> list:
    """Return all documents for a user."""
    docs = Document.query.filter_by(user_id=user_id).order_by(Document.upload_time.desc()).all()
    return [d.to_dict() for d in docs]


def get_document_detail(doc_id: int, user_id: int) -> dict:
    """Return full analysis for a single document."""
    doc = Document.query.filter_by(id=doc_id, user_id=user_id).first()
    if not doc:
        return {"success": False, "error": "Document not found."}

    clauses = ClauseAnalysis.query.filter_by(document_id=doc_id).order_by(ClauseAnalysis.clause_number).all()
    return {
        "success": True,
        "document": doc.to_dict(),
        "clauses": [c.to_dict() for c in clauses],
    }


def _detect_doc_type(text: str) -> str:
    """Heuristic document type detection from text."""
    lower = text.lower()
    if "employment" in lower or "employee" in lower or "employer" in lower:
        return "employment"
    if "lease" in lower or "rent" in lower or "tenant" in lower:
        return "rental"
    if "service agreement" in lower or "scope of work" in lower:
        return "service"
    if "non-disclosure" in lower or "nda" in lower:
        return "nda"
    return "contract"
