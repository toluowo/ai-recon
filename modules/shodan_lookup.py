import os
import shodan

def shodan_lookup(domain):
    """
    Shodan search with hybrid behavior:
    - If SHODAN_API_KEY exists, try real search via hostname filter.
    - If it fails or no key, return mock data.
    Returns dict; includes {"mock": True} in mock mode.
    """
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        return {
            "hostnames": [domain],
            "ports": [80, 443],
            "org": "Mock ISP Ltd",
            "country": "NG",
            "vulnerabilities": [],
            "data": [{"banner": "Apache/2.4.54 OpenSSL/1.1.1"}],
            "mock": True
        }

    try:
        api = shodan.Shodan(api_key)
        # Search by hostname (handles domains without resolving IP first)
        q = f"hostname:{domain}"
        results = api.search(q, limit=100)

        ports = set()
        vulns = set()
        banners = []
        org = None
        country = None
        hostnames = set()

        for m in results.get("matches", []):
            if isinstance(m.get("port"), int):
                ports.add(m["port"])
            hostnames.update(m.get("hostnames") or [])
            org = org or m.get("org")
            country = country or m.get("location", {}).get("country_code")
            # collect vulnerabilities if present
            v = m.get("vulns") or {}
            for k in v.keys():
                vulns.add(k)
            # banner text
            btxt = m.get("data")
            if btxt:
                banners.append({"banner": btxt[:500]})

        return {
            "hostnames": sorted(hostnames) or [domain],
            "ports": sorted(ports),
            "org": org,
            "country": country,
            "vulnerabilities": sorted(vulns),
            "data": banners,
            "mock": False
        }
    except Exception as e:
        return {
            "hostnames": [domain],
            "ports": [80, 443],
            "org": None,
            "country": None,
            "vulnerabilities": [],
            "data": [{"banner": f"[MOCK DUE TO ERROR] {str(e)[:200]}"}],
            "mock": True,
            "error": True
        }
