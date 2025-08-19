import whois

def _to_str(x):
    # normalize types for JSON/report
    if isinstance(x, (list, set, tuple)):
        return [str(i) for i in x]
    return str(x)

def whois_lookup(domain):
    """
    WHOIS lookup with offline-safe fallback.
    Returns a dict; includes {"mock": True} when mocked.
    """
    try:
        w = whois.whois(domain)
        return {
            "domain_name": _to_str(w.domain_name) if w.domain_name else domain,
            "registrar": _to_str(w.registrar) if w.registrar else None,
            "creation_date": _to_str(w.creation_date) if w.creation_date else None,
            "expiration_date": _to_str(w.expiration_date) if w.expiration_date else None,
            "name_servers": list(w.name_servers) if w.name_servers else [],
            "emails": _to_str(w.emails) if w.emails else None,
            "org": _to_str(getattr(w, "org", None)) if getattr(w, "org", None) else None,
            "country": _to_str(getattr(w, "country", None)) if getattr(w, "country", None) else None,
            "mock": False
        }
    except Exception:
        # Offline/mock
        return {
            "domain_name": domain,
            "registrar": "Mock Registrar Ltd",
            "creation_date": "2020-01-15",
            "expiration_date": "2026-01-15",
            "name_servers": ["ns1.mockdns.net", "ns2.mockdns.net"],
            "emails": [f"admin@{domain}"],
            "org": "Mock Organization",
            "country": "NG",
            "mock": True
        }
