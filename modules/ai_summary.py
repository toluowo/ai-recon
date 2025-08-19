import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _try_openai(prompt: str) -> str:
    """
    Use OpenAI if key exists. Return text or raise on error.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("No OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise cybersecurity analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return (resp.choices[0].message.content or "").strip()

def generate_summary(context: dict, whois_data: dict, shodan_data: dict) -> str:
    """
    Summarize recon data. Falls back to mock text if OpenAI unavailable.
    """
    prompt = (
        "Summarize these authorized recon findings for a security report. "
        "Be concise, highlight likely risks, and suggest next steps.\n\n"
        f"Context: {context}\n\nWHOIS: {whois_data}\n\nSHODAN: {shodan_data}\n"
    )
    try:
        return _try_openai(prompt)
    except Exception as e:
        return f"[MOCK SUMMARY] Concise findings listed. (AI unavailable: {str(e)})"

def generate_pretext(context: dict) -> str:
    """
    Generate a benign training pretext outline for authorized exercises.
    Falls back to mock text if OpenAI unavailable.
    """
    prompt = (
        "Create a short, benign and lawful social-engineering training pretext outline "
        "for authorized internal testing. Do NOT include harmful instructions or PII.\n\n"
        f"Context: {context}\n"
        "Output sections: Objective, Persona, Channels, Guardrails, Example Dialogue (brief)."
    )
    try:
        return _try_openai(prompt)
    except Exception as e:
        return (
            "[MOCK PRETEXT] Objective: verify employee reporting paths.\n"
            "Persona: IT support auditor.\nChannels: email + ticketing.\n"
            "Guardrails: no credentials requested; include reporting instructions.\n"
            f"(AI unavailable: {str(e)})"
        )
