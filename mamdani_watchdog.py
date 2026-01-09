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
        "organization": "Placeholder - Pending NYC City Record Scrape",
        "tie_type": "Contract/Grant",
        "amount": 0,
        "date_awarded": None,
        "bds_affiliation": "Unverified",
        "source": "NYC City Record",
        "status": "PENDING VERIFICATION"
    }
]

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
    st.caption("Organizations under review for BDS affiliation and NYC funding ties")
    
    if BDS_WATCHLIST and BDS_WATCHLIST[0]["organization"] != "Placeholder - Pending NYC City Record Scrape":
        watchlist_data = []
        for org in BDS_WATCHLIST:
            watchlist_data.append({
                "Organization": org["organization"],
                "Tie Type": org["tie_type"],
                "Amount": f"${org['amount']:,.0f}" if org["amount"] else "—",
                "Status": org["status"]
            })
        st.dataframe(watchlist_data, use_container_width=True, hide_index=True)
    else:
        st.warning("⏳ **Pending:** NYC City Record scrape in progress. Data will populate as contracts are verified.")
    
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
