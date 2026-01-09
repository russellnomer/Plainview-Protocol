"""
Local Agenda Scanner for The Plainview Protocol V8.4

Scans local government meeting agendas for grift keywords,
calculates transparency scores, and allows user flagging.
"""

import hashlib
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re

try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

GRIFT_KEYWORDS = {
    "no-bid": {"weight": 15, "severity": "HIGH", "description": "No competitive bidding"},
    "sole source": {"weight": 15, "severity": "HIGH", "description": "Single vendor selection"},
    "emergency contract": {"weight": 12, "severity": "HIGH", "description": "Bypassed normal procurement"},
    "fee increase": {"weight": 8, "severity": "MEDIUM", "description": "Cost passed to taxpayers"},
    "tax increase": {"weight": 8, "severity": "MEDIUM", "description": "Revenue extraction"},
    "executive session": {"weight": 10, "severity": "MEDIUM", "description": "Closed-door meeting"},
    "confidential": {"weight": 7, "severity": "MEDIUM", "description": "Hidden from public"},
    "consultant": {"weight": 5, "severity": "LOW", "description": "Outside contractor"},
    "amendment": {"weight": 3, "severity": "LOW", "description": "Contract modification"},
    "change order": {"weight": 10, "severity": "HIGH", "description": "Cost overrun indicator"},
    "waiver": {"weight": 8, "severity": "MEDIUM", "description": "Rule exception"},
    "settlement": {"weight": 12, "severity": "HIGH", "description": "Legal payout"},
}

MOCK_AGENDAS = {
    "Nassau County": [
        {
            "id": "NC-2026-001",
            "meeting_date": "2026-01-15",
            "meeting_type": "County Legislature",
            "items": [
                {"id": "NC-2026-001-A", "title": "Resolution for Emergency Contract - Snow Removal Services", "text": "RESOLVED, that the County Executive is authorized to enter into an emergency contract with ABC Plowing LLC for snow removal services, waiving competitive bidding requirements due to severe weather conditions."},
                {"id": "NC-2026-001-B", "title": "Fee Increase - Parks Department", "text": "RESOLVED, that the fee schedule for Nassau County Parks be amended to reflect a 15% fee increase effective March 1, 2026."},
                {"id": "NC-2026-001-C", "title": "Consultant Contract - IT Services", "text": "RESOLVED, that the County enter into a sole source contract with TechGiant Consulting for IT modernization services in the amount of $2.4 million."},
                {"id": "NC-2026-001-D", "title": "Executive Session - Personnel Matters", "text": "Motion to enter executive session to discuss personnel matters regarding the Department of Public Works."},
            ]
        },
        {
            "id": "NC-2026-002",
            "meeting_date": "2026-01-22",
            "meeting_type": "County Legislature",
            "items": [
                {"id": "NC-2026-002-A", "title": "Budget Amendment - Highway Department", "text": "RESOLVED, that the 2026 Operating Budget be amended to include a change order for the Northern State Parkway resurfacing project in the amount of $1.8 million."},
                {"id": "NC-2026-002-B", "title": "Settlement Agreement - Jones v. Nassau County", "text": "RESOLVED, that the County Attorney is authorized to execute a settlement agreement in the matter of Jones v. Nassau County in the amount of $450,000."},
            ]
        }
    ],
    "Oyster Bay Town": [
        {
            "id": "OB-2026-001",
            "meeting_date": "2026-01-14",
            "meeting_type": "Town Board",
            "items": [
                {"id": "OB-2026-001-A", "title": "No-Bid Contract - Sanitation Services", "text": "RESOLVED, that the Town enter into a no-bid contract with CleanSweep Inc. for supplemental sanitation services for a period of 3 years."},
                {"id": "OB-2026-001-B", "title": "Tax Rate Resolution", "text": "RESOLVED, that the general tax increase for fiscal year 2026-2027 be set at 2.9%, within the state tax cap."},
                {"id": "OB-2026-001-C", "title": "Park Improvement Grant", "text": "RESOLVED, that the Town accept a $150,000 state grant for improvements to Syosset-Woodbury Community Park."},
            ]
        }
    ],
    "Hempstead Town": [
        {
            "id": "HT-2026-001",
            "meeting_date": "2026-01-16",
            "meeting_type": "Town Board",
            "items": [
                {"id": "HT-2026-001-A", "title": "Consultant Services - Economic Development", "text": "RESOLVED, that the Town retain the services of GrowthPartners LLC as a consultant for economic development initiatives at a rate of $250/hour."},
                {"id": "HT-2026-001-B", "title": "Waiver Request - Building Permits", "text": "RESOLVED, that the normal 30-day review period be waived for the Roosevelt Field expansion project."},
                {"id": "HT-2026-001-C", "title": "Contract Amendment - Road Paving", "text": "RESOLVED, that the contract with Asphalt Kings Inc. be amended to include additional streets, increasing the contract value by $890,000."},
            ]
        }
    ],
    "Suffolk County": [
        {
            "id": "SC-2026-001",
            "meeting_date": "2026-01-17",
            "meeting_type": "County Legislature",
            "items": [
                {"id": "SC-2026-001-A", "title": "Emergency Declaration - Opioid Crisis", "text": "RESOLVED, that the County Executive is authorized to enter into emergency contracts with treatment facilities to address the ongoing opioid crisis."},
                {"id": "SC-2026-001-B", "title": "Sole Source Software Purchase", "text": "RESOLVED, that the County purchase a sole source license for CrimePredictAI software at a cost of $1.2 million annually."},
            ]
        }
    ]
}


def scan_agenda_item(text: str) -> List[Dict]:
    """Scan agenda text for grift keywords and return matches."""
    findings = []
    text_lower = text.lower()
    
    for keyword, info in GRIFT_KEYWORDS.items():
        keyword_lower = keyword.lower()
        keyword_nohyphen = keyword_lower.replace('-', ' ')
        keyword_nospace = keyword_lower.replace('-', '').replace(' ', '')
        
        found = False
        if keyword_lower in text_lower:
            found = True
        elif keyword_nohyphen in text_lower:
            found = True
        elif keyword_nospace in text_lower:
            found = True
        
        if found:
            findings.append({
                "keyword": keyword,
                "weight": info["weight"],
                "severity": info["severity"],
                "description": info["description"]
            })
    
    return findings


def calculate_transparency_score(agenda_items: List[Dict]) -> Tuple[int, List[Dict]]:
    """Calculate transparency score (0-100) based on flagged items."""
    base_score = 100
    total_deductions = 0
    all_findings = []
    
    for item in agenda_items:
        findings = scan_agenda_item(item.get("text", "") + " " + item.get("title", ""))
        if findings:
            item_deduction = sum(f["weight"] for f in findings)
            total_deductions += item_deduction
            all_findings.append({
                "item_id": item.get("id"),
                "item_title": item.get("title"),
                "findings": findings,
                "deduction": item_deduction
            })
    
    final_score = max(0, base_score - total_deductions)
    return final_score, all_findings


def get_transparency_rating(score: int) -> Tuple[str, str]:
    """Get rating label and color based on score."""
    if score >= 80:
        return "TRANSPARENT", "🟢"
    elif score >= 60:
        return "MOSTLY CLEAR", "🟡"
    elif score >= 40:
        return "OPACITY WARNING", "🟠"
    else:
        return "SHADOW ZONE", "🔴"


def get_jurisdictions() -> List[str]:
    """Get list of available jurisdictions."""
    return list(MOCK_AGENDAS.keys())


def get_agendas(jurisdiction: str) -> List[Dict]:
    """Get agendas for a jurisdiction."""
    return MOCK_AGENDAS.get(jurisdiction, [])


def init_agenda_flags_table():
    """Initialize the agenda_flags table in PostgreSQL."""
    if not PSYCOPG2_AVAILABLE:
        return False
    
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agenda_flags (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(64),
                jurisdiction VARCHAR(100),
                agenda_id VARCHAR(50),
                item_id VARCHAR(50),
                item_title TEXT,
                keyword VARCHAR(50),
                user_notes TEXT,
                flag_type VARCHAR(20) DEFAULT 'suspicious',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def save_agenda_flag(session_id: str, jurisdiction: str, agenda_id: str, 
                     item_id: str, item_title: str, keyword: str, 
                     user_notes: str = "", flag_type: str = "suspicious") -> bool:
    """Save a user flag to the database."""
    if not PSYCOPG2_AVAILABLE:
        return False
    
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO agenda_flags 
            (session_id, jurisdiction, agenda_id, item_id, item_title, keyword, user_notes, flag_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (session_id, jurisdiction, agenda_id, item_id, item_title, keyword, user_notes, flag_type))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def get_flag_count(jurisdiction: str = None) -> int:
    """Get count of flags for a jurisdiction or all."""
    if not PSYCOPG2_AVAILABLE:
        return 0
    
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return 0
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        if jurisdiction:
            cursor.execute("SELECT COUNT(*) FROM agenda_flags WHERE jurisdiction = %s", (jurisdiction,))
        else:
            cursor.execute("SELECT COUNT(*) FROM agenda_flags")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count
    except Exception:
        return 0
