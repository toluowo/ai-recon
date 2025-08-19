## `recon_ai.py`

#!/usr/bin/env python3
import os
import json
import argparse
import textwrap
from colorama import Fore, Style, init as colorama_init
from tabulate import tabulate
from dotenv import load_dotenv

# Load env early
load_dotenv()
colorama_init(autoreset=True)

# Local modules
from modules.whois_lookup import whois_lookup
from modules.shodan_lookup import shodan_lookup
from modules.ai_summary import generate_summary, generate_pretext
from modules.risk_scoring import LiveRiskScorer

# ---------- helpers ----------
def safe_dump(obj) -> str:
    try:
        return json.dumps(obj, default=str, indent=2)
    except Exception:
        try:
            return str(obj)
        except Exception:
            return "<unserializable>"

def extract_whois_findings(whois_data):
    findings = []
    try:
        d = whois_data if isinstance(whois_data, dict) else (getattr(whois_data, "__dict__", {}) or {})
        registrar = str(d.get("registrar", "")).lower()
        ns = [str(s).lower() for s in (d.get("name_servers") or [])]
        country = str(d.get("country", "")).upper()
        created = str(d.get("creation_date", ""))

        if registrar and "privacy" in registrar:
            findings.append({"factor": "WHOIS privacy protection enabled", "severity": "medium"})
        if ns and any(n.startswith("ns1.") for n in ns):
            findings.append({"factor": "Single-provider DNS footprint", "severity": "low"})
        if created and created < "2015-01-01":
            findings.append({"factor": "Old domain registration date", "severity": "low"})
        if country and country not in ["US","UK","CA","AU","DE","FR","NL","SE","NO"]:
            findings.append({"factor": f"Registration country: {country}", "severity": "medium"})
    except Exception:
        findings.append({"factor": "WHOIS parse failure", "severity": "low"})
    return findings

def extract_shodan_findings(shodan_data):
    findings = []
    if not isinstance(shodan_data, dict):
        findings.append({"factor": "Shodan: non-dict response", "severity": "low"})
        return findings

    if shodan_data.get("error"):
        findings.append({"factor": "Shodan API error", "severity": "low"})
        return findings

    ports = shodan_data.get("ports") or []
    if ports:
        if any(p in (22, 23, 3389, 5900) for p in ports):
            findings.append({"factor": f"Exposed remote access port(s): {ports}", "severity": "high"})
        elif len(ports) > 5:
            findings.append({"factor": f"Many open ports ({len(ports)})", "severity": "medium"})
        else:
            findings.append({"factor": f"Open ports: {ports}", "severity": "low"})

    vulns = shodan_data.get("vulnerabilities") or []
    if isinstance(vulns, dict):
        vulns = list(vulns.keys())
    if vulns:
        findings.append({"factor": f"{len(vulns)} known vulnerabilities from banners", "severity": "critical"})

    banners = shodan_data.get("data") or []
    tech_hits = 0
    for item in banners:
        banner = (item.get("banner") or "").lower()
        if any(x in banner for x in ["apache/2.2", "openssl/1.0.", "php/5.", "ms-sql", "ftp"]):
            tech_hits += 1
    if tech_hits:
        findings.append({"factor": f"Outdated/legacy service banners ({tech_hits})", "severity": "medium"})

    if shodan_data.get("mock"):
        findings.append({"factor": "[MOCK] Shodan data (offline mode)", "severity": "low"})
    return findings

# ---------- main ----------
def main():
    parser = argparse.ArgumentParser(description="AI-Driven Recon (Hybrid: Mock + Real)")
    parser.add_argument("--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("--company", help="Company name for pretext (optional)")
    parser.add_argument("--summary", action="store_true", help="Generate AI (or mock) summary")
    parser.add_argument("--score", action="store_true", help="Calculate risk score with live updates")
    parser.add_argument("--pretext", action="store_true", help="Generate pretext (AI or mock)")
    parser.add_argument("--output", default="reports/recon_report.md", help="Path to save the Markdown report")
    parser.add_argument("--no-ansi", action="store_true", help="Disable colors/animation")
    args = parser.parse_args()

    # configure risk engine ANSI
    from modules.risk_scoring import set_ansi_enabled
    set_ansi_enabled(not args.no_ansi)

    domain = args.domain
    company = args.company or "Target Org"

    print(Fore.CYAN + f"[+] Starting recon for {domain}")

    # Live risk engine
    scorer = LiveRiskScorer()

    # WHOIS
    whois_data = whois_lookup(domain)
    print(Fore.YELLOW + ("[*] WHOIS Data Retrieved " + ("[LIVE]" if not whois_data.get("mock") else "[MOCK]")))
    whois_findings = extract_whois_findings(whois_data)
    if args.score:
        scorer.add_many(whois_findings)

    # Shodan
    shodan_data = shodan_lookup(domain)
    print(Fore.YELLOW + ("[*] Shodan Data Retrieved " + ("[LIVE]" if isinstance(shodan_data, dict) and not shodan_data.get("mock") else "[MOCK]")))
    shodan_findings = extract_shodan_findings(shodan_data)
    if args.score:
        scorer.add_many(shodan_findings)

    # Pretty CLI table (quick overview)
    overview = [
        ["Domain", whois_data.get("domain_name", "N/A")],
        ["Registrar", whois_data.get("registrar", "N/A")],
        ["Creation Date", whois_data.get("creation_date", "N/A")],
        ["Expiration Date", whois_data.get("expiration_date", "N/A")],
        ["Name Servers", ", ".join(whois_data.get("name_servers", [])) if isinstance(whois_data.get("name_servers"), list) else whois_data.get("name_servers", "N/A")],
        ["Org/WHOIS Country", f"{whois_data.get('org','N/A')} / {whois_data.get('country','N/A')}"],
        ["Shodan Ports", ", ".join(map(str, (shodan_data.get('ports') or []))) if isinstance(shodan_data, dict) else "N/A"]
    ]
    print(Style.BRIGHT + tabulate(overview, headers=["Field", "Value"], tablefmt="grid"))

    # AI Summary / Pretext
    recon_ctx = {"domain": domain}
    ai_summary = generate_summary(recon_ctx, whois_data, shodan_data) if args.summary else "Summary not requested."
    pretext = generate_pretext({"domain": domain, "org": company}) if args.pretext else "Pretext not requested."

    # Finalize risk
    if args.score:
        final_result = scorer.finalize()
        print("\n=== RISK SCORING REPORT ===")
        print(scorer.render_table())
    else:
        final_result = {"risk_score": 0, "factors": ["Scoring not requested."]}

    # Write report
    os.makedirs("reports", exist_ok=True)
    with open(args.output, "w") as f:
        f.write(f"# AI Recon Report for {domain}\n\n")
        f.write("## Recon Data\n\n")
        f.write("### WHOIS DATA\n")
        f.write(safe_dump(whois_data) + "\n\n")
        f.write("### SHODAN DATA\n")
        f.write(safe_dump(shodan_data) + "\n\n")
        f.write("## AI Summary\n")
        f.write((ai_summary or "").strip() + "\n\n")
        f.write("## Pretext (Social Engineering)\n")
        f.write((pretext or "").strip() + "\n\n")
        f.write("## Risk Score\n")
        f.write(f"Score: {final_result['risk_score']}\n")
        f.write("Factors:\n")
        for t in final_result["factors"]:
            f.write(f"- {t}\n")

    print(Fore.GREEN + f"[+] Recon complete. Report saved to {args.output}")

if __name__ == "__main__":
    main()
