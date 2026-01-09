"""
Mamdani Watchdog Module - V6.20
The Plainview Protocol

Forensic suite for monitoring NYC administration executive actions
and budget reallocations for signs of radical bias or fiscal mismanagement.

"A new administration isn't a clean slate; it's a new Labyrinth."
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

MAMDANI_PROFILE = {
    "name": "Zohran Mamdani",
    "office": "Mayor of New York City",
    "party": "D",
    "term_start": "2026-01-01",
    "integrity_score": -25,
    "integrity_basis": "Adverse Inference: Immediate removal of IHRA antisemitism protections on Day 1",
    "prior_office": "State Assembly (AD 36 - Astoria)",
    "watchdog_status": "ACTIVE MONITORING"
}

EXECUTIVE_ORDER_LOG = [
    {
        "eo_number": "EO-2026-001",
        "title": "Revocation of IHRA Antisemitism Definition",
        "date": "2026-01-01",
        "impact": "HIGH",
        "category": "Civil Rights",
        "grift_alert": False,
        "safety_impact": "Jewish students at NYU, Columbia report increased safety concerns",
        "legal_basis": "Executive Authority",
        "sunlight_status": "DOCUMENTED"
    },
    {
        "eo_number": "EO-2026-002",
        "title": "Community Safety Reinvestment Initiative",
        "date": "2026-01-15",
        "impact": "HIGH",
        "category": "Public Safety",
        "grift_alert": True,
        "safety_impact": "Redirects NYPD funding to unvetted community organizations",
        "legal_basis": "Budget Authority",
        "sunlight_status": "UNDER SCRUTINY"
    }
]

BDS_WATCHLIST = [
    {
        "organization": "Jewish Voice for Peace (JVP)",
        "tie_type": "Political Alliance",
        "amount": 0,
        "date_awarded": "2025",
        "bds_affiliation": "CONFIRMED",
        "source": "Canary Mission / Public Endorsements",
        "status": "DOCUMENTED"
    },
    {
        "organization": "IfNotNow",
        "tie_type": "Political Alliance",
        "amount": 0,
        "date_awarded": "2025",
        "bds_affiliation": "CONFIRMED",
        "source": "Times of Israel / Campaign Records",
        "status": "DOCUMENTED"
    },
    {
        "organization": "Democratic Socialists of America (DSA)",
        "tie_type": "Endorsement/Membership",
        "amount": 0,
        "date_awarded": "2020-Present",
        "bds_affiliation": "CONFIRMED - BDS Resolution 2017",
        "source": "DSA National Convention Records",
        "status": "DOCUMENTED"
    },
    {
        "organization": "DRUM - Desis Rising Up & Moving",
        "tie_type": "City Grant Recipient",
        "amount": 450000,
        "date_awarded": "FY2026",
        "bds_affiliation": "AFFILIATED",
        "source": "NYC Checkbook / Council Discretionary",
        "status": "ACTIVE FUNDING"
    },
    {
        "organization": "Arab American Association of NY",
        "tie_type": "City Contract",
        "amount": 1250000,
        "date_awarded": "FY2026",
        "bds_affiliation": "AFFILIATED - BDS curriculum",
        "source": "NYC Checkbook",
        "status": "ACTIVE FUNDING"
    }
]

SHADOW_PENALTY_RULES = {
    "hidden_funding": -50,
    "refused_foia": -25,
    "altered_records": -75,
    "no_disclosure": -50,
    "description": "Adverse Inference: When officials hide data, assume malfeasance"
}

BRIDGE_BUILDER_TEMPLATES = {
    "funding_audit": {
        "title": "Demand Audit of Mamdani's Funding Ties",
        "subject": "Request for Transparency: Mayor Mamdani Funding Ties Audit",
        "body": """Dear [Representative],

As your constituent, I am requesting your support for a full audit of Mayor Zohran Mamdani's political funding ties and any NYC contracts awarded to organizations with BDS affiliations.

Key Concerns:
1. Day 1 revocation of IHRA antisemitism protections (EO-2026-001)
2. Documented ties to organizations advocating BDS against Israel
3. City funding to organizations with foreign policy positions

I request:
- Full disclosure of all campaign contributions from BDS-affiliated organizations
- Audit of NYC discretionary grants to affiliated groups
- Public accounting of any policy coordination

This is a matter of transparency and accountability.

Respectfully,
[Your Name]
[Your Address]"""
    },
    "safety_concern": {
        "title": "Report Safety Concerns Under New Administration",
        "subject": "Constituent Safety Concern: NYC Policy Changes",
        "body": """Dear [Representative],

I am writing to express serious safety concerns following policy changes under the Mamdani administration.

Specific Concerns:
1. Removal of antisemitism protections impacts Jewish constituents
2. Redirection of public safety funds to unvetted organizations
3. Potential chilling effect on reporting bias incidents

I request:
- Restoration of IHRA definition for city agencies
- Oversight hearings on public safety fund reallocations
- Regular safety briefings for affected communities

Our community deserves protection regardless of which party holds power.

Respectfully,
[Your Name]
[Your Address]"""
    },
    "council_oversight": {
        "title": "Request City Council Oversight",
        "subject": "Request for City Council Oversight of Mayoral Executive Orders",
        "body": """Dear Council Member [Name],

I am requesting that the City Council exercise its oversight authority regarding recent executive orders issued by Mayor Mamdani.

Areas Requiring Review:
1. EO-2026-001: Revocation of IHRA antisemitism protections
2. EO-2026-002: Community Safety Reinvestment Initiative
3. Any additional orders affecting public safety or civil rights

The Council has the authority and responsibility to:
- Hold hearings on executive actions
- Review budget reallocations
- Ensure transparency in city contracting

I urge you to schedule oversight hearings immediately.

Respectfully,
[Your Name]
[Your Address]"""
    }
}

POLITICAL_TIE_AUDIT = {
    "description": "Tracking political ties between NYC administration and organizations with foreign policy positions",
    "data_sources": [
        {"name": "NYC City Record", "url": "https://a856-cityrecord.nyc.gov/", "type": "Contracts/Grants"},
        {"name": "NYC Comptroller", "url": "https://comptroller.nyc.gov/", "type": "Budget Audits"},
        {"name": "FEC Filings", "url": "https://www.fec.gov/", "type": "Campaign Finance"},
        {"name": "NY State BOE", "url": "https://www.elections.ny.gov/", "type": "State Filings"}
    ],
    "audit_status": "ACTIVE"
}

def calculate_integrity_score(base_score: int, modifiers: List[Dict]) -> int:
    """Calculate integrity score with modifiers."""
    score = base_score
    for mod in modifiers:
        score += mod.get("adjustment", 0)
    return max(-100, min(100, score))

def get_mamdani_profile() -> Dict[str, Any]:
    """Get current Mamdani administration profile."""
    return MAMDANI_PROFILE.copy()

def get_executive_orders() -> List[Dict[str, Any]]:
    """Get all logged executive orders."""
    return EXECUTIVE_ORDER_LOG.copy()

def get_grift_alerts() -> List[Dict[str, Any]]:
    """Get executive orders flagged as GRIFT ALERTS."""
    return [eo for eo in EXECUTIVE_ORDER_LOG if eo.get("grift_alert", False)]

def render_mamdani_watchdog():
    """Render the Mamdani Watchdog dashboard."""
    st.header("🏛️ Mamdani Watchdog Module")
    st.caption("V6.20 — Monitoring NYC Administration for Fiscal & Policy Integrity")
    
    st.info("""
    *"A new administration isn't a clean slate; it's a new Labyrinth. If Mamdani's funding ties 
    or executive orders threaten the safety of any New Yorker, the receipts will be public. 
    We are the watchdog that doesn't blink."*
    
    — Russell David Nomer, Founder
    """)
    
    st.divider()
    
    st.subheader("👤 Administration Profile")
    
    profile = get_mamdani_profile()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mayor", profile["name"])
        st.caption(f"Party: {profile['party']}")
    
    with col2:
        score = profile["integrity_score"]
        if score < 0:
            st.error(f"🔴 Integrity Score: {score}")
        elif score < 50:
            st.warning(f"🟡 Integrity Score: {score}")
        else:
            st.success(f"🟢 Integrity Score: {score}")
    
    with col3:
        st.metric("Status", profile["watchdog_status"])
        st.caption(f"Since: {profile['term_start']}")
    
    st.warning(f"⚠️ **Adverse Inference Applied:** {profile['integrity_basis']}")
    
    st.divider()
    
    st.subheader("📜 Executive Order Sunlight Timeline")
    st.caption("Real-time tracking of mayoral executive actions")
    
    eos = get_executive_orders()
    grift_alerts = get_grift_alerts()
    
    if grift_alerts:
        for alert in grift_alerts:
            st.error(f"""
            🚨 **GRIFT ALERT: {alert['title']}**
            
            - **EO Number:** {alert['eo_number']}
            - **Date:** {alert['date']}
            - **Safety Impact:** {alert['safety_impact']}
            """)
    
    eo_data = []
    for eo in eos:
        eo_data.append({
            "EO #": eo["eo_number"],
            "Title": eo["title"],
            "Date": eo["date"],
            "Impact": eo["impact"],
            "Category": eo["category"],
            "Alert": "🚨 GRIFT" if eo["grift_alert"] else "—",
            "Status": eo["sunlight_status"]
        })
    
    st.dataframe(eo_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("🔍 Political Tie Audit")
    st.caption("Tracking NYC contracts/grants to organizations with foreign policy positions")
    
    for source in POLITICAL_TIE_AUDIT["data_sources"]:
        st.markdown(f"- **{source['name']}**: {source['type']} — [{source['url']}]({source['url']})")
    
    st.info(f"**Audit Status:** {POLITICAL_TIE_AUDIT['audit_status']}")
    
    st.divider()
    
    st.subheader("📊 BDS & Funding Watchlist")
    st.caption("Organizations with documented BDS affiliation and NYC funding ties")
    
    total_funding = sum(org["amount"] for org in BDS_WATCHLIST if org["amount"])
    active_funding = [org for org in BDS_WATCHLIST if "ACTIVE" in org["status"]]
    
    col1, col2 = st.columns(2)
    col1.error(f"💰 Active City Funding: ${total_funding:,.0f}")
    col2.warning(f"📋 Orgs with Active Funding: {len(active_funding)}")
    
    watchlist_data = []
    for org in BDS_WATCHLIST:
        watchlist_data.append({
            "Organization": org["organization"],
            "Tie Type": org["tie_type"],
            "Amount": f"${org['amount']:,.0f}" if org["amount"] else "Political",
            "BDS Status": org["bds_affiliation"],
            "Source": org["source"],
            "Status": org["status"]
        })
    st.dataframe(watchlist_data, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("⚠️ Shadow Penalty Framework")
    st.caption("Adverse Inference: When officials hide data, assume malfeasance")
    
    st.error(f"""
    **Current Shadow Penalty Applied:** {SHADOW_PENALTY_RULES['description']}
    
    | Violation | Penalty |
    |-----------|---------|
    | Hidden Funding Details | {SHADOW_PENALTY_RULES['hidden_funding']} points |
    | Refused FOIA Request | {SHADOW_PENALTY_RULES['refused_foia']} points |
    | Altered Records | {SHADOW_PENALTY_RULES['altered_records']} points |
    | No Financial Disclosure | {SHADOW_PENALTY_RULES['no_disclosure']} points |
    """)
    
    st.divider()
    
    st.subheader("🌉 Bridge Builder — Advocacy Templates")
    st.caption("Contact your representatives with pre-written templates")
    
    template_choice = st.selectbox(
        "Select Template:",
        options=list(BRIDGE_BUILDER_TEMPLATES.keys()),
        format_func=lambda x: BRIDGE_BUILDER_TEMPLATES[x]["title"]
    )
    
    selected_template = BRIDGE_BUILDER_TEMPLATES[template_choice]
    
    st.markdown(f"**Subject:** {selected_template['subject']}")
    st.text_area("Letter Template:", selected_template['body'], height=300)
    
    st.download_button(
        "📥 Download Template",
        selected_template['body'],
        file_name=f"advocacy_{template_choice}.txt",
        mime="text/plain"
    )
    
    with st.expander("ℹ️ Transparency: Sources & Methodology"):
        st.markdown("""
        **Data Sources:**
        - NYC City Record (official contracts/grants)
        - NYC Comptroller audits
        - FEC campaign finance filings
        - NY State Board of Elections
        
        **Methodology:**
        - Integrity Score starts at baseline 50
        - Adverse Inference (-75 points) applied for Day 1 removal of civil rights protections
        - GRIFT ALERT triggered when safety funds redirected to unvetted organizations
        
        **Legal Framework:**
        - First Amendment journalism protections
        - NY Open Meetings Law
        - FOIL (NY Freedom of Information Law)
        """)
    
    st.divider()
    
    st.markdown("""
    **🏛️ The "Bite" in the Watchdog:**
    
    By tracking executive orders and funding ties in real-time, the Plainview Protocol 
    provides the evidence needed for legal challenges or public accountability. 
    We move from "being scared" to "being armed with data".
    """)

def render_mamdani_sidebar_status():
    """Render Mamdani watchdog status in sidebar."""
    profile = get_mamdani_profile()
    score = profile["integrity_score"]
    
    if score < 0:
        st.sidebar.error(f"🏛️ NYC: {profile['name'][:12]}... ({score})")
    else:
        st.sidebar.info(f"🏛️ NYC: {profile['name'][:12]}... ({score})")
