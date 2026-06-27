"""
Case matching service — TF-IDF similarity search over legal_cases table.
Builds an in-memory TF-IDF matrix on first call after DB load.
"""
import re
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models.legal_case import LegalCase

# ── In-memory TF-IDF corpus cache ────────────────────────────────────────────
_tfidf_vectorizer = None
_tfidf_matrix     = None
_case_index       = []          # list of LegalCase.id in matrix row order


def _build_tfidf():
    """Build TF-IDF matrix from the DB on first call or when cache is stale."""
    global _tfidf_vectorizer, _tfidf_matrix, _case_index

    cases = LegalCase.query.all()
    if not cases:
        return False

    # Combine all text fields into one document per case
    docs = []
    _case_index = []
    for c in cases:
        text = " ".join(filter(None, [
            c.title or "",
            c.act_name or "",
            c.section or "",
            (c.summary or "") * 2,          # weight summary 2×
            c.keywords or "",
            c.judgement_text or "",
        ]))
        docs.append(text.lower())
        _case_index.append(c.id)

    _tfidf_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        max_features=10000,
        sublinear_tf=True,
    )
    _tfidf_matrix = _tfidf_vectorizer.fit_transform(docs)
    return True


def reset_cache():
    """Call this when cases are inserted/deleted."""
    global _tfidf_vectorizer, _tfidf_matrix, _case_index
    _tfidf_vectorizer = None
    _tfidf_matrix = None
    _case_index = []


# ── Public API ────────────────────────────────────────────────────────────────

def find_similar_cases(
    query: str,
    year: str  = None,
    court: str = None,
    top_k: int = 10,
) -> Dict:
    """
    Hybrid search:
    1. TF-IDF cosine similarity over all cases (fast, accurate)
    2. Optional year / court post-filters
    3. Fallback to LIKE keyword search if query is very short
    """
    if not query or not query.strip():
        return {"success": False, "error": "Please enter a search query."}

    query = query.strip()

    # ── Build TF-IDF if needed ────────────────────────────────────────────
    global _tfidf_vectorizer, _tfidf_matrix, _case_index
    if _tfidf_vectorizer is None:
        if not _build_tfidf():
            return {"success": False, "error": "No case data available. Run the seed script first."}

    # ── Short query fallback (< 3 chars) ─────────────────────────────────
    if len(query) < 3:
        return _keyword_search(query, year, court, top_k)

    # ── TF-IDF similarity ─────────────────────────────────────────────────
    try:
        q_vec  = _tfidf_vectorizer.transform([query.lower()])
        scores = cosine_similarity(q_vec, _tfidf_matrix).flatten()

        # Get top-N indices sorted by score
        top_indices = scores.argsort()[::-1]

        # Retrieve and filter cases
        results = []
        for idx in top_indices:
            if scores[idx] < 0.01:          # skip near-zero matches
                break
            case_id = _case_index[idx]
            case    = LegalCase.query.get(case_id)
            if case is None:
                continue

            # Apply optional filters
            if year and year not in ("Any", ""):
                try:
                    if case.year != int(year):
                        continue
                except ValueError:
                    pass

            if court and court not in ("Any", ""):
                if court.lower() not in (case.court or "").lower():
                    continue

            d = case.to_dict()
            d["score"] = round(float(scores[idx]), 4)
            d["keywords"] = case.keywords or ""
            results.append(d)

            if len(results) >= top_k:
                break

        # Fallback if TF-IDF returned nothing
        if not results:
            return _keyword_search(query, year, court, top_k)

        return {"success": True, "count": len(results), "cases": results, "method": "tfidf"}

    except Exception as e:
        # Graceful fallback on TF-IDF errors
        return _keyword_search(query, year, court, top_k)


def _keyword_search(query: str, year, court, top_k: int) -> Dict:
    """Fallback LIKE-based keyword search."""
    q = LegalCase.query
    terms = query.split()[:3]
    for term in terms:
        q = q.filter(
            LegalCase.title.ilike(f"%{term}%")   |
            LegalCase.summary.ilike(f"%{term}%") |
            LegalCase.act_name.ilike(f"%{term}%")|
            LegalCase.keywords.ilike(f"%{term}%")
        )
    if year and year not in ("Any", ""):
        try:
            q = q.filter(LegalCase.year == int(year))
        except ValueError:
            pass
    if court and court not in ("Any", ""):
        q = q.filter(LegalCase.court.ilike(f"%{court}%"))

    cases = q.limit(top_k).all()
    results = []
    for c in cases:
        d = c.to_dict()
        d["score"] = 1.0
        d["keywords"] = c.keywords or ""
        results.append(d)

    return {"success": True, "count": len(results), "cases": results, "method": "keyword"}


# ── Filter Helpers ────────────────────────────────────────────────────────────

def get_all_courts() -> List[str]:
    rows = LegalCase.query.with_entities(LegalCase.court).distinct().all()
    return sorted([r[0] for r in rows if r[0]])


def get_year_range() -> Dict:
    from sqlalchemy import func
    result = LegalCase.query.with_entities(
        func.min(LegalCase.year),
        func.max(LegalCase.year)
    ).first()
    return {"min": result[0] or 1950, "max": result[1] or 2024}
