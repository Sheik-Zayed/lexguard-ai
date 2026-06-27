"""
LexGuard AI — RAG Legal Advisor Service
Pipeline:
  1. Accept user legal query
  2. Retrieve top-3 relevant IPC sections via TF-IDF (from ipc_sections_full.json)
  3. Send retrieved sections as context to Gemini (or OpenAI) for structured answer
  4. Fallback to TF-IDF-only structured response if no API key configured
"""
import json
from flask import current_app


# ─── Main Entry Point ────────────────────────────────────────────────────────

def get_legal_advice(question: str) -> dict:
    """
    Full RAG pipeline — retrieval + generation.
    Returns a structured dict with keys:
        query, sections, llm_answer, source ('gemini' | 'openai' | 'tfidf')
    """
    # Step 1: Retrieve relevant IPC sections
    retriever = current_app.ipc_retriever
    top_sections = retriever.search(question, top_k=3)

    if not top_sections:
        return _empty_response(question)

    # Step 2: Try Gemini
    gemini_key = current_app.config.get("GEMINI_API_KEY", "")
    if gemini_key and gemini_key not in ("", "your_gemini_api_key_here"):
        result = _call_gemini(question, top_sections, gemini_key)
        if result:
            return {
                "query": question,
                "sections": top_sections,
                "llm_answer": result,
                "source": "gemini",
            }

    # Step 3: Try OpenAI
    openai_key = current_app.config.get("OPENAI_API_KEY", "")
    if openai_key and openai_key not in ("", "your_openai_api_key_here"):
        result = _call_openai(question, top_sections, openai_key)
        if result:
            return {
                "query": question,
                "sections": top_sections,
                "llm_answer": result,
                "source": "openai",
            }

    # Step 4: TF-IDF fallback — build structured answer from retrieved sections
    return {
        "query": question,
        "sections": top_sections,
        "llm_answer": _tfidf_fallback_answer(question, top_sections),
        "source": "tfidf",
    }


# ─── Gemini Integration ───────────────────────────────────────────────────────

def _call_gemini(question: str, sections: list, api_key: str) -> dict | None:
    """Call Google Gemini API with retrieved IPC context. Skips on quota/auth errors."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = _build_prompt(question, sections)
        response = model.generate_content(prompt)
        raw = response.text.strip()
        return _parse_llm_response(raw)
    except Exception as e:
        err_str = str(e)
        # On quota / auth errors skip immediately — don't retry or wait
        if any(k in err_str for k in ("429", "quota", "RESOURCE_EXHAUSTED", "API_KEY", "401", "403")):
            print(f"[LexGuard] Gemini skipped (quota/auth): {err_str[:120]}")
        else:
            print(f"[LexGuard] Gemini error: {err_str[:200]}")
        return None


# ─── OpenAI Integration ───────────────────────────────────────────────────────

def _call_openai(question: str, sections: list, api_key: str) -> dict | None:
    """Call OpenAI API with retrieved IPC context."""
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        prompt = _build_prompt(question, sections)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert Indian legal advisor. Always answer based on the provided IPC sections and structure your response exactly as instructed."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1200,
        )
        raw = response.choices[0].message.content.strip()
        return _parse_llm_response(raw)
    except Exception as e:
        print(f"[LexGuard] OpenAI error: {e}")
        return None


# ─── Prompt Builder ───────────────────────────────────────────────────────────

def _build_prompt(question: str, sections: list) -> str:
    """Build a structured RAG prompt with retrieved IPC sections as context."""
    context_parts = []
    for i, s in enumerate(sections, 1):
        context_parts.append(
            f"[Section {i}]\n"
            f"IPC Section: {s.get('section', 'N/A')}\n"
            f"Title: {s.get('title', 'N/A')}\n"
            f"Description: {s.get('description', 'N/A')}\n"
            f"Punishment: {s.get('punishment', 'N/A')}"
        )
    context = "\n\n".join(context_parts)

    return f"""You are an expert Indian legal advisor with deep knowledge of the Indian Penal Code.

A user has asked the following legal question:
\"{question}\"

Based on these retrieved IPC sections, provide a structured legal answer:

{context}

Respond ONLY in the following JSON format (no markdown, no extra text):
{{
  "primary_section": "IPC XXX",
  "primary_title": "Section title",
  "plain_meaning": "Explain in simple English what the law says and how it applies to this question (2-4 sentences)",
  "punishment": "Describe the punishment for this offence clearly",
  "practical_advice": "Give 3-4 actionable steps the person should take (numbered list)",
  "related_sections": ["IPC XXX", "IPC YYY"],
  "disclaimer": "This is general legal information only. Consult a licensed advocate for advice specific to your situation."
}}"""


# ─── LLM Response Parser ──────────────────────────────────────────────────────

def _parse_llm_response(raw: str) -> dict | None:
    """Parse the LLM's JSON response, stripping markdown if present."""
    try:
        # Remove markdown code fences if present
        text = raw.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        return json.loads(text)
    except Exception:
        # Return raw text as plain_meaning if JSON parsing fails
        return {
            "primary_section": "Multiple IPC Sections Apply",
            "primary_title": "See retrieved sections",
            "plain_meaning": raw,
            "punishment": "See relevant sections above",
            "practical_advice": "1. Consult a licensed advocate.\n2. File a police complaint if applicable.\n3. Collect and preserve evidence.",
            "related_sections": [],
            "disclaimer": "This is general legal information only. Consult a licensed advocate for advice specific to your situation.",
        }


# ─── TF-IDF Fallback ─────────────────────────────────────────────────────────

def _tfidf_fallback_answer(question: str, sections: list) -> dict:
    """Build a structured response from TF-IDF retrieval alone (no LLM)."""
    if not sections:
        return _empty_response(question)["llm_answer"]

    primary = sections[0]
    related = [s.get("section", "") for s in sections[1:]]

    return {
        "primary_section": primary.get("section", "N/A"),
        "primary_title": primary.get("title", "N/A"),
        "plain_meaning": primary.get("description", "No description available."),
        "punishment": primary.get("punishment", "Refer to the relevant IPC section."),
        "practical_advice": (
            "1. Document all evidence related to your situation.\n"
            "2. File a First Information Report (FIR) at your nearest police station if a cognizable offence has occurred.\n"
            "3. Consult a licensed advocate who specialises in criminal law.\n"
            "4. If in immediate danger, contact emergency services (112)."
        ),
        "related_sections": related,
        "disclaimer": "This is AI-generated legal information based on IPC text. No LLM API key is configured. For accurate legal advice, consult a licensed advocate.",
    }


def _empty_response(question: str) -> dict:
    return {
        "query": question,
        "sections": [],
        "llm_answer": {
            "primary_section": "N/A",
            "primary_title": "No relevant section found",
            "plain_meaning": "We could not find a relevant IPC section for your query. Please try rephrasing or consult a lawyer directly.",
            "punishment": "N/A",
            "practical_advice": "1. Consult a licensed advocate directly.\n2. Contact Legal Aid Services in your district.\n3. Call the National Legal Services Authority helpline: 15100.",
            "related_sections": [],
            "disclaimer": "This is general legal information only.",
        },
        "source": "none",
    }
