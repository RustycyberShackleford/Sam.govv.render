from datetime import datetime, timedelta

def demo_opportunities_by_naics(naics: str):
    code = (naics or "").strip()
    if not code or not code.isdigit():
        return []
    today = datetime.utcnow().date()
    return [
        {
            "solicitation": f"NAVY-{code}-R-001",
            "title": f"Services under NAICS {code} - Customer Engagement Platform",
            "agency": "Department of the Navy",
            "response_due": (today + timedelta(days=14)).isoformat(),
            "set_aside": "Total Small Business",
            "naics": code,
            "psc": "D399",
            "status": "Open"
        },
        {
            "solicitation": f"USAF-{code}-R-014",
            "title": f"Enterprise Integration and Data Orchestration ({code})",
            "agency": "Department of the Air Force",
            "response_due": (today + timedelta(days=21)).isoformat(),
            "set_aside": "None",
            "naics": code,
            "psc": "D304",
            "status": "Open"
        },
        {
            "solicitation": f"GSA-{code}-R-207",
            "title": f"CRM/Power Platform Support ({code})",
            "agency": "General Services Administration",
            "response_due": (today + timedelta(days=28)).isoformat(),
            "set_aside": "8(a)",
            "naics": code,
            "psc": "R499",
            "status": "Open"
        },
    ]
