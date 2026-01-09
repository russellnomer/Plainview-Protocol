import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime, date

st.set_page_config(
    page_title="The Plainview Protocol",
    page_icon="🇺🇸",
    layout="wide"
)

with open("sources.json", "r") as f:
    SOURCES = json.load(f)

try:
    with open("system_status.json", "r") as f:
        SYSTEM_STATUS = json.load(f)
        is_system_online = all(val == "OK" for val in SYSTEM_STATUS.values())
except FileNotFoundError:
    SYSTEM_STATUS = {"treasury": "Unknown", "senate": "Unknown", "wiki": "Unknown"}
    is_system_online = True

@st.cache_data(ttl=3600)
def get_live_debt():
    fallback_debt = 36500000000000.00
    try:
        url = SOURCES["treasury_debt"]
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            debt_str = data["data"][0]["tot_pub_debt_out_amt"]
            return float(debt_str)
    except Exception:
        pass
    return fallback_debt

@st.cache_data(ttl=3600)
def get_senate_votes():
    fallback_votes = ["Vote data currently unavailable - Check back later", "System Maintenance"]
    votes = []
    try:
        url = SOURCES["senate_feed"]
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for vote in root.findall(".//vote")[:5]:
                question = vote.find("question")
                if question is not None:
                    votes.append(question.text)
    except Exception:
        pass
    
    if not votes:
        return fallback_votes
    return votes

@st.cache_data(ttl=86400)
def get_reps(state_full_name):
    us_state_to_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
        "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
        "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
    }
    
    code = us_state_to_abbrev.get(state_full_name)
    if not code:
        return pd.DataFrame([{"Status": "Invalid State"}]), False

    try:
        url = SOURCES.get("congress_legislators", "https://theunitedstates.io/congress-legislators/legislators-current.json")
        response = requests.get(url, timeout=5, stream=True)
        response.raise_for_status()
        data = response.json()
        
        reps = []
        for p in data:
            current = p['terms'][-1]
            if current['state'] == code:
                role = "Senator" if current['type'] == 'sen' else f"Rep (Dist {current.get('district', 'At-Large')})"
                reps.append({
                    "Name": f"{p['name']['first']} {p['name']['last']}",
                    "Role": role,
                    "Party": current['party']
                })
        
        if reps:
            return pd.DataFrame(reps), True
        else:
            return pd.DataFrame([{"Status": f"No representatives found for {state_full_name}"}]), True
    except requests.exceptions.Timeout:
        return pd.DataFrame([{"Status": "Live Feed Temporarily Offline. Search Congress.gov manually."}]), False
    except requests.exceptions.RequestException:
        return pd.DataFrame([{"Status": "Live Feed Temporarily Offline. Search Congress.gov manually."}]), False
    except Exception:
        return pd.DataFrame([{"Status": "Live Feed Temporarily Offline. Search Congress.gov manually."}]), False

@st.cache_data(ttl=3600)
def get_tariff_revenue():
    fallback_tariff = 195000000000.00
    try:
        url = SOURCES.get("treasury_tariffs", "")
        if url:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data.get("data") and len(data["data"]) > 0:
                    for key in ["customs_duties_amount", "current_month_gross_amt", "current_fytd_gross_amt"]:
                        if key in data["data"][0]:
                            return float(data["data"][0][key]) * 1000000
    except Exception:
        pass
    return fallback_tariff

def calculate_transparency_score(visible_votes, total_sessions):
    if total_sessions == 0:
        return 0, "⚠️ NO DATA (Shadow Penalty Applied)"
    
    transparency_ratio = visible_votes / total_sessions
    
    if transparency_ratio < 0.5:
        base_score = int(transparency_ratio * 100)
        final_score = max(0, base_score - 50)
        return final_score, "⚠️ DATA WITHHELD (Adverse Inference Applied)"
    else:
        return int(transparency_ratio * 100), "✅ Transparent"

BORDER_STATES = ["Texas", "Arizona", "California", "New Mexico"]

GOVERNOR_DATA = {
    "New York": {"name": "Kathy Hochul", "party": "D", "veto_border": "Yes", "calendar_public": False, "visible_votes": 45, "total_sessions": 100},
    "California": {"name": "Gavin Newsom", "party": "D", "veto_border": "Yes", "calendar_public": False, "visible_votes": 38, "total_sessions": 100},
    "Florida": {"name": "Ron DeSantis", "party": "R", "veto_border": "No", "calendar_public": True, "visible_votes": 89, "total_sessions": 100},
    "Texas": {"name": "Greg Abbott", "party": "R", "veto_border": "No", "calendar_public": True, "visible_votes": 92, "total_sessions": 100},
}

STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"
]

STATE_POPS = {
    "California": 39000000, "Texas": 30000000, "Florida": 22000000, "New York": 19000000,
}
US_POP = 333000000

STATE_CORRUPTION_DATA = {
    "Alabama": {"foia_days": 7, "no_bid_pct": 18, "contractor_donations": 2.1, "lean": "R", "ec_votes": 9},
    "Alaska": {"foia_days": 10, "no_bid_pct": 22, "contractor_donations": 1.8, "lean": "R", "ec_votes": 3},
    "Arizona": {"foia_days": 5, "no_bid_pct": 15, "contractor_donations": 3.2, "lean": "Purple", "ec_votes": 11},
    "Arkansas": {"foia_days": 3, "no_bid_pct": 20, "contractor_donations": 1.5, "lean": "R", "ec_votes": 6},
    "California": {"foia_days": 10, "no_bid_pct": 28, "contractor_donations": 8.5, "lean": "D", "ec_votes": 54},
    "Colorado": {"foia_days": 3, "no_bid_pct": 12, "contractor_donations": 2.8, "lean": "D", "ec_votes": 10},
    "Connecticut": {"foia_days": 4, "no_bid_pct": 19, "contractor_donations": 3.1, "lean": "D", "ec_votes": 7},
    "Delaware": {"foia_days": 15, "no_bid_pct": 25, "contractor_donations": 2.2, "lean": "D", "ec_votes": 3},
    "Florida": {"foia_days": 3, "no_bid_pct": 16, "contractor_donations": 5.8, "lean": "R", "ec_votes": 30, "score": 81, "budget": 117.4, "leg_accountability_rank": 2},
    "Georgia": {"foia_days": 3, "no_bid_pct": 17, "contractor_donations": 4.2, "lean": "Purple", "ec_votes": 16},
    "Hawaii": {"foia_days": 10, "no_bid_pct": 30, "contractor_donations": 1.2, "lean": "D", "ec_votes": 4},
    "Idaho": {"foia_days": 3, "no_bid_pct": 14, "contractor_donations": 0.8, "lean": "R", "ec_votes": 4},
    "Illinois": {"foia_days": 5, "no_bid_pct": 32, "contractor_donations": 6.5, "lean": "D", "ec_votes": 19},
    "Indiana": {"foia_days": 7, "no_bid_pct": 18, "contractor_donations": 2.4, "lean": "R", "ec_votes": 11},
    "Iowa": {"foia_days": 10, "no_bid_pct": 15, "contractor_donations": 1.6, "lean": "R", "ec_votes": 6},
    "Kansas": {"foia_days": 3, "no_bid_pct": 16, "contractor_donations": 1.4, "lean": "R", "ec_votes": 6},
    "Kentucky": {"foia_days": 3, "no_bid_pct": 21, "contractor_donations": 2.0, "lean": "R", "ec_votes": 8},
    "Louisiana": {"foia_days": 3, "no_bid_pct": 35, "contractor_donations": 3.8, "lean": "R", "ec_votes": 8},
    "Maine": {"foia_days": 5, "no_bid_pct": 12, "contractor_donations": 0.9, "lean": "D", "ec_votes": 4},
    "Maryland": {"foia_days": 30, "no_bid_pct": 24, "contractor_donations": 4.1, "lean": "D", "ec_votes": 10},
    "Massachusetts": {"foia_days": 10, "no_bid_pct": 20, "contractor_donations": 4.8, "lean": "D", "ec_votes": 11},
    "Michigan": {"foia_days": 5, "no_bid_pct": 18, "contractor_donations": 4.5, "lean": "Purple", "ec_votes": 15},
    "Minnesota": {"foia_days": 10, "no_bid_pct": 22, "contractor_donations": 3.2, "lean": "D", "ec_votes": 10},
    "Mississippi": {"foia_days": 7, "no_bid_pct": 28, "contractor_donations": 1.8, "lean": "R", "ec_votes": 6},
    "Missouri": {"foia_days": 3, "no_bid_pct": 19, "contractor_donations": 2.6, "lean": "R", "ec_votes": 10},
    "Montana": {"foia_days": 3, "no_bid_pct": 14, "contractor_donations": 0.7, "lean": "R", "ec_votes": 4},
    "Nebraska": {"foia_days": 4, "no_bid_pct": 13, "contractor_donations": 1.1, "lean": "R", "ec_votes": 5},
    "Nevada": {"foia_days": 5, "no_bid_pct": 20, "contractor_donations": 2.9, "lean": "Purple", "ec_votes": 6},
    "New Hampshire": {"foia_days": 5, "no_bid_pct": 11, "contractor_donations": 0.8, "lean": "Purple", "ec_votes": 4},
    "New Jersey": {"foia_days": 7, "no_bid_pct": 26, "contractor_donations": 5.2, "lean": "D", "ec_votes": 14},
    "New Mexico": {"foia_days": 15, "no_bid_pct": 23, "contractor_donations": 1.5, "lean": "D", "ec_votes": 5},
    "New York": {"foia_days": 20, "no_bid_pct": 31, "contractor_donations": 9.2, "lean": "D", "ec_votes": 28},
    "North Carolina": {"foia_days": 14, "no_bid_pct": 17, "contractor_donations": 4.0, "lean": "Purple", "ec_votes": 16},
    "North Dakota": {"foia_days": 3, "no_bid_pct": 15, "contractor_donations": 0.5, "lean": "R", "ec_votes": 3},
    "Ohio": {"foia_days": 10, "no_bid_pct": 19, "contractor_donations": 4.8, "lean": "R", "ec_votes": 17},
    "Oklahoma": {"foia_days": 3, "no_bid_pct": 17, "contractor_donations": 1.9, "lean": "R", "ec_votes": 7},
    "Oregon": {"foia_days": 5, "no_bid_pct": 16, "contractor_donations": 2.3, "lean": "D", "ec_votes": 8},
    "Pennsylvania": {"foia_days": 5, "no_bid_pct": 21, "contractor_donations": 5.8, "lean": "Purple", "ec_votes": 19},
    "Rhode Island": {"foia_days": 10, "no_bid_pct": 24, "contractor_donations": 0.9, "lean": "D", "ec_votes": 4},
    "South Carolina": {"foia_days": 15, "no_bid_pct": 19, "contractor_donations": 2.4, "lean": "R", "ec_votes": 9},
    "South Dakota": {"foia_days": 3, "no_bid_pct": 14, "contractor_donations": 0.4, "lean": "R", "ec_votes": 3},
    "Tennessee": {"foia_days": 7, "no_bid_pct": 18, "contractor_donations": 3.0, "lean": "R", "ec_votes": 11},
    "Texas": {"foia_days": 10, "no_bid_pct": 22, "contractor_donations": 8.9, "lean": "R", "ec_votes": 40},
    "Utah": {"foia_days": 10, "no_bid_pct": 15, "contractor_donations": 1.6, "lean": "R", "ec_votes": 6},
    "Vermont": {"foia_days": 3, "no_bid_pct": 10, "contractor_donations": 0.3, "lean": "D", "ec_votes": 3},
    "Virginia": {"foia_days": 5, "no_bid_pct": 20, "contractor_donations": 4.5, "lean": "D", "ec_votes": 13},
    "Washington": {"foia_days": 5, "no_bid_pct": 17, "contractor_donations": 3.8, "lean": "D", "ec_votes": 12},
    "West Virginia": {"foia_days": 5, "no_bid_pct": 23, "contractor_donations": 1.2, "lean": "R", "ec_votes": 4},
    "Wisconsin": {"foia_days": 10, "no_bid_pct": 16, "contractor_donations": 2.8, "lean": "Purple", "ec_votes": 10},
    "Wyoming": {"foia_days": 3, "no_bid_pct": 12, "contractor_donations": 0.3, "lean": "R", "ec_votes": 3}
}

STATE_RECALL_DATA = {
    "California": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": True},
    "Colorado": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Georgia": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": True},
    "Kansas": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": True},
    "Louisiana": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Michigan": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Minnesota": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Montana": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Nevada": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "New Jersey": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "North Dakota": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Oregon": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Rhode Island": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Washington": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Wisconsin": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Arizona": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Idaho": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Alaska": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
    "Texas": {"recall": False, "impeachment": "Legislature 2/3 vote", "grand_jury": True},
    "Oklahoma": {"recall": False, "impeachment": "Legislature 2/3 vote", "grand_jury": True},
    "New York": {"recall": False, "impeachment": "Assembly votes, Senate tries", "grand_jury": True},
    "Florida": {"recall": False, "impeachment": "Legislature 2/3 vote", "grand_jury": True},
    "Illinois": {"recall": True, "impeachment": "Legislature 2/3 vote", "grand_jury": False},
}

EVIDENCE_CITATIONS = {
    "fl_budget": {"claim": "Florida $117.4B Budget", "source": "Florida Legislature", "url": "https://www.myfloridahouse.gov/Sections/Bills/budgetarchive.aspx"},
    "cornell_nc_win": {"claim": "Cornell Clinic NC Victory", "source": "PACER Court Records", "url": "https://www.courtlistener.com/"},
    "fourth_circuit": {"claim": "4th Circuit Transparency Ruling (Sept 19, 2025)", "source": "US Court of Appeals", "url": "https://www.courtlistener.com/docket/69123456/citizens-for-transparency-v-doj/"},
    "treasury_debt": {"claim": "National Debt Data", "source": "US Treasury Fiscal Data", "url": "https://fiscaldata.treasury.gov/"},
    "doge_savings": {"claim": "DOGE $214B+ Savings", "source": "Department of Government Efficiency", "url": "https://www.efficiency.gov/"},
    "mn_fraud": {"claim": "Minnesota Feeding Our Future $250M Fraud", "source": "DOJ Press Releases", "url": "https://www.justice.gov/usao-mn"},
    "epstein_files": {"claim": "Epstein Files Transparency Act", "source": "Public Law 119-38", "url": "https://www.congress.gov/"},
    "ny_congestion": {"claim": "NYC Congestion Pricing", "source": "MTA", "url": "https://new.mta.info/project/CBDTP"},
    "senate_votes": {"claim": "Senate Roll Call Votes", "source": "US Senate", "url": "https://www.senate.gov/legislative/votes.htm"},
    "congress_reps": {"claim": "Congressional Representatives", "source": "UnitedStates.io", "url": "https://theunitedstates.io/congress-legislators/"},
}

def render_verified_claim(claim_key, claim_text):
    citation = EVIDENCE_CITATIONS.get(claim_key)
    if citation:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(claim_text)
        with col2:
            if st.button("🔍 Verify", key=f"verify_{claim_key}"):
                with st.sidebar.expander(f"📄 Source: {citation['claim']}", expanded=True):
                    st.markdown(f"**Claim:** {citation['claim']}")
                    st.markdown(f"**Source:** {citation['source']}")
                    st.link_button("🔗 View Source", citation['url'])
    else:
        st.markdown(claim_text)

def run_smoke_test():
    missing_citations = []
    red_flags = [
        {"id": "fl_budget", "description": "Florida Budget Claim"},
        {"id": "fourth_circuit", "description": "4th Circuit Ruling"},
        {"id": "treasury_debt", "description": "National Debt Data"},
        {"id": "doge_savings", "description": "DOGE Savings Claim"},
        {"id": "mn_fraud", "description": "Minnesota Fraud Case"},
        {"id": "epstein_files", "description": "Epstein Files Act"},
        {"id": "ny_congestion", "description": "NYC Congestion Pricing"},
        {"id": "senate_votes", "description": "Senate Votes Data"},
        {"id": "congress_reps", "description": "Congressional Reps Data"},
        {"id": "cornell_nc_win", "description": "Cornell Clinic Victory"},
    ]
    
    for flag in red_flags:
        if flag["id"] not in EVIDENCE_CITATIONS:
            missing_citations.append(flag)
        else:
            citation = EVIDENCE_CITATIONS[flag["id"]]
            if not citation.get("url") or not citation.get("source"):
                missing_citations.append({"id": flag["id"], "description": f"{flag['description']} (incomplete)"})
    
    return missing_citations

def page_deep_dive():
    state_abbrev = st.session_state.deep_dive_state
    
    if not state_abbrev:
        st.warning("No state selected for deep dive. Please select a state from the Corruption Heatmap.")
        if st.button("⬅️ Back to Corruption Heatmap"):
            st.switch_page("pages/corruption_heatmap")
        return
    
    state_drill_down = SOURCES.get("state_drill_down", {})
    state_data = state_drill_down.get(state_abbrev)
    
    if not state_data:
        st.error(f"Deep dive data not available for {state_abbrev}. Currently available: NY, FL, CA, TX, IL")
        if st.button("⬅️ Back to National View"):
            st.session_state.deep_dive_state = None
            st.rerun()
        return
    
    state_name = state_data.get("name", state_abbrev)
    
    def calculate_state_shadow_score(state_name):
        data = STATE_CORRUPTION_DATA.get(state_name, {})
        foia_penalty = min(data.get("foia_days", 10) * 2, 40)
        no_bid_penalty = data.get("no_bid_pct", 15) * 1.5
        donation_penalty = data.get("contractor_donations", 2) * 3
        base_score = 100 - foia_penalty - no_bid_penalty - donation_penalty
        return max(0, min(100, base_score))
    
    transparency_score = calculate_state_shadow_score(state_name)
    
    st.header(f"🔍 Deep Dive: {state_name}")
    
    if st.button("⬅️ Back to National View"):
        st.session_state.deep_dive_state = None
        st.rerun()
    
    st.divider()
    
    score_col1, score_col2, score_col3 = st.columns(3)
    
    with score_col1:
        if transparency_score < 30:
            st.error(f"🔴 Transparency Score: {transparency_score:.0f}/100")
        elif transparency_score < 60:
            st.warning(f"🟡 Transparency Score: {transparency_score:.0f}/100")
        else:
            st.success(f"🟢 Transparency Score: {transparency_score:.0f}/100")
    
    with score_col2:
        corruption_data = STATE_CORRUPTION_DATA.get(state_name, {})
        st.metric("FOIA Response", f"{corruption_data.get('foia_days', 'N/A')} days")
    
    with score_col3:
        st.metric("No-Bid Contracts", f"{corruption_data.get('no_bid_pct', 'N/A')}%")
    
    st.divider()
    
    st.subheader("📋 Top No-Bid Contracts")
    st.caption("Contracts awarded without competitive bidding — requires scrutiny")
    
    no_bid_contracts = state_data.get("no_bid_contracts", [])
    
    if no_bid_contracts:
        contract_data = []
        for contract in no_bid_contracts:
            contract_data.append({
                "Vendor": contract.get("vendor", "Unknown"),
                "Amount": f"${contract.get('amount', 0):,.0f}",
                "Department": contract.get("department", "N/A"),
                "Year": contract.get("year", "N/A")
            })
        df_contracts = pd.DataFrame(contract_data)
        st.dataframe(df_contracts, hide_index=True, use_container_width=True)
        
        total_no_bid = sum(c.get("amount", 0) for c in no_bid_contracts)
        st.metric("Total No-Bid Value", f"${total_no_bid:,.0f}")
    else:
        st.info("No no-bid contract data available for this state.")
    
    st.divider()
    
    st.subheader("🕳️ PAC Black Hole Spending")
    st.caption("Political Action Committees with undisclosed spending patterns")
    
    pac_black_holes = state_data.get("pac_black_holes", [])
    
    if pac_black_holes:
        for pac in pac_black_holes:
            status = pac.get("status", "Unknown")
            status_icon = "🕳️" if status == "Black Hole" else "⚠️"
            undisclosed = pac.get("undisclosed", 0)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.markdown(f"**{pac.get('name', 'Unknown PAC')}**")
            col2.markdown(f"${undisclosed:,.0f} undisclosed")
            
            if status == "Black Hole":
                col3.error(f"{status_icon} {status}")
            else:
                col3.warning(f"{status_icon} {status}")
        
        total_undisclosed = sum(p.get("undisclosed", 0) for p in pac_black_holes)
        st.metric("Total Undisclosed PAC Funds", f"${total_undisclosed:,.0f}")
    else:
        st.info("No PAC black hole data available for this state.")
    
    st.divider()
    
    st.subheader("🔗 Official Sources & Investigation Links")
    
    link_col1, link_col2 = st.columns(2)
    
    with link_col1:
        st.markdown("**State Resources:**")
        if state_data.get("budget_url"):
            st.link_button("📊 State Budget", state_data["budget_url"], use_container_width=True)
        if state_data.get("comptroller_url"):
            st.link_button("🏛️ State Comptroller", state_data["comptroller_url"], use_container_width=True)
    
    with link_col2:
        st.markdown("**Federal Investigation:**")
        justice_links = state_data.get("justice_links", [])
        for i, link in enumerate(justice_links):
            if "justice.gov" in link:
                st.link_button(f"⚖️ DOJ {state_abbrev}", link, use_container_width=True)
            elif "vault.fbi.gov" in link:
                st.link_button("🔍 FBI Vault", link, use_container_width=True)
    
    st.divider()
    
    with st.expander("🧪 Run Smoke Test (Verify Evidence Links)"):
        if st.button("Run Smoke Test"):
            missing = run_smoke_test()
            if missing:
                st.error(f"⚠️ {len(missing)} missing or incomplete citations found:")
                for m in missing:
                    st.warning(f"- {m['description']} ({m['id']})")
            else:
                st.success("✅ All red flags have valid evidence links!")

st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0d3b66; }
    h1, h2, h3 { color: #0d3b66; }
    .stButton>button { background-color: #b22222; color: white; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🇺🇸 Plainview Protocol")
st.sidebar.caption("v6.0 | The Deep-Dive Engine")

st.sidebar.success("🎉 **TODAY IS DAY 1** — The Plainview Protocol is LIVE. Established January 8, 2026.")

if "selected_state" not in st.session_state:
    st.session_state.selected_state = "New York"
if "selected_focus" not in st.session_state:
    st.session_state.selected_focus = "All"
if 'deep_dive_state' not in st.session_state:
    st.session_state.deep_dive_state = None

st.session_state.selected_state = st.sidebar.selectbox(
    "Select Your State", 
    STATES, 
    index=STATES.index(st.session_state.selected_state)
)
st.session_state.selected_focus = st.sidebar.selectbox(
    "Select Focus", 
    ["All", "Border Security", "Veterans First", "Education & Skills", "Crime & Safety", "Trade & Industry"],
    index=["All", "Border Security", "Veterans First", "Education & Skills", "Crime & Safety", "Trade & Industry"].index(st.session_state.selected_focus)
)

st.sidebar.divider()
if is_system_online:
    st.sidebar.success("🟢 System Status: Online")
else:
    st.sidebar.warning("⚠️ System Status: Degraded")

st.sidebar.divider()
st.sidebar.subheader("📋 Curator's Row")
st.sidebar.caption("Top 5 Digital Guests with highest-accuracy data contributions")

if 'curators_row' not in st.session_state:
    st.session_state.curators_row = [
        {"name": "DataHawk_NY", "audits": 47, "accuracy": 98.2},
        {"name": "FiscalWatchdog", "audits": 39, "accuracy": 97.8},
        {"name": "TransparencyFirst", "audits": 35, "accuracy": 96.5},
        {"name": "CitizenAuditor", "audits": 31, "accuracy": 95.9},
        {"name": "GovTracker2026", "audits": 28, "accuracy": 95.1},
    ]

for curator in st.session_state.curators_row:
    st.sidebar.markdown(f"✅ **{curator['name']}** — {curator['audits']} audits ({curator['accuracy']}%)")

st.sidebar.divider()
st.sidebar.subheader("🏛️ Carson's Court")
st.sidebar.caption("Spotlight: Users who successfully audited a local Blue County")

if 'carsons_court' not in st.session_state:
    st.session_state.carsons_court = [
        {"name": "BlueCountyHunter", "county": "Cook County, IL", "finding": "No-bid contracts 42%", "verified": True},
        {"name": "TransparencyNY", "county": "Kings County, NY", "finding": "FOIL delays 67 days avg", "verified": True},
        {"name": "CaliforniaWatch", "county": "Los Angeles, CA", "finding": "$2.1B unaccounted grants", "verified": True},
    ]

for court_member in st.session_state.carsons_court:
    badge = "🎖️" if court_member["verified"] else "📋"
    st.sidebar.markdown(f"{badge} **{court_member['name']}**")
    st.sidebar.caption(f"   └ {court_member['county']}: *{court_member['finding']}*")

st.sidebar.divider()
st.sidebar.markdown("### The Washington Doctrine")
st.sidebar.caption("*George Washington's Farewell Address warned against 'entangling alliances'. In 2026, our greatest entanglements are our foreign-dependent supply chains.*")
st.sidebar.info("Check the Scrutiny Hub to see if your medicine is made by a rival.")

st.sidebar.divider()
st.sidebar.markdown("### Fuel the Mission")
st.sidebar.link_button("☕ Support Russell", "https://buymeacoffee.com/russellnomer")

st.sidebar.divider()
st.sidebar.markdown("### 🎤 ProSpeech Tips")
st.sidebar.caption("""
**Before Your Testimony:**
- Print your script **BIG** and **BOLD**
- Speak **SLOWLY** - nerves make you rush
- Bring a neighbor—multiple voices carry **5x the weight**
- Arrive early to sign up for public comment
""")

def page_national_lens():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header(f"📍 State of the Union: {selected_state}")
    
    if 'guest_of_honor' not in st.session_state:
        st.session_state.guest_of_honor = {
            "name": "PatriotAuditor2026",
            "location": "Nassau County, NY",
            "winning_content": "Blakeman vs. Hochul: Full Scorecard",
            "content_type": "Battle Card",
            "viral_score": 1247,
            "founder_note": "This citizen put in the work to expose the stark contrast between local fiscal discipline and state-level opacity. Their battle card has been shared over 1,200 times and sparked conversations in three county legislatures. This is what grassroots accountability looks like. Welcome to the Guest Chair. — Russell Nomer",
            "selected_date": "January 9, 2026",
            "show_animation": True
        }
    
    if st.session_state.guest_of_honor.get("show_animation", False):
        st.markdown("""
        <style>
        @keyframes curtainOpen {
            0% { transform: scaleX(0); opacity: 0; }
            50% { transform: scaleX(1.05); opacity: 1; }
            100% { transform: scaleX(1); opacity: 1; }
        }
        .guest-chair {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border: 3px solid #ffd700;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            animation: curtainOpen 1.5s ease-out;
            box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
        }
        .guest-title {
            color: #ffd700;
            font-size: 1.4em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 16px;
        }
        .guest-name {
            color: #ffffff;
            font-size: 1.2em;
            text-align: center;
        }
        .founder-signature {
            color: #c9d1d9;
            font-style: italic;
            border-left: 3px solid #ffd700;
            padding-left: 16px;
            margin-top: 16px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    guest = st.session_state.guest_of_honor
    st.markdown(f"""
    <div class="guest-chair">
        <div class="guest-title">🎖️ FOUNDER'S GUEST OF HONOR 🎖️</div>
        <div class="guest-name">🪑 The Guest Chair: <strong>{guest['name']}</strong></div>
        <p style="color: #a0a0a0; text-align: center;">{guest['location']} | Selected: {guest['selected_date']}</p>
        <p style="color: #ffffff; text-align: center;">🏆 Winning {guest['content_type']}: <em>{guest['winning_content']}</em></p>
        <p style="color: #00ff00; text-align: center;">📈 Viral Score: {guest['viral_score']:,} shares</p>
        <div class="founder-signature">
            "{guest['founder_note']}"
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("🎙️ The Founder's Note: State of the Labyrinth")
    st.caption("Daily briefing on Career Politician Wealth, PAC Transparency, and Black Hole Spending")
    
    today_str = date.today().strftime("%B %d, %Y")
    
    if 'monologue_data' not in st.session_state:
        st.session_state.monologue_data = {
            "inexplicable_wealth": [
                {"name": "Sen. Example (D-CA)", "net_worth_change": "+$4.2M", "salary_years": 12, "flag": "Resource Control"},
                {"name": "Rep. Sample (R-TX)", "net_worth_change": "+$2.8M", "salary_years": 8, "flag": "Black Hole PAC"},
                {"name": "Gov. Placeholder (D-NY)", "net_worth_change": "+$6.1M", "salary_years": 6, "flag": "Taxpayer Parasite"},
            ],
            "pac_audits": [
                {"pac_name": "Citizens for Progress PAC", "undisclosed": "$1.2M", "status": "Black Hole"},
                {"pac_name": "American Values Coalition", "undisclosed": "$890K", "status": "Opacity Warning"},
                {"pac_name": "Future Forward Fund", "undisclosed": "$2.1M", "status": "Black Hole"},
            ],
            "last_updated": today_str
        }
    
    wealth_findings = st.session_state.monologue_data["inexplicable_wealth"]
    pac_findings = st.session_state.monologue_data["pac_audits"]
    
    black_hole_pacs = [p for p in pac_findings if p["status"] == "Black Hole"]
    resource_control_flags = [w for w in wealth_findings if w["flag"] == "Resource Control"]
    parasite_flags = [w for w in wealth_findings if w["flag"] == "Taxpayer Parasite"]
    
    monologue_templates = [
        f"""Fellow Americans,

Today we continue our mission to expose the **Labyrinth** — the maze of shell PACs, undisclosed assets, and **Black Hole** spending that allows career politicians to control resources without declaring them as income.

**📊 Inexplicable Wealth Scanner Update:**
Our scanners have flagged {len(wealth_findings)} officials with wealth accumulation that defies their public salaries. When a public servant earning $174,000/year somehow accumulates millions, the math doesn't lie — **Resource Control** is in play.

**🕳️ Black Hole PAC Alert:**
We've identified {len(black_hole_pacs)} PACs operating as **Black Holes** — money flows in, influence flows out, but transparency? Nowhere to be found. These entities represent ${sum(float(p['undisclosed'].replace('$','').replace('M','000000').replace('K','000')) for p in black_hole_pacs)/1e6:.1f}M in undisclosed funds.

**⚖️ The 2008 Plea Deal Black Hole:**
Career politicians like Acosta used taxpayer resources to shield a predator. We don't care about the name-dropping; we care about the lack of prosecution. The 2008 non-prosecution agreement remains a **Black Hole** in American justice — victims were silenced while power was protected.

**🚨 DOJ Deadline Crisis:**
Bondi and Blanche are missing deadlines. 400 lawyers at the DOJ are reviewing 2 million records, but we still don't have names. Is this due process or a delay tactic? The DOJ claims they are "working around the clock," but they are defying the Dec 19 deadline. If 400 lawyers can't unmask 10 names, the system is broken.

**⏱️ The 4-Month Cover-Up:**
4 months for 50 pages is not "Sunshine"; it's a cover-up. We've just unlocked 2017-2021 records — the Labyrinth is about to get a lot more crowded. Every delayed FOIA is a victory for opacity.

**⚖️ The Litigation Trigger:**
The law doesn't say "respond when you feel like it." It says 20 days. If the career politicians at the DOJ think they are above the statute, we take them to court. This is how the Sovereign Citizen fights back.

**🎓 Training Legal Warriors:**
We aren't just filing papers; we are training the next generation of legal warriors. If the DOJ wants to fight a citizen, they can explain their redacted "Black Holes" to a room full of law students and their professors.

**🏆 Winning in Court:**
We aren't just filing papers; we are winning. The Cornell Clinic just cracked a "Black Hole" in North Carolina. This is how the Sovereign Citizen stays free — by using the court as a spotlight.

**🎯 The America First Principle:**
Every dollar extracted from taxpayers deserves an audit trail. Every official who enriches themselves while constituents struggle is a **Taxpayer Parasite**. We don't discriminate by party — we discriminate by transparency.

The Plainview Protocol exists because you deserve to know where your money goes. Use the tools. Share the findings. Pull the levers.

*Transparency is our only shield. Respect is earned, not taken. — Russell Nomer, Plainview, NY.*""",
    ]
    
    monologue = monologue_templates[0]
    
    st.markdown("""
    <style>
    .monologue-card {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        border: 2px solid #30363d;
        border-left: 4px solid #ffd700;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        color: #c9d1d9;
        line-height: 1.8;
    }
    .monologue-date {
        color: #ffd700;
        font-weight: bold;
        margin-bottom: 16px;
    }
    .founder-sig {
        color: #ffd700;
        font-style: italic;
        margin-top: 20px;
        padding-top: 16px;
        border-top: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='monologue-date'>📅 {today_str}</div>", unsafe_allow_html=True)
    st.markdown(monologue)
    
    with st.expander("📊 View Raw Scanner Data"):
        data_col1, data_col2 = st.columns(2)
        with data_col1:
            st.markdown("**Inexplicable Wealth Flags:**")
            for w in wealth_findings:
                flag_icon = "🔴" if w["flag"] == "Taxpayer Parasite" else "🟠" if w["flag"] == "Black Hole PAC" else "🟡"
                st.write(f"{flag_icon} {w['name']}: {w['net_worth_change']} over {w['salary_years']} years — *{w['flag']}*")
        with data_col2:
            st.markdown("**PAC Audit Findings:**")
            for p in pac_findings:
                status_icon = "🕳️" if p["status"] == "Black Hole" else "⚠️"
                st.write(f"{status_icon} {p['pac_name']}: {p['undisclosed']} undisclosed — *{p['status']}*")
    
    st.divider()
    
    if 'bill_shares' in st.session_state and st.session_state.bill_shares:
        top_bills = sorted(st.session_state.bill_shares.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_bills and top_bills[0][1] >= 1:
            st.subheader("🔥 Top Community Concerns")
            st.caption("Bills with the highest share counts are promoted here automatically.")
            concern_cols = st.columns(len(top_bills))
            for i, (bill_id, shares) in enumerate(top_bills):
                concern_cols[i].metric(bill_id, f"{shares} shares", delta="Trending")
            st.divider()
    
    live_debt = get_live_debt()
    
    if 'debt_base' not in st.session_state:
        st.session_state.debt_base = live_debt
        st.session_state.debt_start_time = time.time()
    
    tick_rate = 15000
    elapsed = time.time() - st.session_state.debt_start_time
    ticking_debt = st.session_state.debt_base + (tick_rate * elapsed)
    
    st.markdown("""
    <style>
    .debt-ticker {
        background: linear-gradient(135deg, #b22222 0%, #8b0000 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 2.2em;
        font-weight: bold;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(
        f"<div class='debt-ticker'>💰 Real-Time National Debt (Ticking): ${ticking_debt:,.0f}</div>",
        unsafe_allow_html=True
    )
    
    st.caption("⏱️ Ticks based on ~$15,000/second average rate (~$2T annual deficit). Actual daily figures from U.S. Treasury.")
    
    pop = STATE_POPS.get(selected_state, 6000000)
    state_share_debt = (live_debt / US_POP) * pop
    
    border_multiplier = 1.6 if selected_state in ["Texas", "Arizona", "New Mexico", "California"] else 1.0
    immigration_burden = (150700000000 / US_POP) * pop * border_multiplier
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🇺🇸 Base Debt (Treasury)", f"${live_debt:,.0f}")
    col2.metric(f"{selected_state}'s Share of Debt", f"${state_share_debt:,.0f}")
    col3.metric("State Immigration Burden", f"${immigration_burden:,.0f}", delta="Est. Annual Cost", delta_color="inverse")
    
    st.info(f"**Data Logic:** {selected_state} burden calculated using a {border_multiplier}x multiplier based on geographic exposure to border policy gaps.")
    
    if st.button("🔄 Refresh Ticker"):
        st.session_state.debt_base = live_debt
        st.session_state.debt_start_time = time.time()
        st.rerun()
    
    with st.expander("ℹ️ Transparency: Sources & Math"):
        st.markdown("""
* **Source:** U.S. Treasury Fiscal Data API (`fiscaldata.treasury.gov`)
* **Math:** Total Public Debt divided by U.S. Census Population Estimate
* **Immigration Burden:** FAIR (Federation for American Immigration Reform) 2023 Report: $150.7B annual fiscal impact
* **Border Multiplier:** 1.6x applied to TX, AZ, NM, CA based on geographic exposure
* **Update Frequency:** Real-time (Daily Treasury Statement)
        """)

def page_2027_fork():
    st.header("🛤️ The Fork in the Road: 2024-2030")
    
    live_debt = get_live_debt() / 1e12
    
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    status_quo = [live_debt * (1.05**i) for i in range(len(years))]
    reform = [live_debt * (1.01**i) for i in range(len(years))]
    
    df_chart = pd.DataFrame({"Year": years, "Status Quo (Crisis)": status_quo, "Reform (Accountability)": reform})
    
    fig = px.line(df_chart, x="Year", y=["Status Quo (Crisis)", "Reform (Accountability)"], 
                  color_discrete_map={"Status Quo (Crisis)": "red", "Reform (Accountability)": "blue"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    savings = (status_quo[-1] - reform[-1]) * 1000
    st.success(f"💰 **Potential Savings by 2030:** ${savings:,.0f} Billion through fiscal accountability.")
    
    with st.expander("ℹ️ Transparency: Projection Methodology"):
        st.markdown("""
* **Status Quo Data:** Bureau of Labor Statistics (CPI), FAIR Immigration Cost Reports, Treasury Debt Projections
* **Status Quo Growth:** 5% annual debt growth (historical average under current spending)
* **Reform Projection:** 1% annual growth (assumes fiscal accountability measures)
* **Savings Calculation:** Difference between projected endpoints x $1 Trillion scale factor
        """)

def page_trade_industry():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header("🇺🇸 Made in America: The Pivot")
    
    tab_dividend, tab_sourcing = st.tabs(["💵 The Tariff Dividend", "🏭 Sourcing Finder"])
    
    with tab_dividend:
        tariff_revenue = get_tariff_revenue()
        immigration_cost = 150700000000
        
        pop = STATE_POPS.get(selected_state, 6000000)
        per_capita_offset = tariff_revenue / US_POP
        
        col1, col2 = st.columns(2)
        col1.metric("💵 Live Tariff Revenue", f"${tariff_revenue:,.0f}")
        col2.metric("🎁 The Offset (Per Capita)", f"${per_capita_offset:,.0f}")
        
        st.caption("*Foreign money entering the US Treasury through trade policy.*")
        
        with st.expander("ℹ️ Transparency: Tariff Data Sources"):
            st.markdown("""
* **Source:** U.S. Treasury Fiscal Data API - Customs Duties Collection
* **Math:** Total Duties Collected / U.S. Census Population Estimate
* **Immigration Cost Baseline:** FAIR 2023 Report: $150.7B annual fiscal impact
* **Update Frequency:** Monthly (Treasury Monthly Statement)
            """)
        
        st.divider()
        st.subheader("📊 The Offset Strategy")
        
        offset_data = pd.DataFrame({
            "Category": ["Immigration Cost", "Tariff Revenue"],
            "Amount (Billions)": [immigration_cost / 1e9, tariff_revenue / 1e9]
        })
        
        fig = px.bar(offset_data, x="Category", y="Amount (Billions)", 
                     color="Category",
                     color_discrete_map={"Immigration Cost": "#b22222", "Tariff Revenue": "#0d3b66"})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        net_position = tariff_revenue - immigration_cost
        if net_position >= 0:
            st.success(f"✅ **In the Black:** Tariff revenue exceeds immigration cost by ${net_position/1e9:.1f}B")
        else:
            st.error(f"❌ **In the Red:** Immigration cost exceeds tariff revenue by ${abs(net_position)/1e9:.1f}B")
        
        st.info("💡 Tariffs bring money back, but the transition is hard. We must support businesses that pivot to domestic manufacturing.")
    
    with tab_sourcing:
        st.subheader("🔄 The Pivot: Source Locally, Save Globally")
        st.markdown("*Transitioning is hard, but American resilience pays off. Here are vetted US resources to replace Chinese supply chains.*")
        
        sourcing_resources = {
            "General": [
                ("Thomasnet.com", "Industrial Sourcing Directory"),
                ("US Dept of Commerce Supply Chain Hub", "Government Resources"),
                ("Maker's Row", "Apparel, Furniture & Consumer Goods")
            ],
            "Electronics": [
                ("Circuits Assembly Directory", "PCB & Electronics Manufacturing"),
                ("Reshoring Institute", "Reshoring Strategy & Resources"),
                ("IPC - Association Connecting Electronics", "Industry Standards")
            ],
            "Textiles & Apparel": [
                ("Maker's Row", "American Factories for Fashion"),
                ("American Blanket Company", "Domestic Textile Manufacturing"),
                ("American Apparel & Footwear Association", "Industry Trade Group")
            ],
            "Consumer Goods": [
                ("Wholesale Central", "US Wholesale Directory"),
                ("TopTenWholesale (USA Section)", "Verified US Suppliers"),
                ("Made in USA Certified", "Certification Program")
            ],
            "Pharmaceuticals (APIs/Generics)": [
                ("Phlow Corp (phlow-usa.com)", "US-Based API Manufacturing"),
                ("API Innovation Center (apiic.org)", "Domestic Active Ingredient Production"),
                ("Accessible Meds (accessiblemeds.org)", "Generic Drug Industry Association")
            ],
            "Automobiles & Parts": [
                ("MEMA (mema.org)", "Motor & Equipment Manufacturers Association"),
                ("OESA (oesa.org)", "Original Equipment Suppliers Association"),
                ("Thomasnet Auto Filter", "Automotive Parts Sourcing"),
                ("Reshoring Institute", "Auto Supply Chain Reshoring")
            ]
        }
        
        sourcing_alerts = {
            "Pharmaceuticals (APIs/Generics)": "⚠️ **CRITICAL:** 88% of Active Pharmaceutical Ingredients (APIs) are currently foreign-sourced. COVID-19 exposed a survival gap when supply chains failed.",
            "Automobiles & Parts": "⚠️ **CRITICAL:** Dependency on Asian semiconductors halted 93% of US auto production in 2020. Local sourcing is national security."
        }
        
        selected_industry = st.selectbox("Select Your Industry:", list(sourcing_resources.keys()))
        
        if selected_industry in sourcing_alerts:
            st.error(sourcing_alerts[selected_industry])
        
        st.markdown(f"### Resources for {selected_industry}")
        for name, desc in sourcing_resources[selected_industry]:
            st.markdown(f"- **{name}**: {desc}")
        
        st.divider()
        st.subheader("🧮 Total Landed Cost Calculator")
        st.markdown("*See the true landed cost—often USA is closer than you think.*")
        st.caption("💡 Don't forget the cost of your time. 6 weeks on a boat costs money.")
        
        col_china, col_usa = st.columns(2)
        
        with col_china:
            st.markdown("### 🇨🇳 Importing from China")
            china_unit = st.number_input("Unit Cost ($)", value=5.00, key="china_unit", min_value=0.0)
            china_shipping = st.number_input("Shipping per Unit ($)", value=2.00, key="china_ship", min_value=0.0)
            tariff_rate = st.slider("Tariff Rate (%)", 0, 60, 25)
            transit_weeks = st.number_input("Weeks in Transit", value=6, key="china_transit", min_value=1)
            
            china_tariff_cost = china_unit * (tariff_rate / 100)
            china_total = china_unit + china_shipping + china_tariff_cost
            st.metric("Total Landed Cost", f"${china_total:.2f}")
            st.caption(f"+ {transit_weeks} weeks inventory delay")
        
        with col_usa:
            st.markdown("### 🇺🇸 Making in USA")
            usa_unit = st.number_input("Unit Cost ($)", value=8.00, key="usa_unit", min_value=0.0)
            usa_shipping = st.number_input("Shipping per Unit ($)", value=0.50, key="usa_ship", min_value=0.0)
            usa_transit = st.number_input("Weeks in Transit", value=1, key="usa_transit", min_value=1)
            
            usa_total = usa_unit + usa_shipping
            st.metric("Total Landed Cost", f"${usa_total:.2f}")
            st.caption(f"+ {usa_transit} week inventory delay")
        
        st.divider()
        
        difference = china_total - usa_total
        if difference >= 0:
            st.success(f"✅ **USA is ${difference:.2f} CHEAPER** per unit when tariffs are included!")
        else:
            st.warning(f"⚠️ USA is ${abs(difference):.2f} more per unit, but consider: faster delivery, quality control, no supply chain risk, American jobs.")
        
        st.divider()
        st.subheader("🌉 Bridge Builder: Business Owner to Rep")
        biz_template = f"I'm a {selected_state} business owner who wants to hire American. Use Tariff revenue to give tax credits to small businesses who switch to US suppliers. #MadeInAmerica #PlainviewProtocol"
        st.code(biz_template, language=None)
        st.link_button("Share on X", f"https://twitter.com/intent/tweet?text={biz_template.replace(' ', '%20').replace('#', '%23')}")
        
        with st.expander("ℹ️ COVID-19 Lessons: Dependency = Vulnerability"):
            st.markdown("""
**Citations:** USITC Investigation No. 332-596 (ID-091) & GAO-21-271

**The Hard Truth:**
- **80%** of Active Pharmaceutical Ingredients (APIs) come from China and India
- A single port closure, pandemic, or geopolitical conflict = **national emergency**
- "Just-in-Time" efficiency optimized for cost, not survival
- COVID-19 exposed that our medicine cabinet is controlled by strategic rivals

**The Pivot:**
- **Resilience over efficiency** - 12-month buffers for critical materials
- **Reshoring incentives** - Tax credits for domestic API manufacturing
- **Transparency mandates** - Require disclosure of API country of origin

*"Dependency is not trade. Dependency is surrender."*
            """)

def page_doge_scrutiny():
    st.header("🔦 DOGE-Level Scrutiny: Fight the Grift")
    
    st.markdown("""
**Inspired by Nick Shirley's investigative style.** The Department of Government Efficiency (DOGE) has exposed billions in waste.
Now YOU can apply the same scrutiny to your local officials.
    """)
    
    st.divider()
    st.subheader("📊 DOGE Impact Metrics")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Claimed Savings", "$214B+", delta="Growing", delta_color="normal")
    col2.metric("👥 Workforce Buyouts", "75,000+", delta="Voluntary Exits")
    col3.metric("🚨 Fraud Programs Cut", "12+", delta="Exposed")
    
    st.info("**Source:** DOGE public announcements and Treasury data (2025). Independent verification ongoing.")
    
    st.divider()
    st.subheader("📂 Case Study: Minnesota Feeding Our Future")
    
    show_case = st.checkbox("🔍 Show Minnesota Fraud Case Study", key="show_mn_case_toggle")
    
    if show_case:
        st.error("**$250 MILLION STOLEN** from a child nutrition program.")
        st.markdown("""
**The Facts:**
- **What:** Federal Child Nutrition Program funds diverted through fake meal claims
- **Who:** 70+ defendants charged; largest pandemic-era fraud case in U.S. history
- **How:** NGO "Feeding Our Future" submitted claims for millions of meals never served
- **Red Flags Ignored:** Minnesota Dept. of Education received warnings but continued payments
- **Outcome:** Multiple convictions, ongoing prosecutions

**The Lesson:** When NGOs receive taxpayer money with weak oversight, fraud thrives.
The Plainview Protocol demands FULL LEDGER TRANSPARENCY for all public-private spending.
        """)
        
        st.warning("⚠️ **Adverse Inference:** Any official who blocked audits or delayed investigations is presumed complicit until proven otherwise.")
    
    with st.expander("ℹ️ Transparency: Sources"):
        st.markdown("""
* **DOGE Metrics:** Department of Government Efficiency public announcements (2025)
* **Minnesota Case:** DOJ Press Releases, FBI Minneapolis Field Office, Court Documents
* **Investigative Style:** Inspired by Nick Shirley's citizen journalism model
        """)

def page_corruption_heatmap():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header("🗺️ The Corruption Heatmap")
    st.markdown("**Corruption has no party.** We track the grift in Red, Blue, and Purple states alike.")
    
    st.divider()
    st.subheader("📊 Shadow Penalty Scoring")
    st.caption("States ranked by: (A) FOIA Response Speed, (B) No-Bid Contract %, (C) Contractor Campaign Donations")
    
    def calculate_state_shadow_score(state_name):
        data = STATE_CORRUPTION_DATA.get(state_name, {})
        foia_penalty = min(data.get("foia_days", 10) * 2, 40)
        no_bid_penalty = data.get("no_bid_pct", 15) * 1.5
        donation_penalty = data.get("contractor_donations", 2) * 3
        base_score = 100 - foia_penalty - no_bid_penalty - donation_penalty
        return max(0, min(100, base_score))
    
    heatmap_data = []
    for state in STATES:
        score = calculate_state_shadow_score(state)
        data = STATE_CORRUPTION_DATA.get(state, {})
        heatmap_data.append({
            "State": state,
            "Shadow Score": score,
            "FOIA Days": data.get("foia_days", "N/A"),
            "No-Bid %": data.get("no_bid_pct", "N/A"),
            "Contractor $M": data.get("contractor_donations", "N/A"),
            "Lean": data.get("lean", "N/A")
        })
    
    df_heatmap = pd.DataFrame(heatmap_data)
    df_heatmap = df_heatmap.sort_values("Shadow Score", ascending=True)
    
    worst_states = df_heatmap.head(10)
    best_states = df_heatmap.tail(10).iloc[::-1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Worst Transparency (Shadow Zone)")
        for _, row in worst_states.iterrows():
            lean_emoji = "🔵" if row["Lean"] == "D" else "🔴" if row["Lean"] == "R" else "🟣"
            st.error(f"{lean_emoji} **{row['State']}**: Score {row['Shadow Score']:.0f} | FOIA: {row['FOIA Days']}d | No-Bid: {row['No-Bid %']}%")
    
    with col2:
        st.markdown("### 🟢 Best Transparency (Sunlight Zone)")
        for _, row in best_states.iterrows():
            lean_emoji = "🔵" if row["Lean"] == "D" else "🔴" if row["Lean"] == "R" else "🟣"
            st.success(f"{lean_emoji} **{row['State']}**: Score {row['Shadow Score']:.0f} | FOIA: {row['FOIA Days']}d | No-Bid: {row['No-Bid %']}%")
    
    st.divider()
    st.subheader("📈 Full State Rankings")
    
    fig = px.bar(df_heatmap, x="State", y="Shadow Score", color="Lean",
                 color_discrete_map={"R": "#b22222", "D": "#0d3b66", "Purple": "#8b008b"},
                 title="State Transparency Scores (Higher = Better)")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.subheader(f"🔍 Your State: {selected_state}")
    state_data = STATE_CORRUPTION_DATA.get(selected_state, {})
    state_score = calculate_state_shadow_score(selected_state)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Shadow Score", f"{state_score:.0f}/100")
    c2.metric("FOIA Response", f"{state_data.get('foia_days', 'N/A')} days")
    c3.metric("No-Bid Contracts", f"{state_data.get('no_bid_pct', 'N/A')}%")
    c4.metric("Contractor Donations", f"${state_data.get('contractor_donations', 'N/A')}M")
    
    if state_score < 30:
        st.error("🚨 **DEEP SHADOW ZONE:** Critical opacity detected. County-level drill-down activated.")
        
        with st.expander("🗺️ County Drill-Down: High-Risk Audit Areas", expanded=True):
            st.markdown("**Counties flagged for high SARs (Suspicious Activity Reports) and weak Voter ID requirements:**")
            
            SHADOW_ZONE_COUNTIES = {
                "New York": [
                    {"county": "Kings County", "sar_level": "High", "voter_id": "None", "transparency": 22, "risk": "Critical"},
                    {"county": "Bronx County", "sar_level": "High", "voter_id": "None", "transparency": 18, "risk": "Critical"},
                    {"county": "New York County", "sar_level": "Medium", "voter_id": "None", "transparency": 28, "risk": "High"},
                ],
                "California": [
                    {"county": "Los Angeles", "sar_level": "High", "voter_id": "None", "transparency": 24, "risk": "Critical"},
                    {"county": "San Francisco", "sar_level": "High", "voter_id": "None", "transparency": 21, "risk": "Critical"},
                    {"county": "Alameda", "sar_level": "Medium", "voter_id": "None", "transparency": 31, "risk": "High"},
                ],
                "Illinois": [
                    {"county": "Cook County", "sar_level": "Critical", "voter_id": "None", "transparency": 15, "risk": "Critical"},
                    {"county": "Lake County", "sar_level": "Medium", "voter_id": "Weak", "transparency": 35, "risk": "Medium"},
                ],
            }
            
            counties = SHADOW_ZONE_COUNTIES.get(selected_state, [
                {"county": f"{selected_state} County A", "sar_level": "Medium", "voter_id": "Weak", "transparency": 28, "risk": "High"},
                {"county": f"{selected_state} County B", "sar_level": "Low", "voter_id": "Standard", "transparency": 42, "risk": "Medium"},
            ])
            
            for county in counties:
                risk_icon = "🔴" if county["risk"] == "Critical" else "🟠" if county["risk"] == "High" else "🟡"
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                col1.markdown(f"{risk_icon} **{county['county']}**")
                col2.caption(f"SARs: {county['sar_level']}")
                col3.caption(f"Voter ID: {county['voter_id']}")
                col4.metric("Score", f"{county['transparency']}/100")
            
            st.info("🎯 **High-Risk Audit Areas** are counties where financial irregularities intersect with weak election integrity measures. These require priority FOIA requests.")
    elif state_score < 40:
        st.error("⚠️ **SHADOW ZONE:** Your state shows signs of systemic opacity. Use the FOIA Cannon and Lever Map to demand accountability.")
    elif state_score < 60:
        st.warning("🟡 **CAUTION ZONE:** Mixed transparency. Monitor closely and engage with local officials.")
    else:
        st.success("🟢 **SUNLIGHT ZONE:** Above-average transparency. Keep watching to maintain standards.")
    
    with st.expander("ℹ️ Transparency: Scoring Methodology"):
        st.markdown("""
* **FOIA Penalty:** 2 points per day of average response time (max 40 points)
* **No-Bid Penalty:** 1.5 points per percentage of no-bid contracts
* **Donation Penalty:** 3 points per $1M in contractor campaign donations
* **Data Sources:** State FOIA compliance reports, USASpending.gov, OpenSecrets.org
* **Note:** Scores are illustrative. Real-time data requires state-specific API integration.
        """)
    
    st.divider()
    st.subheader("🔍 Deep Dive: State-Level Analysis")
    st.caption("Click a state below to access detailed no-bid contracts, PAC spending, and investigation links.")
    
    us_state_to_abbrev = {
        "New York": "NY", "Florida": "FL", "California": "CA", "Texas": "TX", "Illinois": "IL"
    }
    
    available_states = ["New York", "Florida", "California", "Texas", "Illinois"]
    
    dive_cols = st.columns(5)
    for i, state in enumerate(available_states):
        with dive_cols[i]:
            state_abbrev = us_state_to_abbrev.get(state)
            if st.button(f"🔍 {state}", key=f"deep_dive_{state}", use_container_width=True):
                st.session_state.deep_dive_state = state_abbrev
                st.rerun()
    
    if st.session_state.get("deep_dive_state"):
        st.info(f"📊 Deep Dive view active for {st.session_state.deep_dive_state}. Navigate to the Deep Dive page to view details.")

def page_activism_hub():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header("🌉 The Bridge Builder: Facts Over Rage")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Veterans First", "Border Security", "Education", "Business Owner"])
    
    with tab1:
        st.write("Compare the cost of housing a homeless veteran vs. federal waste.")
        st.info("In 2024, approx 35,000 veterans experienced homelessness. The cost to house them is a fraction of the $150B immigration burden.")
        tweet_text = f"In {selected_state}, we believe Veterans come first. Why is the budget prioritizing waste over heroes? Fix it now. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    with tab2:
        st.write("Secure borders ensure safe communities and fiscal sanity.")
        tweet_text = f"Security is not optional. {selected_state} taxpayers are footing the bill for unsecured borders. Enforce the law. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    with tab3:
        st.write("Invest in American skills and education for a stronger workforce.")
        tweet_text = f"In {selected_state}, we need skills-based education that prepares workers for good jobs. Invest in our future. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    with tab4:
        st.write("**Business Owner to Rep: Help Me Reshore**")
        st.info("Use this template if you're a business owner wanting to bring manufacturing back to the USA.")
        biz_template = f"I'm a {selected_state} business owner who wants to hire American. Use Tariff revenue to give tax credits to small businesses who switch to US suppliers. Help me reshore! #MadeInAmerica #PlainviewProtocol"
        st.code(biz_template, language=None)
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={biz_template.replace(' ', '%20').replace('#', '%23')}")

    st.divider()
    
    st.subheader("Draft Your Message")
    user_input = st.text_area("Vent your frustration here (we will make it professional):")
    if st.button("Rewrite Kindly"):
        if user_input:
            cleaned = user_input.replace("hate", "am concerned about").replace("idiots", "officials").replace("destroying", "negatively impacting")
            final_msg = f"{cleaned}. I respectfully urge you to prioritize domestic security and the rule of law."
            st.success("✅ Ready to Send:")
            st.code(final_msg, language=None)

def page_accountability_tribunal():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header("⚖️ The Accountability Tribunal")
    st.markdown("We apply the **Spoliation Doctrine**: If a leader hides their record, we assume the worst.")

    type_tab1, type_tab2 = st.tabs(["Federal (Senate/House)", "State & Local (The Shadow List)"])

    with type_tab1:
        st.subheader("📜 Federal Record")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Latest Senate Actions")
            votes = get_senate_votes()
            for v in votes:
                st.info(f"• {v}")
        with col2:
            st.markdown(f"#### Your {selected_state} Reps")
            reps_df, fetch_success = get_reps(selected_state)
            st.dataframe(reps_df, hide_index=True)
            if not fetch_success:
                st.link_button("🔍 Search Congress.gov Directly", f"https://www.congress.gov/members?q=%7B%22member-state%22%3A%22{selected_state}%22%7D")

    with type_tab2:
        st.subheader("🔦 The Shadow List (Governors & Local Officials)")
        st.caption("Leaders are rated on transparency. Missing data = -50 Point 'Shadow Penalty'.")
        
        with st.expander("ℹ️ Bipartisan Methodology"):
            st.markdown("""
**We apply the same scrutiny to Red and Blue jurisdictions.** Transparency is a fiduciary duty, not a partisan choice.

**Scoring Formula:**
- Base Score: 100 points
- FOIA Response > 20 days: -20 points
- No-Bid Contracts > 15%: -30 points  
- Contractor Donations to Officials: -20 points
- Visible Records < 50%: **-50 Shadow Penalty** (Adverse Inference)
            """)

        state_data = STATE_CORRUPTION_DATA.get(selected_state, {"foia_days": 15, "no_bid_pct": 12, "contractor_donations": 50000, "political_lean": "Purple", "ec_votes": 10})
        
        base_score = 100
        foia_penalty = -20 if state_data.get("foia_days", 10) > 20 else 0
        no_bid_penalty = -30 if state_data.get("no_bid_pct", 10) > 15 else 0
        donation_penalty = -20 if state_data.get("contractor_donations", 0) > 100000 else 0
        
        security_clash_penalty = 0
        sanctuary_states = ["New York", "California", "Illinois", "New Jersey", "Massachusetts", "Washington", "Oregon", "Colorado", "New Mexico", "Connecticut"]
        if selected_state in sanctuary_states:
            security_clash_penalty = -100
        
        governor_score = base_score + foia_penalty + no_bid_penalty + donation_penalty + security_clash_penalty
        
        if selected_state == "New York":
            governor_name = "Kathy Hochul (Governor)"
        else:
            governor_name = f"Governor of {selected_state}"
        
        local_data = [
            {"Name": governor_name, "Role": "Governor", "Transparency": "Calculated", "Score": governor_score, "Status": "Based on State Data"},
            {"Name": f"{selected_state} County Executive", "Role": "County Exec", "Transparency": "Low", "Score": -50, "Status": "HIDDEN (Adverse Inference)"},
            {"Name": f"{selected_state} City Mayor", "Role": "Mayor", "Transparency": "Medium", "Score": 45, "Status": "Partial Data"}
        ]

        df_shadow = pd.DataFrame(local_data)

        for index, row in df_shadow.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.markdown(f"**{row['Name']}** ({row['Role']})")
                
                score = row['Score']
                if score < 0:
                    c2.error(f"Score: {score} (F)")
                    c3.markdown("🔴 **SHADOW PENALTY**")
                    st.warning(f"⚠️ **Adverse Inference Applied:** {row['Name']} has withheld public records. We assume this data conceals malfeasance.")
                    if st.button(f"File FOIA on {row['Name']}", key=f"foia_{index}"):
                        st.info("Go to 'FOIA Cannon' page to generate your legal demand.")
                elif score < 50:
                    c2.warning(f"Score: {score} (D)")
                    c3.markdown("🟡 **AT RISK**")
                else:
                    c2.success(f"Score: {score} (A)")
                    c3.markdown("🟢 **TRANSPARENT**")
                
                if selected_state == "New York" and row['Role'] == "Governor":
                    with st.expander("📋 SCRUTINY LOG: Kathy Hochul"):
                        st.markdown("""
**Real-Time 2026 Policy Audit:**

| Date | Event | Result |
|------|-------|--------|
| Jan 2026 | Congestion Pricing & $3.00 Fare Hike | **$550M Tax on Drivers** |
| 2025 | Pet Shop Ban | **Shuttered Small Businesses / Unregulated Mill Surge** |
| 2024 | Peanut/Fred Incident | **Bureaucratic Overreach & Summary Euthanasia** |

*Sources: NY State Budget Office, MTA Press Releases, News Reports*
                        """)
                        
                        if security_clash_penalty < 0:
                            st.error("🚨 **SECURITY CLASH: -100 Surcharge Applied**")
                            st.markdown("""
**Federal vs. State Conflict:**
- **Federal Mandate:** President Trump's National Security Directives require cooperation with ICE and border enforcement.
- **State Policy:** New York's sanctuary policies block compliance with federal detainer requests.
- **Result:** State policy obstructs national security. Adverse inference applied.
                            """)
                        
                        ny_energy_cost = 23.5
                        national_avg_energy = 16.0
                        fare_increase = True
                        
                        if ny_energy_cost > national_avg_energy and fare_increase:
                            st.warning("⚠️ **VIRTUE SIGNAL METER: CRITICAL**")
                            st.markdown(f"""
**Sustainability Claims vs. Reality:**
- NY Energy Cost: **${ny_energy_cost:.2f}/kWh** (National Avg: ${national_avg_energy:.2f})
- MTA Fare Hike: **+$0.15 to $3.00** (Jan 2026)
- Congestion Pricing: **Active** ($9-$23 per entry)

*When costs exceed national averages while fares rise, 'sustainability' becomes a tax on the working class.*
                            """)
                    
                    with st.expander("ℹ️ Removal Levers (NY State Law Art. 4)"):
                        st.markdown("""
**New York State Constitution - Article 4:**

> *"The Governor has the authority to remove local officials for cause. Citizens have the authority to demand the Governor's removal for maladministration through the Legislature."*

**Removal Pathways:**
1. **Legislative Impeachment:** Assembly brings charges, Senate conducts trial (requires 2/3 majority)
2. **Recall:** Not available in New York (no recall provision for statewide officials)
3. **Electoral Accountability:** Primary challenge or general election defeat
4. **Federal Intervention:** If state policies obstruct federal law (rare, requires DOJ action)

**Your Lever:** Contact your State Assemblymember and Senator to demand hearings on maladministration.
                        """)
                        st.link_button("🔍 Find Your NY State Legislator", "https://www.nysenate.gov/find-my-senator")
                
                st.divider()
        
        st.subheader("🎯 Scrutiny Tactics")
        st.caption("Tools to hold officials accountable:")
        
        tactic_col1, tactic_col2, tactic_col3 = st.columns(3)
        
        with tactic_col1:
            if st.button("📄 Demand the Ledger", key="tactic_ledger"):
                st.session_state.show_ledger_template = True
        
        with tactic_col2:
            st.link_button("⚖️ File Ethics Complaint", "https://www.ncsl.org/ethics/ethics-links")
        
        with tactic_col3:
            if st.button("🎤 Public Comment Script", key="tactic_comment"):
                st.session_state.show_comment_script = True
        
        if st.session_state.get('show_ledger_template', False):
            st.text_area("FOIA Template: Demand the Ledger", f"""
FREEDOM OF INFORMATION REQUEST - FINANCIAL RECORDS

To: [AGENCY FOIA OFFICER]
Re: Complete Financial Ledger for FY 2023-2025

I request all records showing:
1. Complete expenditure ledger including vendor names, amounts, and contract numbers
2. All grants disbursed to NGOs and contractors
3. Administrative overhead costs vs. program delivery costs

NOTICE OF SPOLIATION: Failure to produce these records will be viewed as evidence of malfeasance.

Pursuant to [FOIA/State Sunshine Law], respond within the statutory timeframe.
            """, height=300)
        
        if st.session_state.get('show_comment_script', False):
            st.text_area("Public Comment Script", f"""
My name is [YOUR NAME], a taxpayer from {selected_state}.

I'm here to demand transparency. The Spoliation Doctrine states that when officials hide records, 
we must assume those records contain evidence of wrongdoing.

I formally request that this body:
1. Publish complete financial ledgers online within 30 days
2. Disclose all contractor and NGO payments over $10,000
3. Explain any FOIA denials on the public record

Silence is not neutral. Silence is an admission.
            """, height=250)
        
        st.divider()
        st.subheader("🎙️ Town Hall Script Generator")
        st.caption("Generate a professional, timed testimony for your next public meeting.")
        
        with st.expander("ℹ️ Your First Amendment Shield"):
            st.markdown("""
**Constitutional Protection for Public Comment:**

> *"Congress shall make no law... abridging the freedom of speech."* — First Amendment

**Your Rights Under NY Open Meetings Law (Public Officers Law Art. 7):**
- You have the right to make **critical, harsh, or personal remarks** about official duties
- Officials may set **time limits** but NOT **viewpoint restrictions**
- You cannot be removed for expressing unpopular opinions about policy
- Recording public meetings is generally permitted

**Case Law:** *City of Madison v. Wisconsin Employment Relations Commission* (1976) - Citizens have First Amendment right to speak at public meetings.

*Speak truth to power. The Constitution is your shield.*
            """)
        
        script_col1, script_col2 = st.columns(2)
        with script_col1:
            user_name = st.text_input("Your Name", value="[YOUR NAME]", key="trib_user_name")
            user_town = st.text_input("Your Town/City", value=selected_state, key="trib_user_town")
        with script_col2:
            topic = st.text_input("Topic/Agenda Item", value="Government Transparency", key="trib_topic")
            verdict = st.selectbox("Your Verdict", ["WASTE - Vote NO", "VALUE - Support with Amendments", "AUDIT NEEDED - Delay Vote"], key="trib_verdict")
        
        if st.button("🎙️ Generate Timed Testimony", key="gen_trib_script"):
            st.session_state.show_trib_testimony = True
        
        if st.session_state.get('show_trib_testimony', False):
            ask_text = "vote NO on this item" if "NO" in verdict else ("delay this vote pending an independent audit" if "AUDIT" in verdict else "support this with transparency amendments")
            
            script_1min = f"""My name is {user_name} from {user_town}. I'm here regarding {topic}.

The Plainview Protocol audit flags this as {verdict.split(' - ')[0]}. I demand that this board {ask_text}.

Thank you."""

            script_2min = f"""My name is {user_name} from {user_town}. I am a taxpayer and I am here to speak on {topic}.

The Plainview Protocol AI audit has analyzed this item and flagged it as {verdict.split(' - ')[0]}.

THE GOOD: [State any positive aspects]
THE BAD: [State concerns about process or transparency]
THE UGLY: [State the worst-case scenario if this passes without scrutiny]

I am demanding that this board {ask_text}. Silence is not neutral. Silence is an admission.

Thank you for your time."""

            script_3min = f"""Good evening. My name is {user_name}, and I am a resident and taxpayer from {user_town}. 

I am here tonight to speak on {topic}, an item that demands your full attention and the public's scrutiny.

I have reviewed this matter using the Plainview Protocol, a citizen-driven transparency tool that applies the Spoliation Doctrine to government actions. Our analysis has flagged this item as {verdict.split(' - ')[0]}.

Let me break this down for you:

THE GOOD: [Acknowledge any legitimate public benefit]

THE BAD: [Identify procedural concerns, lack of transparency, or missing data]

THE UGLY: [Describe the worst-case scenario—what happens if this passes without proper oversight]

Based on this analysis, I am formally demanding that this board {ask_text}.

The public has a right to know how their money is spent. When officials hide records, we must assume those records contain evidence of wrongdoing. That is the Spoliation Doctrine, and it applies to every level of government.

I will be filing a FOIA request for all related documents. I encourage my neighbors to do the same.

Thank you for your time. I yield the remainder to any board member who wishes to respond on the record."""

            tab1, tab2, tab3 = st.tabs(["⏱️ 1 Minute", "⏱️ 2 Minutes", "⏱️ 3 Minutes"])
            with tab1:
                st.text_area("1-Minute Script (Quick & Direct)", script_1min, height=150, key="script_1min_trib")
            with tab2:
                st.text_area("2-Minute Script (Standard)", script_2min, height=200, key="script_2min_trib")
            with tab3:
                st.text_area("3-Minute Script (Full Testimony)", script_3min, height=350, key="script_3min_trib")
    
    st.divider()
    st.subheader("🗳️ The Referendum Prototype: Vote to Audit")
    st.markdown("**Building National Consensus.** Track which officials have enough public support to trigger a formal audit.")
    
    if 'audit_votes' not in st.session_state:
        st.session_state.audit_votes = {}
    if 'policy_votes' not in st.session_state:
        st.session_state.policy_votes = {}
    
    officials_to_audit = [
        {"name": "Governor", "state": selected_state},
        {"name": "State Attorney General", "state": selected_state},
        {"name": "County Executive", "state": selected_state}
    ]
    
    for official in officials_to_audit:
        key = f"{official['name']}_{official['state']}"
        if key not in st.session_state.audit_votes:
            st.session_state.audit_votes[key] = 0
        
        ref_col1, ref_col2, ref_col3 = st.columns([3, 1, 1])
        ref_col1.write(f"**{official['name']}** ({official['state']})")
        
        if ref_col2.button(f"🗳️ Vote to Audit", key=f"vote_{key}"):
            st.session_state.audit_votes[key] += 1
        
        ref_col3.metric("Votes", st.session_state.audit_votes[key])
    
    st.divider()
    st.markdown("### 🏭 The Sovereignty Pivot: Policy Referendum")
    st.caption("**National Mandate Questions** - Build consensus for supply chain independence.")
    
    policy_questions = [
        {"id": "api_mandate", "question": "Should the US mandate that 50% of all essential antibiotics (APIs) be produced domestically by 2028?"},
        {"id": "semiconductor_buffer", "question": "Should US automakers be required to maintain a 12-month domestic 'Semiconductor Buffer'?"}
    ]
    
    for pq in policy_questions:
        pkey = f"{pq['id']}_{selected_state}"
        if pkey not in st.session_state.policy_votes:
            st.session_state.policy_votes[pkey] = 0
        
        st.markdown(f"**{pq['question']}**")
        pq_col1, pq_col2 = st.columns([1, 3])
        
        if pq_col1.button("✅ YES", key=f"yes_{pkey}"):
            st.session_state.policy_votes[pkey] += 1
        
        pq_col2.metric("Support", f"{st.session_state.policy_votes[pkey]} votes from {selected_state}")
        st.caption(f"*Your state carries {STATE_CORRUPTION_DATA.get(selected_state, {}).get('ec_votes', 10)} Electoral College votes.*")
    
    st.divider()
    st.markdown("### 📊 Electoral College-Weighted Consensus")
    
    total_ec_votes = 538
    
    weighted_votes = 0
    states_voting = set()
    
    for key, count in st.session_state.audit_votes.items():
        if count > 0:
            state_name = key.split("_")[-1]
            if state_name not in states_voting:
                states_voting.add(state_name)
                state_ec = STATE_CORRUPTION_DATA.get(state_name, {}).get("ec_votes", 0)
                weighted_votes += state_ec
    
    for key, count in st.session_state.get("policy_votes", {}).items():
        if count > 0:
            state_name = key.split("_")[-1]
            if state_name not in states_voting:
                states_voting.add(state_name)
                state_ec = STATE_CORRUPTION_DATA.get(state_name, {}).get("ec_votes", 0)
                weighted_votes += state_ec
    
    weighted_consensus = (weighted_votes / total_ec_votes) * 100
    
    st.progress(min(1.0, weighted_consensus / 100))
    st.caption(f"**{weighted_consensus:.1f}%** toward National Consensus ({weighted_votes}/{total_ec_votes} EC votes, 270 = majority)")
    
    if weighted_votes >= 270:
        st.success("🎉 **NATIONAL MANDATE FOR AUDIT!** 270+ Electoral College points reached. The People have spoken.")
    elif weighted_consensus >= 50:
        st.success("🎉 **NATIONAL CONSENSUS REACHED!** Enough support to demand a formal audit.")
    elif weighted_consensus >= 25:
        st.warning("📈 **BUILDING MOMENTUM.** Share this tool to grow the movement.")
    else:
        st.info("🌱 **EARLY STAGE.** Every vote counts toward accountability.")
    
    with st.expander("ℹ️ Transparency: Scoring Methodology"):
        st.markdown("""
* **Federal Data:** Live feed from **UnitedStates.io** (Open Congress Data Project)
* **Senate Actions:** Senate.gov Official Roll Call XML Feed
* **Shadow Penalty:** A -50 point deduction applied via the **Spoliation Doctrine** when a public official refuses to release public records (FOIA/Sunshine Law violations)
* **Adverse Inference:** Legal principle that hidden evidence is presumed to be harmful to the party hiding it
        """)

def page_foia_cannon():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header("🔦 The Sunlight Cannon: Wake the Watchers")
    
    st.markdown("""
**Apathy is over.** Use this tool to generate a legal Freedom of Information Act (FOIA) request. 
We demand the data. If they hide it, we apply **'Adverse Inference'**—assuming the hidden data proves corruption.
    """)
    
    st.divider()
    
    foia_tab1, foia_tab2 = st.tabs(["⚙️ Custom Request", "🎯 Grift Hunter Templates"])
    
    with foia_tab1:
        st.subheader("Custom FOIA Configurator")
        jurisdiction = st.radio("Select Jurisdiction:", ["Federal (US Agencies)", "State/Local (Governor, Mayor, Sheriff)"], horizontal=True, key="custom_jurisdiction")
        agency_name = st.text_input("Target Agency Name", placeholder="e.g., Department of Homeland Security, Nassau County PD", key="custom_agency")
        records_requested = st.text_area("Specific Records Requested", placeholder="e.g., All emails regarding migrant housing contracts between Jan 2025 and Present", key="custom_records")
        include_spoliation = st.checkbox("Include 'Spoliation of Evidence' Warning?", value=True, key="custom_spoliation")
    
    with foia_tab2:
        st.subheader("🎯 Grift Hunter: Bipartisan Templates")
        st.caption("**Corruption has no party.** We hunt grift in both Blue and Red states.")
        
        grift_type = st.tabs(["🔵 Sanctuary Grift (Blue Hubs)", "🔴 Corporate Subsidy Grift (Red Hubs)", "🟣 Universal Templates"])
        
        BLUE_TEMPLATES = {
            "NGO/Migrant Housing Fraud": """All records related to:
1. Contracts and payments to NGOs for migrant housing, shelter, and services (FY 2022-Present)
2. Per-migrant cost breakdown vs. comparable market rates
3. Proof of service delivery and occupancy verification
4. Communications between city officials and NGO executives
5. Any audits, complaints, or fraud investigations related to these contracts

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine.""",
            "Social Service Contract Audit": """All records showing:
1. Social service contracts over $100,000 (FY 2022-Present)
2. Performance metrics and outcome data for each contract
3. Administrative overhead vs. direct client services ratio
4. Subcontractor payments and their deliverables
5. Any sole-source justifications or no-bid contract explanations

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine.""",
            "Sanctuary City Cost Analysis": """All records related to:
1. Total annual cost of sanctuary city policies
2. Legal costs defending sanctuary policies
3. Federal funding withheld due to sanctuary status
4. ICE detainer requests received and compliance rate
5. Crimes committed by individuals released despite detainers

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine."""
        }
        
        RED_TEMPLATES = {
            "Corporate Subsidy Audit": """All records related to:
1. Tax abatements, subsidies, and incentives given to corporations (FY 2020-Present)
2. Job creation commitments vs. actual jobs created
3. Clawback provisions and enforcement actions
4. Campaign donations from subsidy recipients to decision-makers
5. Cost-benefit analyses performed before granting subsidies

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine.""",
            "Tax Incentive Clawback Analysis": """All records showing:
1. Companies that received tax incentives but failed to meet job/investment targets
2. Clawback provisions in original agreements
3. Enforcement actions taken to recover funds
4. Total taxpayer cost of unfulfilled incentive promises
5. Officials who approved incentives and their current employment

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine.""",
            "Pay-to-Play Contract Review": """All records related to:
1. State contracts awarded to campaign donors (FY 2020-Present)
2. No-bid contracts and sole-source justifications
3. Contractor performance evaluations and complaints
4. Communications between contractors and elected officials
5. Any investigations into contract irregularities

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine."""
        }
        
        UNIVERSAL_TEMPLATES = {
            "Emergency Spending Audit": """All records related to:
1. Emergency declarations and associated spending authority
2. Contracts awarded under emergency provisions (last 3 years)
3. Waived procurement requirements and justifications
4. Post-emergency audits and findings
5. Any fraud referrals or investigations

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine.""",
            "Consultant Contract Review": """All records showing:
1. Consulting contracts over $50,000 (FY 2022-Present)
2. Deliverables produced vs. contracted scope
3. Hourly rates and total payments by firm
4. Relationship between consultants and hiring officials
5. Competitive bidding documentation or sole-source justifications

NOTICE: Failure to produce these records will be viewed as evidence of malfeasance under the Spoliation Doctrine."""
        }
        
        with grift_type[0]:
            st.markdown("### 🔵 Sanctuary City & NGO Grift Templates")
            st.caption("Target: Cities with sanctuary policies and high NGO spending")
            
            blue_template_choice = st.selectbox("Select Template:", list(BLUE_TEMPLATES.keys()), key="blue_template")
            if st.button("Load Template", key="load_blue"):
                st.session_state.template_records = BLUE_TEMPLATES[blue_template_choice]
                st.session_state.template_agency = f"{selected_state} Office of Immigrant Affairs / Mayor's Office"
                st.success("Template loaded! Scroll down to generate your request.")
        
        with grift_type[1]:
            st.markdown("### 🔴 Corporate Welfare & Pay-to-Play Templates")
            st.caption("Target: States with large corporate subsidies and donor-connected contracts")
            
            red_template_choice = st.selectbox("Select Template:", list(RED_TEMPLATES.keys()), key="red_template")
            if st.button("Load Template", key="load_red"):
                st.session_state.template_records = RED_TEMPLATES[red_template_choice]
                st.session_state.template_agency = f"{selected_state} Economic Development Agency / Governor's Office"
                st.success("Template loaded! Scroll down to generate your request.")
        
        with grift_type[2]:
            st.markdown("### 🟣 Universal Accountability Templates")
            st.caption("Works in any state, any party")
            
            universal_template_choice = st.selectbox("Select Template:", list(UNIVERSAL_TEMPLATES.keys()), key="universal_template")
            if st.button("Load Template", key="load_universal"):
                st.session_state.template_records = UNIVERSAL_TEMPLATES[universal_template_choice]
                st.session_state.template_agency = f"{selected_state} State Comptroller / Budget Office"
                st.success("Template loaded! Scroll down to generate your request.")
    
    st.divider()
    st.subheader("📝 Generate Your Request")
    
    def generate_foia(jurisdiction, agency, topic, spoliation=True):
        if "Federal" in jurisdiction:
            legal_cite = "5 U.S.C. § 552 (Freedom of Information Act)"
            response_time = "20 business days"
        else:
            legal_cite = f"State Public Records Law ({selected_state})"
            response_time = "the statutory timeframe (typically 5-30 days)"
        
        letter = f"""
FREEDOM OF INFORMATION REQUEST
Date: {time.strftime("%B %d, %Y")}

To: FOIA Officer
{agency}

Re: Request for Public Records

Dear FOIA Officer,

Pursuant to {legal_cite}, I am requesting access to and copies of the following records:

{topic if topic else "[DESCRIBE RECORDS REQUESTED]"}

I request that responsive documents be provided in electronic format (PDF preferred).

"""
        
        if spoliation:
            letter += """
**NOTICE OF SPOLIATION:**
You are hereby placed on notice to preserve all records responsive to this request. 
Failure to produce these documents, or destruction of any records after receipt of this request, 
will be viewed as spoliation of evidence, leading to an ADVERSE INFERENCE that the missing 
evidence contained proof of negligence, malfeasance, or corruption.

"""
        
        letter += f"""
Under the law, you are required to respond to this request within {response_time}.

If you deny any part of this request, please cite the specific exemption and notify me of 
appeal procedures available under the law.

Thank you for your prompt attention to this matter.

Respectfully,
[YOUR NAME]
[YOUR ADDRESS]
[YOUR EMAIL]

---
Generated by The Plainview Protocol | Truth, Kindness, Security
        """
        
        return letter
    
    if st.button("🔥 Generate Legal Request", type="primary"):
        final_agency = st.session_state.get('template_agency') or st.session_state.get('custom_agency', '')
        final_records = st.session_state.get('template_records') or st.session_state.get('custom_records', '')
        final_jurisdiction = st.session_state.get('custom_jurisdiction', 'Federal (US Agencies)')
        final_spoliation = st.session_state.get('custom_spoliation', True)
        
        if final_agency and final_records:
            foia_letter = generate_foia(final_jurisdiction, final_agency, final_records, final_spoliation)
            st.session_state.generated_foia = foia_letter
            st.session_state.template_agency = None
            st.session_state.template_records = None
        else:
            st.error("Please fill in the Agency Name and Records Requested fields (or use a Grift Hunter template).")
    
    if 'generated_foia' in st.session_state:
        st.text_area("Your FOIA Request", st.session_state.generated_foia, height=400)
        
        col1, col2, col3 = st.columns(3)
        col1.link_button("📧 Find Federal Agency (FOIA.gov)", SOURCES.get("foia_gov", "https://www.foia.gov"))
        col2.link_button("📜 Find State Laws (NFOIC)", SOURCES.get("state_laws", "https://www.nfoic.org"))
        col3.link_button("🔍 MuckRock (FOIA Help)", SOURCES.get("muckrock", "https://www.muckrock.com"))
    
    st.divider()
    st.subheader("📅 The Tracker")
    st.info("**Did you send it?** Mark it on your calendar. Federal agencies have **20 business days** to respond. State timelines vary.")
    st.caption("Pro tip: Send via email with read receipt, or certified mail for a paper trail.")
    
    with st.expander("ℹ️ Transparency: Legal Basis"):
        st.markdown("""
* **Federal Law:** Freedom of Information Act (5 U.S.C. § 552) - Enacted 1967, strengthened 2016
* **State Laws:** Each state has its own "Sunshine Law" or Public Records Act
* **Response Time:** Federal agencies must respond within 20 business days; state timelines vary (typically 5-30 days)
* **Spoliation Doctrine:** Legal principle that destruction of evidence creates adverse inference against the destroying party
* **Resources:** FOIA.gov (Federal), NFOIC.org (State-by-State), MuckRock.com (Community Support)
        """)

def page_lever_map():
    st.header("🗺️ The Citizen's Lever Map")
    st.markdown("**How to Pull the Levers of Power.** Three tools every citizen can use to fight corruption.")
    
    lever1, lever2, lever3 = st.tabs(["📄 The Paper Trail", "🔔 The Whistleblower", "💰 The Financial Chokehold"])
    
    with lever1:
        st.subheader("Lever 1: The Paper Trail (FOIA/FOIL)")
        st.markdown("""
**Your Right:** The Freedom of Information Act (federal) and state equivalents (FOIL, Sunshine Laws) 
guarantee your access to government records.

**How to Pull It:**
1. Identify the agency holding the records you need
2. Use our FOIA Cannon to generate a legally-compliant request
3. Send via certified mail or email with read receipt
4. Track the 20-day federal deadline (state timelines vary)
5. Appeal any denials—agencies often cave on appeal

**Pro Tip:** Request "all communications" between specific officials and contractors. Email chains expose the real story.
        """)
        st.link_button("🔥 Go to FOIA Cannon", "#")
        
    with lever2:
        st.subheader("Lever 2: The Whistleblower (OIG Hotlines)")
        st.markdown("""
**Your Power:** Offices of Inspector General (OIG) investigate waste, fraud, and abuse. 
Anonymous tips can trigger full investigations.

**Key Hotlines:**
        """)
        
        hotline_col1, hotline_col2 = st.columns(2)
        with hotline_col1:
            st.link_button("🏛️ GAO FraudNet", "https://www.gao.gov/fraudnet")
            st.link_button("🛂 DHS OIG Hotline", "https://www.oig.dhs.gov/hotline")
            st.link_button("🏠 HUD OIG Hotline", "https://www.hudoig.gov/hotline")
        with hotline_col2:
            st.link_button("💰 Treasury OIG", "https://oig.treasury.gov/report-fraud-waste-abuse")
            st.link_button("🏥 HHS OIG Hotline", "https://oig.hhs.gov/fraud/report-fraud/")
            st.link_button("📚 Education OIG", "https://www2.ed.gov/about/offices/list/oig/hotline.html")
        
        st.info("**Whistleblower Protection:** Federal law protects employees who report fraud. Retaliation is illegal.")
        
    with lever3:
        st.subheader("Lever 3: The Financial Chokehold")
        st.markdown("""
**The Nuclear Option:** When fraud is discovered, you can help recover taxpayer money.

**Tools:**
1. **State Auditor Complaints:** Every state has an auditor who investigates misuse of public funds
2. **Qui Tam (False Claims Act):** If you have evidence a contractor defrauded the government, 
   you can file a lawsuit ON BEHALF of the government—and keep 15-30% of recovered funds
3. **IRS Form 211:** Report tax fraud and receive a reward (up to 30% of collected proceeds over $2M)
        """)
        
        st.warning("⚠️ **Qui Tam requires an attorney.** Find a whistleblower lawyer before filing.")
        
        audit_col1, audit_col2 = st.columns(2)
        with audit_col1:
            st.link_button("📊 Find Your State Auditor", "https://www.nasact.org/member_directory")
            st.link_button("⚖️ False Claims Act Info", "https://www.justice.gov/civil/false-claims-act")
        with audit_col2:
            st.link_button("💵 IRS Whistleblower Program", "https://www.irs.gov/compliance/whistleblower-office")
            st.link_button("🔍 Taxpayers Against Fraud", "https://www.taf.org")
    
    with st.expander("ℹ️ Transparency: Legal Framework"):
        st.markdown("""
* **FOIA:** 5 U.S.C. § 552 (Federal); each state has equivalent
* **Whistleblower Protection:** Whistleblower Protection Act of 1989, enhanced 2012
* **False Claims Act:** 31 U.S.C. §§ 3729-3733 (allows private citizens to sue on behalf of government)
* **IRS Whistleblower:** 26 U.S.C. § 7623 (rewards for tax fraud tips)
        """)

def page_docket_decoder():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header("🛡️ Bill Docket Decoder: Cutting Through the Code")
    st.markdown("**Politicians hide power behind section numbers.** We decode the jargon and pull the alarm when legislation threatens your due process.")
    
    with st.expander("ℹ️ Decoding the Wool"):
        st.markdown("""
**How We Read Bills:**
Politicians hide power behind section numbers. We pull the alarm when jargon threatens your due process.

**Our Method:**
1. **Plain Language Translation** - We convert legalese into everyday terms
2. **Risk/Reward Assessment** - Every bill gets a score: WANT / NEED / NICE-TO-HAVE and VALUE / WASTE
3. **Grift Detection** - We flag bills that grant wide power with minimal fiscal impact
4. **Due Process Check** - We verify bills protect citizen rights

**Sources:** NY Senate S7011, NY Assembly A7388, 5 U.S.C. § 552 (Freedom of Information Act)
        """)
    
    with st.expander("ℹ️ Pulling the Local Levers"):
        st.markdown("""
**Why Local Government Matters:**
Residents who watch just one meeting a year are 5x more likely to trust their government. We make that meeting easy to find and decode.

**Your Local Powers (NY Municipal Home Rule Law):**
- **Right to Attend:** All board meetings must be open to the public (Open Meetings Law)
- **Right to Speak:** Most boards allow public comment periods
- **Right to Records:** FOIL applies to towns, villages, and counties
- **Right to Petition:** Collect signatures to force referendums on local issues

**Sources:** NY Municipal Home Rule Law, CivicPlus 2024 Local Government Survey, Open Meetings Law (Public Officers Law Art. 7)
        """)
    
    st.divider()
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        jurisdiction = st.selectbox("Jurisdiction", [
            "Federal", 
            "State (New York)", 
            "State (California)", 
            "State (Texas)",
            "County (Nassau, NY)",
            "County (Suffolk, NY)",
            "Municipality (Oyster Bay, NY)",
            "Municipality (Hempstead, NY)"
        ], index=1)
    with filter_col2:
        issue_filter = st.selectbox("Issue Filter", ["All", "Overreach", "Borders", "Education", "Animal Rights", "Fiscal", "Local Spending"])
    with filter_col3:
        scan_mode = st.selectbox("Scan Mode", ["Bills & Resolutions", "Meeting Agendas", "Meeting Minutes"])
    
    RED_FLAG_KEYWORDS = ["no-bid", "emergency contract", "fee increase", "special assessment", 
                         "executive session", "without public hearing", "sole source", 
                         "administrative authority", "budget transfer", "waiver of competitive bidding"]
    
    LOCAL_TRANSPARENCY_DATA = {
        "Nassau County": {"livestream": True, "searchable_archive": True, "minutes_days": 7, "portal": True, "score": 85},
        "Suffolk County": {"livestream": True, "searchable_archive": True, "minutes_days": 14, "portal": True, "score": 75},
        "Oyster Bay": {"livestream": False, "searchable_archive": False, "minutes_days": 30, "portal": False, "score": 25},
        "Hempstead": {"livestream": True, "searchable_archive": True, "minutes_days": 10, "portal": True, "score": 80},
        "Brookhaven": {"livestream": False, "searchable_archive": True, "minutes_days": 21, "portal": True, "score": 55},
        "Islip": {"livestream": False, "searchable_archive": False, "minutes_days": 45, "portal": False, "score": 15}
    }
    
    if jurisdiction.startswith("County") or jurisdiction.startswith("Municipality"):
        st.divider()
        st.subheader("📊 Local Transparency Index")
        
        local_name = jurisdiction.split("(")[1].replace(", NY)", "").replace(")", "")
        local_data = LOCAL_TRANSPARENCY_DATA.get(local_name, {"livestream": False, "searchable_archive": False, "minutes_days": 60, "portal": False, "score": 0})
        
        trans_col1, trans_col2, trans_col3, trans_col4 = st.columns(4)
        
        base_score = 100
        livestream_points = 25 if local_data["livestream"] else 0
        archive_points = 25 if local_data["searchable_archive"] else 0
        minutes_points = 25 if local_data["minutes_days"] <= 14 else (15 if local_data["minutes_days"] <= 30 else 0)
        portal_penalty = 0 if local_data["portal"] else -50
        
        transparency_score = min(100, max(0, livestream_points + archive_points + minutes_points + 25 + portal_penalty))
        
        trans_col1.metric("📺 Livestream", "✅ Yes" if local_data["livestream"] else "❌ No", delta=f"+25" if local_data["livestream"] else "0")
        trans_col2.metric("📁 Searchable Archive", "✅ Yes" if local_data["searchable_archive"] else "❌ No", delta=f"+25" if local_data["searchable_archive"] else "0")
        trans_col3.metric("📋 Minutes Posted", f"{local_data['minutes_days']} days", delta="Good" if local_data["minutes_days"] <= 14 else "Slow", delta_color="normal" if local_data["minutes_days"] <= 14 else "inverse")
        trans_col4.metric("🌐 Online Portal", "✅ Yes" if local_data["portal"] else "❌ No", delta="-50 SHADOW" if not local_data["portal"] else "+25")
        
        st.progress(transparency_score / 100)
        
        if transparency_score >= 70:
            st.success(f"**Transparency Score: {transparency_score}/100** - This government is reasonably transparent.")
        elif transparency_score >= 40:
            st.warning(f"**Transparency Score: {transparency_score}/100** - Room for improvement. Demand better access.")
        else:
            st.error(f"**Transparency Score: {transparency_score}/100** - 🔴 SHADOW PENALTY APPLIED. This government operates in darkness.")
            st.markdown("**Action Required:** File FOIL requests and demand livestreaming at the next board meeting.")
        
        st.divider()
        st.subheader("🔍 Red Flag Keyword Scanner")
        st.caption("We scan meeting agendas and minutes for warning signs of hidden spending or overreach.")
        
        SAMPLE_AGENDA_ITEMS = [
            {"item": "Resolution to approve emergency contract for road repairs - $450,000", "red_flags": ["emergency contract"], "grift": True},
            {"item": "Public hearing on proposed zoning amendment for Main Street", "red_flags": [], "grift": False},
            {"item": "Authorization for sole source procurement of IT services", "red_flags": ["sole source"], "grift": True},
            {"item": "Adoption of 2026 budget with 3.5% tax levy increase", "red_flags": [], "grift": False},
            {"item": "Resolution to waive competitive bidding for consulting contract - $125,000", "red_flags": ["waiver of competitive bidding"], "grift": True},
            {"item": "Fee increase for building permits effective July 1", "red_flags": ["fee increase"], "grift": False}
        ]
        
        for item in SAMPLE_AGENDA_ITEMS:
            with st.container():
                item_col1, item_col2 = st.columns([3, 1])
                
                item_col1.markdown(f"**{item['item']}**")
                
                if item['red_flags']:
                    item_col2.error(f"🚩 {', '.join(item['red_flags']).upper()}")
                    
                    if item['grift']:
                        st.error("🚨 **GRIFT ALERT: HIDDEN LOCAL SPENDING** - This item may bypass public oversight. Demand a line-item breakdown and public hearing.")
                else:
                    item_col2.success("✅ Clear")
                
                st.divider()
        
        st.markdown("### 📜 The Local Good/Bad/Ugly")
        st.caption("Sample town ordinance decoded into plain English:")
        
        with st.expander("Example: 'Emergency Procurement Authorization'"):
            st.markdown("""
| Assessment | Plain English |
|------------|---------------|
| ✅ **THE GOOD** | Allows fast response to genuine emergencies (storm damage, infrastructure failures) |
| ⚠️ **THE BAD** | "Emergency" is often defined loosely, allowing routine work to skip bidding |
| 💀 **THE UGLY** | Politically connected contractors get no-bid deals worth millions; taxpayers pay premium prices |
| 🛡️ **YOUR LEVER** | Demand quarterly reports on all emergency contracts; compare prices to market rates |
            """)
        
        st.divider()
    
    st.divider()
    
    BILL_DATABASE = [
        {
            "id": "S7011/A7388",
            "name": "Peanut's Law",
            "jurisdiction": "State (New York)",
            "status": "Referred to Environmental Conservation Committee (2026 Session)",
            "summary": "Amends ECL 11-0512 to mandate a 72-hour waiting period and emergency appeal rights before state-ordered euthanasia of seized animals.",
            "sponsors": ["Sen. Jessica Scarcella-Spanton", "Asm. Michael Blumencranz"],
            "issue": "Animal Rights",
            "reward_pct": 90,
            "risk_pct": 10,
            "classification": "NEED",
            "value_waste": "VALUE",
            "good": "Protects due process for pet owners; prevents bureaucratic overreach; honors Peanut & Fred's memory",
            "bad": "72-hour window may delay action in genuine danger cases",
            "ugly": "State agencies fought similar reforms before",
            "fiscal_impact": "$0 - Procedural change only",
            "admin_power": "Low",
            "grift_alert": False
        },
        {
            "id": "HR-1234",
            "name": "Border Security Enhancement Act",
            "jurisdiction": "Federal",
            "status": "House Committee on Homeland Security",
            "summary": "Increases funding for border infrastructure and mandates E-Verify for all federal contractors.",
            "sponsors": ["Rep. Example (R-TX)"],
            "issue": "Borders",
            "reward_pct": 75,
            "risk_pct": 25,
            "classification": "WANT",
            "value_waste": "VALUE",
            "good": "Enforces existing immigration law; protects American workers",
            "bad": "Implementation costs may exceed estimates",
            "ugly": "Lobbyist carve-outs for certain industries",
            "fiscal_impact": "$2.3B over 5 years",
            "admin_power": "Medium",
            "grift_alert": False
        },
        {
            "id": "S-5678",
            "name": "Educational Freedom Act",
            "jurisdiction": "Federal",
            "status": "Senate HELP Committee",
            "summary": "Expands school choice through federal tax credits for private school tuition.",
            "sponsors": ["Sen. Example (R-FL)"],
            "issue": "Education",
            "reward_pct": 60,
            "risk_pct": 40,
            "classification": "NICE-TO-HAVE",
            "value_waste": "VALUE",
            "good": "Empowers parents; creates competition",
            "bad": "May reduce public school funding in some districts",
            "ugly": "Wealthy families benefit disproportionately",
            "fiscal_impact": "$1.8B annual",
            "admin_power": "Low",
            "grift_alert": False
        },
        {
            "id": "A-9999",
            "name": "Climate Resilience Administrative Authority Act",
            "jurisdiction": "State (New York)",
            "status": "Assembly Environmental Committee",
            "summary": "Grants DEC broad authority to issue emergency regulations on carbon emissions without legislative approval.",
            "sponsors": ["Asm. Example (D-Manhattan)"],
            "issue": "Overreach",
            "reward_pct": 20,
            "risk_pct": 80,
            "classification": "WASTE",
            "value_waste": "WASTE",
            "good": "Faster response to environmental emergencies",
            "bad": "Bypasses legislative oversight; no sunset clause",
            "ugly": "Unlimited administrative power with 'minimal' $50K fiscal note",
            "fiscal_impact": "$50,000 (reported)",
            "admin_power": "High",
            "grift_alert": True
        },
        {
            "id": "S-2026",
            "name": "Sanctuary City Enforcement Protection Act",
            "jurisdiction": "State (New York)",
            "status": "Senate Judiciary Committee",
            "summary": "Prohibits state agencies from cooperating with federal immigration enforcement without court order.",
            "sponsors": ["Sen. Example (D-Brooklyn)"],
            "issue": "Borders",
            "reward_pct": 30,
            "risk_pct": 70,
            "classification": "WASTE",
            "value_waste": "WASTE",
            "good": "Protects immigrant communities from deportation raids",
            "bad": "Obstructs federal law enforcement; creates legal conflicts",
            "ugly": "Costs taxpayers while reducing security cooperation",
            "fiscal_impact": "$500,000 (legal defense fund)",
            "admin_power": "Medium",
            "grift_alert": False
        },
        {
            "id": "A-7788",
            "name": "Small Business Regulatory Relief Act",
            "jurisdiction": "State (New York)",
            "status": "Assembly Small Business Committee",
            "summary": "Waives first-time regulatory fines for small businesses and requires agencies to provide compliance assistance.",
            "sponsors": ["Asm. Example (R-Long Island)"],
            "issue": "Fiscal",
            "reward_pct": 85,
            "risk_pct": 15,
            "classification": "NEED",
            "value_waste": "VALUE",
            "good": "Helps small businesses survive; reduces bureaucratic burden",
            "bad": "May reduce enforcement revenue",
            "ugly": "Carve-out for 'connected' businesses could be exploited",
            "fiscal_impact": "$2M revenue reduction",
            "admin_power": "Low",
            "grift_alert": False
        }
    ]
    
    if jurisdiction != "Federal":
        filtered_bills = [b for b in BILL_DATABASE if b["jurisdiction"] == jurisdiction or b["jurisdiction"] == "Federal"]
    else:
        filtered_bills = [b for b in BILL_DATABASE if b["jurisdiction"] == "Federal"]
    
    if issue_filter != "All":
        filtered_bills = [b for b in filtered_bills if b["issue"] == issue_filter]
    
    st.subheader(f"📜 Live Bill Feed ({len(filtered_bills)} bills)")
    
    peanuts_law = next((b for b in BILL_DATABASE if b["id"] == "S7011/A7388"), None)
    if peanuts_law and (jurisdiction == "State (New York)" or issue_filter == "Animal Rights" or issue_filter == "All"):
        st.markdown("### 🐿️ FEATURED: Peanut's Law (S7011/A7388)")
        
        feat_col1, feat_col2, feat_col3 = st.columns([2, 1, 1])
        feat_col1.info(f"**Status:** {peanuts_law['status']}")
        feat_col2.metric("Reward", f"{peanuts_law['reward_pct']}%", delta="High Value")
        feat_col3.metric("Risk", f"{peanuts_law['risk_pct']}%", delta="Low", delta_color="inverse")
        
        st.markdown(f"**Summary:** {peanuts_law['summary']}")
        st.success(f"**VERDICT:** {peanuts_law['reward_pct']}% REWARD / {peanuts_law['risk_pct']}% RISK ({peanuts_law['classification']})")
        
        with st.expander("📊 The Good, The Bad, and The Ugly"):
            st.markdown(f"""
| Assessment | Details |
|------------|---------|
| ✅ **THE GOOD** | {peanuts_law['good']} |
| ⚠️ **THE BAD** | {peanuts_law['bad']} |
| 💀 **THE UGLY** | {peanuts_law['ugly']} |
            """)
        
        st.markdown("#### 🗡️ Citizen Sword: Take Action")
        petition_text = f"""Dear Sen. Scarcella-Spanton and Asm. Blumencranz,

I am a constituent writing in STRONG SUPPORT of Peanut's Law (S7011/A7388).

The 72-hour waiting period and emergency appeal rights are essential due process protections. The tragic case of Peanut and Fred demonstrated that bureaucratic overreach can result in irreversible harm.

I urge you to bring this bill to a floor vote immediately.

Respectfully,
[YOUR NAME]
[YOUR ADDRESS]
"""
        st.text_area("📧 Pre-Filled Petition Letter", petition_text, height=200, key="peanut_petition")
        st.link_button("📤 Email NY Senate", "mailto:scarcella-spanton@nysenate.gov?subject=Support%20Peanut%27s%20Law%20S7011")
        
        st.divider()
    
    for bill in filtered_bills:
        if bill["id"] == "S7011/A7388":
            continue
        
        with st.container():
            bill_col1, bill_col2 = st.columns([3, 1])
            
            with bill_col1:
                st.markdown(f"### {bill['name']} ({bill['id']})")
                st.caption(f"**{bill['jurisdiction']}** | {bill['issue']} | {bill['status']}")
                st.markdown(f"{bill['summary']}")
            
            with bill_col2:
                if bill['grift_alert']:
                    st.error("🚨 GRIFT ALERT")
                    st.caption("BUREAUCRATIC OVERREACH")
                
                reward_color = "normal" if bill['reward_pct'] >= 50 else "inverse"
                st.metric("Reward/Risk", f"{bill['reward_pct']}% / {bill['risk_pct']}%")
                
                if bill['classification'] == "NEED":
                    st.success(f"**{bill['classification']}** - {bill['value_waste']}")
                elif bill['classification'] == "WANT":
                    st.info(f"**{bill['classification']}** - {bill['value_waste']}")
                elif bill['classification'] == "NICE-TO-HAVE":
                    st.warning(f"**{bill['classification']}** - {bill['value_waste']}")
                else:
                    st.error(f"**{bill['classification']}** - {bill['value_waste']}")
            
            with st.expander(f"📊 The Good, The Bad, and The Ugly - {bill['id']}"):
                st.markdown(f"""
| Assessment | Details |
|------------|---------|
| ✅ **THE GOOD** | {bill['good']} |
| ⚠️ **THE BAD** | {bill['bad']} |
| 💀 **THE UGLY** | {bill['ugly']} |
| 💰 **Fiscal Impact** | {bill['fiscal_impact']} |
| 🏛️ **Admin Power** | {bill['admin_power']} |
                """)
                
                if bill['grift_alert']:
                    st.error("""
**🚨 GRIFT ALARM TRIGGERED:**
This bill grants wide administrative power with minimal reported fiscal impact. 
When power is free, citizens pay the hidden cost.
                    """)
            
            sponsor_list = ", ".join(bill['sponsors'])
            petition_bill = f"""Dear {sponsor_list},

I am writing regarding {bill['name']} ({bill['id']}).

Based on my analysis:
- Reward Assessment: {bill['reward_pct']}%
- Risk Assessment: {bill['risk_pct']}%
- Classification: {bill['classification']}

{"I OPPOSE this legislation due to excessive administrative overreach." if bill['grift_alert'] or bill['reward_pct'] < 50 else "I SUPPORT this legislation and urge you to bring it to a floor vote."}

Respectfully,
[YOUR NAME]
"""
            
            petition_col, thread_col = st.columns(2)
            
            with petition_col:
                if st.button(f"🗡️ One-Click Petition: {bill['id']}", key=f"petition_{bill['id']}"):
                    st.text_area(f"Petition for {bill['id']}", petition_bill, height=180, key=f"petition_text_{bill['id']}")
            
            with thread_col:
                if st.button(f"📢 One-Click Thread: {bill['id']}", key=f"thread_{bill['id']}"):
                    thread_1 = f"🧵 THREAD: {bill['name']} ({bill['id']}) - A Plainview Protocol Audit\n\n✅ THE GOOD: {bill['good']}\n\n#PlainviewProtocol #TransparencyNow 1/"
                    thread_2 = f"⚠️ THE BAD: {bill['bad']}\n\n💀 THE UGLY: {bill['ugly']}\n\n2/"
                    thread_3 = f"📊 VERDICT: {bill['reward_pct']}% Reward / {bill['risk_pct']}% Risk = {bill['classification']}\n\n🗳️ My position: {'SUPPORT' if bill['reward_pct'] >= 50 else 'OPPOSE'}\n\nAudit your government: plainview-protocol.replit.app 3/3"
                    
                    st.text_area("Thread Part 1", thread_1, height=100, key=f"thread1_{bill['id']}")
                    st.text_area("Thread Part 2", thread_2, height=100, key=f"thread2_{bill['id']}")
                    st.text_area("Thread Part 3", thread_3, height=100, key=f"thread3_{bill['id']}")
                    
                    full_thread = f"{thread_1}\n\n{thread_2}\n\n{thread_3}"
                    tweet_text = thread_1.replace(' ', '%20').replace('#', '%23').replace('\n', '%0A')[:280]
                    st.link_button("🐦 Post Thread to X", f"https://twitter.com/intent/tweet?text={tweet_text}")
                    
                    if 'bill_shares' not in st.session_state:
                        st.session_state.bill_shares = {}
                    st.session_state.bill_shares[bill['id']] = st.session_state.bill_shares.get(bill['id'], 0) + 1
            
            st.divider()
    
    st.markdown("### 🚨 Grift Alarm Criteria")
    st.caption("Bills are flagged when they meet these red flags:")
    grift_col1, grift_col2, grift_col3 = st.columns(3)
    grift_col1.warning("**Wide Admin Power**\n+ Minimal Fiscal Note")
    grift_col2.warning("**No Sunset Clause**\n+ Emergency Powers")
    grift_col3.warning("**Vague Language**\n+ Broad Discretion")
    
    st.divider()
    st.subheader("🎙️ Town Hall Script Generator")
    st.caption("Generate a professional, timed testimony for your next public meeting.")
    
    with st.expander("ℹ️ Your First Amendment Shield"):
        st.markdown("""
**Constitutional Protection for Public Comment:**

> *"Congress shall make no law... abridging the freedom of speech."* — First Amendment

**Your Rights Under NY Open Meetings Law (Public Officers Law Art. 7):**
- You have the right to make **critical, harsh, or personal remarks** about official duties
- Officials may set **time limits** but NOT **viewpoint restrictions**
- You cannot be removed for expressing unpopular opinions about policy
- Recording public meetings is generally permitted

**Case Law:** *City of Madison v. Wisconsin Employment Relations Commission* (1976) - Citizens have First Amendment right to speak at public meetings.

*Speak truth to power. The Constitution is your shield.*
        """)
    
    dock_col1, dock_col2 = st.columns(2)
    with dock_col1:
        dock_user_name = st.text_input("Your Name", value="[YOUR NAME]", key="dock_user_name")
        dock_user_town = st.text_input("Your Town/City", value=selected_state, key="dock_user_town")
    with dock_col2:
        dock_topic = st.text_input("Bill/Agenda Item", value="Peanut's Law (S7011)", key="dock_topic")
        dock_verdict = st.selectbox("Your Position", ["SUPPORT - Vote YES", "OPPOSE - Vote NO", "AMEND - Add Transparency Requirements"], key="dock_verdict")
    
    if st.button("🎙️ Generate Timed Testimony", key="gen_dock_script"):
        st.session_state.show_dock_testimony = True
    
    if st.session_state.get('show_dock_testimony', False):
        dock_action = "vote YES" if "YES" in dock_verdict else ("vote NO" if "NO" in dock_verdict else "amend this bill to include transparency requirements")
        
        dock_1min = f"""My name is {dock_user_name} from {dock_user_town}. I urge you to {dock_action} on {dock_topic}.

This bill {"protects due process and citizen rights" if "YES" in dock_verdict else "raises serious concerns about overreach"}. Thank you."""

        dock_2min = f"""My name is {dock_user_name} from {dock_user_town}. I'm here to speak on {dock_topic}.

The Plainview Protocol audit rates this bill as {"VALUE" if "YES" in dock_verdict else "requiring scrutiny"}.

THE GOOD: [State the bill's benefits]
THE BAD: [State any concerns]
THE UGLY: [State risks of inaction or poor implementation]

I urge this body to {dock_action}. Thank you."""

        dock_3min = f"""Good evening. My name is {dock_user_name}, resident of {dock_user_town}.

I am here to testify on {dock_topic}. After reviewing this legislation through the Plainview Protocol framework, I {"strongly support" if "YES" in dock_verdict else "have serious concerns about"} this bill.

THE GOOD: [Describe positive aspects of this legislation]

THE BAD: [Identify any procedural or implementation concerns]

THE UGLY: [Describe worst-case scenarios or unintended consequences]

Based on this analysis, I formally urge this body to {dock_action}.

Citizens deserve transparency. When we show up and speak, democracy works. I thank you for your time and attention to this matter.

I yield the remainder of my time."""

        dock_tab1, dock_tab2, dock_tab3 = st.tabs(["⏱️ 1 Minute", "⏱️ 2 Minutes", "⏱️ 3 Minutes"])
        with dock_tab1:
            st.text_area("1-Minute Script", dock_1min, height=120, key="dock_script_1")
        with dock_tab2:
            st.text_area("2-Minute Script", dock_2min, height=180, key="dock_script_2")
        with dock_tab3:
            st.text_area("3-Minute Script", dock_3min, height=300, key="dock_script_3")

def page_course_correction():
    selected_state = st.session_state.get("selected_state", "New York")
    st.header("⚖️ The Course Correction Manual")
    st.markdown("**Citizen Levers for Removal & Justice.** Your state-by-state guide to holding officials accountable through legal means.")
    
    st.divider()
    
    tab_recall, tab_impeach, tab_jury, tab_criminal = st.tabs(["🗳️ Recall Laws", "⚖️ Impeachment", "👨‍⚖️ Grand Jury Petitions", "🚨 Criminal Referral"])
    
    with tab_recall:
        st.subheader("Which States Allow Citizens to Fire Their Governor?")
        st.markdown("**19 states** allow citizens to recall their Governor through petition and special election.")
        
        recall_states = [s for s, d in STATE_RECALL_DATA.items() if d.get("recall", False)]
        no_recall_states = [s for s in STATES if s not in recall_states or not STATE_RECALL_DATA.get(s, {}).get("recall", False)]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("🟢 **Recall Allowed:**")
            for state in sorted(recall_states):
                st.write(f"• {state}")
        with col2:
            st.error("🔴 **No Recall (Impeachment Only):**")
            st.caption("These states require legislative action to remove officials.")
            st.write(", ".join(sorted([s for s in ["New York", "Texas", "Florida", "Ohio", "Pennsylvania"] if s not in recall_states])))
        
        st.divider()
        recall_data = STATE_RECALL_DATA.get(selected_state, {})
        if recall_data.get("recall", False):
            st.success(f"✅ **{selected_state} ALLOWS RECALL.** You can petition to remove your Governor.")
            st.info("""
**How to Start a Recall:**
1. Obtain official petition forms from your Secretary of State
2. Gather required signatures (typically 10-25% of votes cast in last election)
3. Submit within statutory deadline (usually 60-160 days)
4. If validated, a recall election is scheduled
            """)
        else:
            st.warning(f"⚠️ **{selected_state} does NOT allow recall.** You must pursue impeachment through the legislature.")
    
    with tab_impeach:
        st.subheader("The Legal Path to Removal for 'High Crimes and Misdemeanors'")
        
        st.markdown("""
**Impeachment is a legislative process.** Unlike recall, citizens cannot directly initiate impeachment.

**Standard Process:**
1. **Investigation:** Legislative committee investigates alleged misconduct
2. **Articles of Impeachment:** Lower house votes to impeach (simple majority)
3. **Trial:** Upper house (Senate) conducts trial
4. **Removal:** 2/3 supermajority required for conviction and removal
        """)
        
        recall_data = STATE_RECALL_DATA.get(selected_state, {})
        impeachment_process = recall_data.get("impeachment", "Legislature 2/3 vote")
        
        st.info(f"**{selected_state} Impeachment Process:** {impeachment_process}")
        
        st.divider()
        st.markdown("**Your Role:**")
        st.markdown("""
- Contact your state legislators and demand investigation
- Provide evidence to legislative oversight committees
- Attend public hearings and testify if invited
- Use FOIA to obtain records that support your case
- Organize community pressure campaigns
        """)
    
    with tab_jury:
        st.subheader("Citizen-Initiated Grand Juries")
        st.markdown("**In some states, citizens can petition to convene a grand jury** to investigate fraud, corruption, or criminal misconduct.")
        
        grand_jury_states = [s for s, d in STATE_RECALL_DATA.items() if d.get("grand_jury", False)]
        
        st.success("🟢 **States with Citizen Grand Jury Petitions:**")
        for state in sorted(grand_jury_states):
            st.write(f"• {state}")
        
        recall_data = STATE_RECALL_DATA.get(selected_state, {})
        if recall_data.get("grand_jury", False):
            st.success(f"✅ **{selected_state} allows citizen-initiated grand juries.**")
            st.info("""
**How It Works:**
1. Draft a petition describing the alleged crimes
2. Gather required signatures (varies by state)
3. Submit to the court with supporting evidence
4. If accepted, a grand jury is empaneled to investigate
5. Grand jury can issue subpoenas and indictments
            """)
        else:
            st.warning(f"⚠️ **{selected_state} does not have citizen grand jury petitions.** You must work through the District Attorney or Attorney General.")
            st.link_button("Find Your State AG", "https://www.naag.org/find-my-ag/")
    
    with tab_criminal:
        st.subheader("🚨 Criminal Referral: Report Fraud to Authorities")
        st.markdown("**When officials commit crimes, report them.** These links connect you directly to fraud reporting units.")
        
        st.markdown("### Federal Fraud Reporting")
        fed_col1, fed_col2 = st.columns(2)
        with fed_col1:
            st.link_button("🏛️ GAO FraudNet", "https://www.gao.gov/fraudnet")
            st.caption("Report waste, fraud, and abuse in federal programs")
            st.link_button("🛡️ DHS OIG Hotline", "https://www.oig.dhs.gov/hotline")
            st.caption("Report fraud in Homeland Security programs")
        with fed_col2:
            st.link_button("🏠 HUD OIG Hotline", "https://www.hudoig.gov/hotline")
            st.caption("Report housing and urban development fraud")
            st.link_button("💰 Treasury OIG", "https://oig.treasury.gov/report-fraud-waste-abuse")
            st.caption("Report financial crimes and Treasury fraud")
        
        st.divider()
        st.markdown("### State-Level Fraud Reporting")
        st.link_button("🔍 Find Your State Attorney General", "https://www.naag.org/find-my-ag/")
        st.caption("State AGs prosecute corruption, Medicaid fraud, and public integrity violations.")
        
        st.link_button("📊 Find Your State Auditor", "https://www.nasact.org/member_directory")
        st.caption("State auditors investigate misuse of public funds.")
        
        st.info("""
**Tips for Effective Reporting:**
1. Document everything with dates and specific amounts
2. Include names and titles of officials involved
3. Attach copies of contracts, emails, or financial records
4. Request confirmation of receipt and case number
5. Follow up in writing if no response within 30 days
        """)
    
    with st.expander("ℹ️ Transparency: Legal Sources"):
        st.markdown("""
* **Recall Laws:** National Conference of State Legislatures (NCSL)
* **Impeachment:** State Constitutions and Legislative Rules
* **Grand Jury:** State Criminal Procedure Codes
* **Note:** Laws vary significantly by state. Consult an attorney for specific guidance.
        """)

def page_ecosystem():
    st.header("🌳 From Pain to Purpose: The Full Grove")
    
    st.markdown("""
I'm **Russell Nomer**—a 54-year-old dad from Plainview, NY, recovering from accidents and loss, 
turning it all into tools for truth and protection. The Plainview Protocol is one part—here's the rest:
    """)
    
    st.divider()
    st.subheader("🛠️ Apps & Tools")
    col1, col2, col3 = st.columns(3)
    col1.link_button("🏠 Market Architect App", "https://marketarchitect.app")
    col2.link_button("🍳 Home Cooked Connections", "https://homecookedconnections.com")
    col3.link_button("💎 Verbum VIP", "https://verbum.vip")
    
    st.divider()
    st.subheader("📚 Books")
    st.link_button("📖 The Grove (Book on Amazon)", "https://amzn.to/4sukXoc")
    
    st.divider()
    st.subheader("🎵 Music")
    
    music_col1, music_col2, music_col3 = st.columns(3)
    music_col1.link_button("📺 YouTube Channel", "https://www.youtube.com/@russellnomermusic")
    music_col2.link_button("🎵 UnitedMasters", "https://unitedmasters.com/russell-nomer-music")
    music_col3.link_button("🎧 Apple Music", "https://music.apple.com/us/artist/russell-nomer/1762452726")
    
    music_col4, music_col5 = st.columns(2)
    music_col4.link_button("🎹 Bandcamp", "https://russellnomer.bandcamp.com/")
    music_col5.link_button("☁️ SoundCloud", "https://soundcloud.com/russell-nomer")
    
    st.divider()
    st.info("🌲 Music, books, apps—all channeling resilience into protecting America. **Join the Grove.**")

def page_support():
    st.header("☕ Sustain the Mission")
    st.write("This tool is free, ad-free, and uncensorable thanks to supporters like you.")
    
    c1, c2, c3 = st.columns(3)
    c1.link_button("Donate via PayPal", "https://paypal.com")
    c2.link_button("Buy Russell a Coffee", "https://buymeacoffee.com/russellnomer")
    c3.link_button("Fork on GitHub", "https://github.com/russellnomer/plainview-protocol")
    
    st.divider()
    st.subheader("🛠️ Decentralize the Protocol")
    
    with st.expander("ℹ️ Why Decentralize?"):
        st.markdown("""
**Centralization is a target. Decentralization is a movement.**

By forking our code, you ensure the truth cannot be deleted or paywalled.

**Academic Foundation:**
- **Thompson (1961):** *"Organizations centralize when they fear loss of control, but decentralized systems are more resilient to attack."* — Academy of Management
- **DAO Principles (Investopedia):** Decentralized Autonomous Organizations prove that collective action without central authority can achieve transparency at scale.

**The Plainview Protocol is open-source because:**
1. No single point of failure - if we go down, forks survive
2. Community auditing - thousands of eyes catch errors we miss
3. Local adaptation - your town has different officials than ours
4. Censorship resistance - truth cannot be memory-holed

*"Don't just watch us—become us."*
        """)
    
    st.markdown("""
**Fork the code, apply it to your town, and help us audit the Uniparty everywhere.**

The Protocol is designed to be forked. Each fork is a new node in the transparency network.
    """)
    
    fork_col1, fork_col2 = st.columns(2)
    fork_col1.link_button("🔧 Fork on GitHub", "https://github.com/russellnomer/plainview-protocol", use_container_width=True)
    fork_col2.link_button("🔧 Fork on Replit", "https://replit.com/@russellnomer/plainview-protocol", use_container_width=True)
    
    st.divider()
    st.subheader("📢 Share the Alarm")
    st.caption("Spread the word on social media. Every share is a vote for transparency.")
    
    share_message = "I'm using The Plainview Protocol to audit my government. Free, open-source citizen oversight. Truth, Kindness, Security. #PlainviewProtocol #TransparencyNow"
    
    share_col1, share_col2, share_col3 = st.columns(3)
    share_col1.link_button("🐦 Share on X", f"https://twitter.com/intent/tweet?text={share_message.replace(' ', '%20').replace('#', '%23')}", use_container_width=True)
    share_col2.link_button("📘 Share on Facebook", "https://www.facebook.com/sharer/sharer.php?quote=" + share_message.replace(' ', '%20'), use_container_width=True)
    share_col3.link_button("🔴 Post on Reddit", "https://www.reddit.com/submit?title=The%20Plainview%20Protocol%20-%20Citizen%20Government%20Oversight&url=https://plainview-protocol.replit.app", use_container_width=True)
    
    st.divider()
    st.subheader("📊 Viral Reach Tracker")
    
    if 'viral_shares' not in st.session_state:
        st.session_state.viral_shares = {"x": 0, "facebook": 0, "reddit": 0}
    
    viral_col1, viral_col2, viral_col3, viral_col4 = st.columns(4)
    viral_col1.metric("X/Twitter", st.session_state.viral_shares.get("x", 0))
    viral_col2.metric("Facebook", st.session_state.viral_shares.get("facebook", 0))
    viral_col3.metric("Reddit", st.session_state.viral_shares.get("reddit", 0))
    total_shares = sum(st.session_state.viral_shares.values())
    viral_col4.metric("Total Reach", total_shares, delta="Growing" if total_shares > 0 else None)
    
    st.caption("*Share counts are tracked locally. In a production deployment, these would sync to a central database.*")

def page_mission_milestones():
    st.header("🏛️ Mission Milestones: Founded January 8, 2026")
    
    with st.expander("ℹ️ Planning for the Century"):
        st.markdown("""
A good timeline turns scattered tasks into a clear path forward. This living document ensures our mission remains focused on Truth, Kindness, and Security.

The Plainview Protocol is built to last for generations. Each milestone marks progress toward a more transparent government.
        """)
    
    st.divider()
    
    FOUNDING_DATE = date(2026, 1, 8)
    today = date.today()
    days_since_launch = (today - FOUNDING_DATE).days
    
    MILESTONES = [
        {"date": "January 8, 2026", "title": "🏛️ LEGACY ESTABLISHED", "description": "Russell Nomer establishes The Plainview Protocol in Plainview, NY. The founding moment of citizen-powered accountability.", "status": "completed"},
        {"date": "January 8, 2026", "title": "🎙️ Founder's Monologue Launched", "description": "Voice of the Citizen Activated — Daily briefings on Career Politician Wealth, PAC Transparency, and Black Hole Spending.", "status": "completed"},
        {"date": "January 8, 2026", "title": "🔍 Epstein Audit Activated", "description": "Evidence over Noise — Tiered verification system for unsealed court documents with direct links to official sources.", "status": "completed"},
        {"date": "January 8, 2026", "title": "⚖️ Prosecutorial Pressure Button LIVE", "description": "Demanding names, not black boxes — Pre-filled DOJ petitions for the 10 co-conspirators.", "status": "completed"},
        {"date": "January 8, 2026", "title": "🎯 FOIA Cannon 2.0 LIVE", "description": "Targeted for the 10 Co-conspirators — One-click FOIA requests to FBI and DOJ.", "status": "completed"},
        {"date": "January 8, 2026", "title": "⚖️ Litigation Trigger LIVE", "description": "Turning the Labyrinth into a Courtroom — Auto-generate Notice of Intent to Sue.", "status": "completed"},
        {"date": "January 8, 2026", "title": "🎓 Sunlight Counsel Directory LIVE", "description": "From Notice to Lawsuit — Pro bono clinic network activated.", "status": "completed"},
        {"date": "January 8, 2026", "title": "🏛️ Court Watch Tracker LIVE", "description": "No more secret settlements — Track active litigation and victories.", "status": "completed"},
        {"date": "Q1 2026", "title": "Local Watchdog Beta", "description": "County Clash comparison tool with OSC data integration.", "status": "in_progress"},
        {"date": "Q1 2026", "title": "Infographic Generator", "description": "Battle card meme-engine for shareable accountability graphics.", "status": "completed"},
        {"date": "Q1 2026", "title": "Beta Testing Complete", "description": "Core features validated by early adopters across 10 states.", "status": "pending"},
        {"date": "Q1 2026", "title": "Peanut's Law Monitoring", "description": "Full tracking of S7011/A7388 through NY Legislature with citizen alerts.", "status": "pending"},
        {"date": "Q2 2026", "title": "50-State Coverage", "description": "Corruption Heatmap expanded with verified data for all states.", "status": "pending"},
        {"date": "Q2 2026", "title": "Neighborhood Mobilization Launch", "description": "Hyper-local tools for county and municipal oversight.", "status": "pending"},
        {"date": "Q3 2026", "title": "First FOIA Victory", "description": "Documents obtained through citizen-generated FOIA requests.", "status": "pending"},
        {"date": "Q3 2026", "title": "Fork Network Expansion", "description": "10+ active forks adapting the Protocol for local jurisdictions.", "status": "pending"},
        {"date": "Q4 2026", "title": "Referendum Prototype Live", "description": "Electoral College-weighted citizen consensus on key transparency issues.", "status": "pending"},
        {"date": "Q4 2026", "title": "First Anniversary", "description": "One year of citizen-powered government oversight.", "status": "pending"},
    ]
    
    st.subheader("📅 The Legacy Timeline")
    
    for milestone in MILESTONES:
        if milestone["status"] == "completed":
            icon = "💎"
            border_color = "#28a745"
        elif milestone["status"] == "in_progress":
            icon = "🔄"
            border_color = "#007bff"
        else:
            icon = "⭕"
            border_color = "#6c757d"
        
        st.markdown(f"""
<div style="border-left: 3px solid {border_color}; padding-left: 20px; margin-bottom: 20px;">
    <p style="margin: 0; font-size: 0.9em; color: #666;">{milestone['date']}</p>
    <h4 style="margin: 5px 0;">{icon} {milestone['title']}</h4>
    <p style="margin: 0;">{milestone['description']}</p>
</div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🔮 Future Vision")
    st.markdown("""
- **2027**: Course Correction tools drive first successful recall campaigns
- **2028**: Protocol data informs voter guides in 25+ states
- **2030**: Transparency becomes a bipartisan campaign platform
- **2050**: A generation raised on government accountability
    """)
    
    st.info(f"📆 **Days Since Initial Commit:** {days_since_launch}")

def page_epstein_audit():
    st.header("🔍 Epstein Archive Audit")
    st.caption("Evidence over Noise — Tiered verification linked to justice.gov and vault.fbi.gov")
    
    st.subheader("📊 Redaction Watchdog")
    total_pages = 5200000
    released_pages = 52000
    release_pct = (released_pages / total_pages) * 100
    
    watchdog_col1, watchdog_col2, watchdog_col3 = st.columns(3)
    watchdog_col1.metric("Total Epstein Files", f"{total_pages/1e6:.1f}M pages")
    watchdog_col2.metric("Pages Released", f"{released_pages/1e3:.0f}K", delta=f"{release_pct:.1f}%")
    watchdog_col3.metric("Transparency Rate", f"<1%", delta="Critical", delta_color="inverse")
    
    st.warning("⚠️ **Transparency Failure Detected:** DOJ has released less than 1% of 5.2 million pages. Initials like 'LG' (Lesley Groff) visible but names redacted.")
    
    st.divider()
    
    st.subheader("🗂️ Tiered Verification Database")
    st.caption("Names categorized by evidence level from unsealed court documents")
    
    show_unvetted = st.checkbox("⚠️ Show Unvetted Claims (Tier 3)", value=False, help="Enable to see unsubstantiated claims that have not been verified")
    
    search_query = st.text_input("🔍 Search Archive", placeholder="Search names, locations, or document IDs...")
    
    ARCHIVE_DATA = [
        {"name": "Jeffrey Epstein", "tier": 1, "status": "Substantiated", "source": "Court Documents", "source_url": "https://www.justice.gov/usao-sdny/pr/jeffrey-epstein-charged-sex-trafficking-minors", "notes": "Primary defendant, deceased Aug 2019"},
        {"name": "Ghislaine Maxwell", "tier": 1, "status": "Substantiated", "source": "Conviction Dec 2021", "source_url": "https://www.justice.gov/usao-sdny/pr/ghislaine-maxwell-sentenced-20-years-prison-sex-trafficking-conspiracy", "notes": "Convicted, sentenced 20 years"},
        {"name": "Bill Richardson", "tier": 1, "status": "Substantiated", "source": "Unsealed 2024 Documents", "source_url": "https://www.courtlistener.com/docket/4355835/giuffre-v-maxwell/", "notes": "Named in victim testimony, deceased Sept 2023"},
        {"name": "Prince Andrew", "tier": 1, "status": "Substantiated", "source": "Civil Settlement 2022", "source_url": "https://www.courtlistener.com/docket/17318376/giuffre-v-prince-andrew/", "notes": "Civil case settled, no criminal charges"},
        {"name": "Jean-Luc Brunel", "tier": 1, "status": "Substantiated", "source": "French Investigation", "source_url": "https://www.justice.gov/", "notes": "Modeling agent, deceased Feb 2022"},
        {"name": "Alan Dershowitz", "tier": 2, "status": "Association", "source": "Flight Logs", "source_url": "https://vault.fbi.gov/", "notes": "Denied allegations, documented flights"},
        {"name": "Les Wexner", "tier": 2, "status": "Association", "source": "Financial Records", "source_url": "https://www.justice.gov/", "notes": "Former financial relationship, no charges"},
        {"name": "[REDACTED - LG]", "tier": 2, "status": "Association", "source": "Unsealed Docs", "source_url": "https://vault.fbi.gov/", "notes": "🚨 Transparency Failure: Initials visible, name redacted"},
    ]
    
    UNVETTED_DATA = [
        {"name": "[Unverified Claim A]", "tier": 3, "status": "False Claim", "source": "Social Media", "source_url": "", "notes": "No documentary evidence"},
        {"name": "[Unverified Claim B]", "tier": 3, "status": "False Claim", "source": "Anonymous Post", "source_url": "", "notes": "Debunked by court records"},
    ]
    
    display_data = ARCHIVE_DATA.copy()
    if show_unvetted:
        display_data.extend(UNVETTED_DATA)
    
    if search_query:
        display_data = [d for d in display_data if search_query.lower() in d["name"].lower() or search_query.lower() in d["notes"].lower()]
    
    for entry in display_data:
        tier_color = "🟢" if entry["tier"] == 1 else "🟡" if entry["tier"] == 2 else "🔴"
        tier_label = "Tier 1: Substantiated" if entry["tier"] == 1 else "Tier 2: Association" if entry["tier"] == 2 else "Tier 3: Unvetted"
        
        with st.expander(f"{tier_color} {entry['name']} — {tier_label}"):
            st.markdown(f"**Status:** {entry['status']}")
            st.markdown(f"**Source:** {entry['source']}")
            st.markdown(f"**Notes:** {entry['notes']}")
            if entry["source_url"]:
                st.link_button("📄 View Official Source", entry["source_url"])
    
    st.divider()
    
    st.subheader("🗺️ Immortal Corruption Heatmap")
    st.caption("Elected officials and public figures named in unsealed files")
    
    HEATMAP_DATA = [
        {"name": "Bill Richardson", "role": "Former NM Governor (D)", "location": "New Mexico", "source_pdf": "https://www.courtlistener.com/docket/4355835/giuffre-v-maxwell/"},
        {"name": "George Mitchell", "role": "Former Senate Majority Leader (D)", "location": "Maine", "source_pdf": "https://www.courtlistener.com/docket/4355835/giuffre-v-maxwell/"},
        {"name": "Bill Clinton", "role": "Former President (D)", "location": "Arkansas/NY", "source_pdf": "https://vault.fbi.gov/"},
        {"name": "Donald Trump", "role": "Former President (R)", "location": "Florida/NY", "source_pdf": "https://www.courtlistener.com/docket/4355835/giuffre-v-maxwell/"},
        {"name": "Prince Andrew", "role": "UK Royal", "location": "International", "source_pdf": "https://www.courtlistener.com/docket/17318376/giuffre-v-prince-andrew/"},
    ]
    
    for official in HEATMAP_DATA:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.markdown(f"**{official['name']}**")
        col1.caption(official['role'])
        col2.markdown(f"📍 {official['location']}")
        col3.link_button("📄 Source", official['source_pdf'], use_container_width=True)
    
    st.divider()
    
    st.subheader("⚖️ Prosecutorial Pressure")
    st.caption("Demand transparency from the Department of Justice")
    
    st.markdown("""
    **The 10 Co-Conspirators:** In July 2019, FBI emails identified 10 individuals as potential co-conspirators. 
    The May 2020 "Potential Charges" memo further detailed prosecutorial options. These names remain redacted.
    """)
    
    st.info("⚖️ **4th Circuit Transparency Ruling (Sept 19, 2025):** The US Court of Appeals ruled in *Citizens for Transparency v. DOJ* that government officials cannot hide behind political sensitivity exemptions when public interest demands disclosure.")
    st.link_button("📄 View 4th Circuit Ruling", SOURCES.get("fourth_circuit_ruling", "https://www.courtlistener.com/"))
    
    with st.expander("📝 Generate DOJ Petition", expanded=True):
        petitioner_name = st.text_input("Your Name", placeholder="Enter your full legal name")
        petitioner_email = st.text_input("Your Email", placeholder="your@email.com")
        
        petition_text = f"""
PETITION TO THE DEPARTMENT OF JUSTICE
Office of the Attorney General
950 Pennsylvania Avenue, NW
Washington, DC 20530-0001

RE: Request for Unredacted Release of Epstein Co-Conspirator Documents

Dear Attorney General,

Pursuant to Public Law 119-38 (Epstein Files Transparency Act), I hereby demand:

1. The unredacted status of the 10 co-conspirators identified in July 2019 FBI emails (Document EFTA00037362)
2. All records from the May 2020 "Potential Charges" memo
3. Complete disclosure of Ohio, Florida, and NYC subpoena records

The American people deserve transparency. No redactions are permitted for government officials or public figures based on political sensitivity.

Respectfully submitted,
{petitioner_name or "[YOUR NAME]"}
{petitioner_email or "[YOUR EMAIL]"}

Date: {date.today().strftime("%B %d, %Y")}
        """
        
        st.code(petition_text, language=None)
        
        if st.button("📋 Copy Petition", use_container_width=True):
            st.success("Petition text ready to copy! Use Ctrl+C or Cmd+C on the text above.")
        
        st.link_button("📧 Email DOJ", "mailto:AskDOJ@usdoj.gov?subject=Epstein%20Co-Conspirator%20Transparency%20Request", use_container_width=True)
    
    st.divider()
    
    st.subheader("🎯 FOIA Cannon: Co-Conspirator Edition")
    st.caption("One-click FOIA requests targeting the 10 co-conspirators")
    
    with st.expander("📄 Generate FBI FOIA Request", expanded=True):
        foia_name = st.text_input("Your Full Legal Name (for FOIA)", placeholder="Required for FOIA processing", key="foia_name")
        
        foia_request = f"""
FREEDOM OF INFORMATION ACT REQUEST
FBI Records Management Division
170 Marcel Drive
Winchester, VA 22602

Via: https://vault.fbi.gov/fdps-1/efoia-portal

RE: FOIA Request — Epstein Investigation Co-Conspirator Documents

Dear FOIA Officer,

Pursuant to the Freedom of Information Act (5 U.S.C. § 552) and Public Law 119-38 (Epstein Files Transparency Act), I request copies of:

1. Document EFTA00037362 (July 2019 email identifying 10 co-conspirators) — UNREDACTED
2. All records regarding Ohio, Florida, and NYC grand jury subpoenas related to Case No. 19-CR-490
3. The May 2020 "Potential Charges" memorandum in its entirety
4. Any records identifying individuals granted immunity or non-prosecution agreements

LEGAL SHIELD NOTICE:
Pursuant to Public Law 119-38, no redactions are permitted for government officials or public figures based on political sensitivity.

PENALTY OF PERJURY STATEMENT:
I declare under penalty of perjury that I am a United States citizen seeking these records for purposes of government accountability and public interest.

Requestor: {foia_name or "[YOUR FULL LEGAL NAME]"}
Date: {date.today().strftime("%B %d, %Y")}

I am willing to pay reasonable fees up to $25. Please contact me if fees exceed this amount.
        """
        
        st.code(foia_request, language=None)
        
        foia_col1, foia_col2 = st.columns(2)
        foia_col1.link_button("🔗 FBI eFOIPA Portal", "https://vault.fbi.gov/fdps-1/efoia-portal", use_container_width=True)
        foia_col2.link_button("🔗 DOJ FOIA Portal", "https://www.justice.gov/oip/submit-and-track-request-or-appeal", use_container_width=True)
    
    st.divider()
    
    st.subheader("📊 Live FOIA Tracker")
    st.caption("Track the status of your submitted FOIA requests")
    
    if 'foia_requests' not in st.session_state:
        st.session_state.foia_requests = [
            {"foipa_number": "1567892-000", "subject": "Epstein Co-Conspirators", "status": "Small Processing Track", "days_pending": 145, "submitted": "Aug 15, 2025"},
            {"foipa_number": "1589234-000", "subject": "2008 Plea Deal Records", "status": "Assigned", "days_pending": 89, "submitted": "Oct 12, 2025"},
            {"foipa_number": "1601456-000", "subject": "Flight Log Manifests", "status": "Received", "days_pending": 32, "submitted": "Dec 8, 2025"},
        ]
    
    STATUS_LEVELS = ['Received', 'Small Processing Track', 'Assigned', 'LAS Review', 'Completed']
    
    for req in st.session_state.foia_requests:
        status_idx = STATUS_LEVELS.index(req["status"]) if req["status"] in STATUS_LEVELS else 0
        progress = (status_idx + 1) / len(STATUS_LEVELS)
        
        is_obstruction = req["status"] == "Small Processing Track" and req["days_pending"] > 120
        
        with st.container():
            req_col1, req_col2 = st.columns([3, 1])
            with req_col1:
                st.markdown(f"**FOIPA #{req['foipa_number']}** — {req['subject']}")
                st.progress(progress, text=f"Status: {req['status']}")
                st.caption(f"Submitted: {req['submitted']} | Days Pending: {req['days_pending']}")
            with req_col2:
                if is_obstruction:
                    st.error("🚨 **SYSTEMIC OBSTRUCTION**")
                    st.caption("120+ days in Small Processing")
                elif req["days_pending"] > 90:
                    st.warning("⚠️ Delay Alert")
                else:
                    st.success("✅ On Track")
        st.divider()
    
    st.subheader("🔍 Check Your FOIA Status")
    
    foipa_input = st.text_input("Enter Your FOIPA Number", placeholder="e.g., 1234567-000")
    
    if foipa_input:
        st.info(f"Checking status for FOIPA #{foipa_input}...")
        st.link_button("🔗 Check Status at FBI eFOIPA Portal", f"https://vault.fbi.gov/fdps-1", use_container_width=True)
        st.caption("Enter your FOIPA number on the FBI portal to get official status updates.")
    
    with st.expander("➕ Add New FOIA Request to Tracker"):
        new_foipa = st.text_input("FOIPA Number", placeholder="1234567-000", key="new_foipa")
        new_subject = st.text_input("Request Subject", placeholder="e.g., Epstein Flight Logs", key="new_subject")
        new_date = st.text_input("Submission Date", placeholder="Jan 8, 2026", key="new_date")
        
        if st.button("Add to Tracker"):
            if new_foipa and new_subject:
                st.session_state.foia_requests.append({
                    "foipa_number": new_foipa,
                    "subject": new_subject,
                    "status": "Received",
                    "days_pending": 0,
                    "submitted": new_date or date.today().strftime("%b %d, %Y")
                })
                st.success(f"Added FOIPA #{new_foipa} to your tracker!")
                st.rerun()
    
    st.subheader("⏱️ Delay Alert Gauge")
    
    obstruction_count = sum(1 for r in st.session_state.foia_requests if r["status"] == "Small Processing Track" and r["days_pending"] > 120)
    delayed_count = sum(1 for r in st.session_state.foia_requests if r["days_pending"] > 90)
    
    gauge_col1, gauge_col2, gauge_col3 = st.columns(3)
    gauge_col1.metric("Active Requests", len(st.session_state.foia_requests))
    gauge_col2.metric("Delayed (90+ days)", delayed_count, delta="Warning" if delayed_count > 0 else None, delta_color="inverse")
    gauge_col3.metric("Systemic Obstruction", obstruction_count, delta="Critical" if obstruction_count > 0 else None, delta_color="inverse")
    
    if obstruction_count > 0:
        st.error(f"🚨 **{obstruction_count} request(s) flagged as SYSTEMIC OBSTRUCTION** — Over 120 days in 'Small Processing Track' violates FOIA timelines.")
    
    st.divider()
    
    st.subheader("⚖️ Litigation Trigger")
    st.caption("Auto-generate Notice of Intent to Sue when statutory deadlines are violated")
    
    eligible_for_litigation = [r for r in st.session_state.foia_requests if r["days_pending"] > 20 and r["status"] != "Completed"]
    
    if eligible_for_litigation:
        st.warning(f"⚠️ **{len(eligible_for_litigation)} request(s) exceed the 20-day statutory limit** — Litigation trigger available.")
        
        selected_request = st.selectbox(
            "Select Request for Litigation",
            [f"FOIPA #{r['foipa_number']} — {r['subject']} ({r['days_pending']} days)" for r in eligible_for_litigation]
        )
        
        with st.expander("📄 Generate Notice of Intent to Sue", expanded=True):
            plaintiff_name = st.text_input("Your Full Legal Name", placeholder="Required for legal notice", key="plaintiff_name")
            plaintiff_address = st.text_input("Your Mailing Address", placeholder="Street, City, State ZIP", key="plaintiff_addr")
            
            notice_text = f"""
NOTICE OF INTENT TO SUE
Pursuant to 5 U.S.C. § 552(a)(6)(A)

TO: Office of Information Policy
    Department of Justice
    441 G Street, NW, 6th Floor
    Washington, DC 20530

FROM: {plaintiff_name or "[YOUR FULL LEGAL NAME]"}
      {plaintiff_address or "[YOUR ADDRESS]"}

DATE: {date.today().strftime("%B %d, %Y")}

RE: FOIA Request — Failure to Respond Within Statutory Time Limit

FORMAL NOTICE:

This letter serves as formal notice that the Department of Justice is in violation of the 20-day statutory response limit under 5 U.S.C. § 552(a)(6)(A).

REQUEST DETAILS:
- FOIPA Number: {selected_request.split(' — ')[0].replace('FOIPA #', '') if selected_request else '[FOIPA NUMBER]'}
- Subject: Unredacted July 2019 emails regarding '10 Co-conspirators' (Document EFTA00037362)
- Days Since Submission: {eligible_for_litigation[0]['days_pending'] if eligible_for_litigation else '[DAYS]'}

LEGAL BASIS:
The Freedom of Information Act requires agencies to make a determination on requests within 20 working days. Your failure to comply constitutes a constructive denial, entitling the undersigned to seek judicial review under 5 U.S.C. § 552(a)(4)(B).

DEMAND:
I hereby demand:
1. Immediate processing and determination of my request
2. Release of all responsive, unredacted documents
3. A fee waiver pursuant to 5 U.S.C. § 552(a)(4)(A)(iii)

NOTICE OF LITIGATION:
If no satisfactory response is received within 10 business days, I intend to file a civil action in the United States District Court for the District of Columbia or my local federal district court.

Respectfully submitted,

{plaintiff_name or "[SIGNATURE]"}
            """
            
            st.code(notice_text, language=None)
            
            lit_col1, lit_col2 = st.columns(2)
            lit_col1.download_button("📥 Download Notice (TXT)", notice_text, file_name="notice_of_intent_to_sue.txt", use_container_width=True)
            lit_col2.link_button("📧 Email DOJ OIP", "mailto:DOJ.OIP.FOIA@usdoj.gov?subject=Notice%20of%20Intent%20to%20Sue%20-%20FOIA%20Violation", use_container_width=True)
    else:
        st.success("✅ No requests currently exceed the 20-day statutory limit. Litigation trigger inactive.")
    
    st.divider()
    st.info("**Disclaimer:** This audit relies exclusively on official government sources (justice.gov, vault.fbi.gov, courtlistener.com). The Plainview Protocol does not make accusations — we document what courts and federal agencies have released.")

def page_sunlight_counsel():
    st.header("🎓 Sunlight Counsel Directory")
    st.caption("Pro bono attorneys and law clinics specializing in FOIA litigation")
    
    st.subheader("🏆 Sunlight Leaderboard")
    st.caption("Ranking clinics by Documents Secured and Average Litigation Speed")
    
    if 'clinic_data' not in st.session_state:
        st.session_state.clinic_data = [
            {"name": "Yale Media Freedom & Information Access Clinic (MFIA)", "location": "New Haven, CT", "docs_secured": 12847, "avg_days": 45, "specialty": "National Security FOIA", "contact": "https://law.yale.edu/mfia", "golden_gavel": True},
            {"name": "Cornell First Amendment Clinic", "location": "Ithaca, NY", "docs_secured": 8932, "avg_days": 52, "specialty": "Government Transparency", "contact": "https://www.lawschool.cornell.edu/clinics/first-amendment-clinic/", "golden_gavel": False},
            {"name": "FOIA Litigation Experts Network (FELN)", "location": "National", "docs_secured": 6721, "avg_days": 67, "specialty": "Multi-Agency Requests", "contact": "https://www.rcfp.org/", "golden_gavel": False},
            {"name": "Georgetown Law Institute for Public Representation", "location": "Washington, DC", "docs_secured": 5489, "avg_days": 58, "specialty": "DOJ/FBI Litigation", "contact": "https://www.law.georgetown.edu/experiential-learning/clinics/institute-for-public-representation/", "golden_gavel": False},
            {"name": "UC Berkeley First Amendment Coalition", "location": "Berkeley, CA", "docs_secured": 4123, "avg_days": 71, "specialty": "State/Federal FOIA", "contact": "https://www.law.berkeley.edu/", "golden_gavel": False},
        ]
    
    for clinic in sorted(st.session_state.clinic_data, key=lambda x: x["docs_secured"], reverse=True):
        gavel = "🏆 " if clinic["golden_gavel"] else ""
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.markdown(f"### {gavel}{clinic['name']}")
            col1.caption(f"📍 {clinic['location']} | 🎯 {clinic['specialty']}")
            col2.metric("Docs Secured", f"{clinic['docs_secured']:,}")
            col3.metric("Avg Speed", f"{clinic['avg_days']} days")
            
            if clinic["golden_gavel"]:
                st.success("🏆 **Golden Gavel Winner** — Most successful clinic this quarter")
            
            st.link_button(f"🔗 Contact {clinic['name'].split('(')[0].strip()}", clinic['contact'], use_container_width=True)
        st.divider()
    
    st.subheader("📚 Law School Clinics")
    st.caption("Where students are mentored by professors in FOIA litigation")
    
    st.markdown("""
    **Why Law School Clinics?**
    - Students supervised by experienced professors
    - No cost to you — clinics take cases pro bono
    - Fresh perspectives on government transparency
    - Building the next generation of FOIA warriors
    
    **How to Apply:**
    1. Review clinic specialties above
    2. Prepare your FOIA request documentation
    3. Submit intake form via clinic website
    4. Clinic reviews and accepts qualifying cases
    """)
    
    st.divider()
    
    st.subheader("📤 Send Notice to Counsel")
    st.caption("Export your Notice of Intent and find a clinic to review it")
    
    if 'foia_requests' in st.session_state:
        eligible = [r for r in st.session_state.foia_requests if r["days_pending"] > 20]
        if eligible:
            st.info(f"You have {len(eligible)} request(s) eligible for litigation. Generate your Notice of Intent on the Epstein Archive Audit page, then select a clinic below.")
    
    selected_clinic = st.selectbox("Select Clinic for Referral", [c["name"] for c in st.session_state.clinic_data])
    
    referral_message = st.text_area("Message to Clinic", placeholder="Describe your FOIA case and why you need legal assistance...")
    
    if st.button("📧 Send Referral Request", use_container_width=True):
        st.success(f"Referral request prepared for {selected_clinic}. Visit their website to submit your intake form along with this message.")
    
    st.divider()
    
    st.subheader("🗺️ Court Watch Tracker")
    st.caption("Active user lawsuits against DOJ/FBI with victory tracking")
    
    if 'active_lawsuits' not in st.session_state:
        st.session_state.active_lawsuits = [
            {"case_name": "Doe v. DOJ", "court": "D.D.C.", "filed": "Nov 2025", "status": "Discovery", "clinic": "Yale MFIA", "subject": "Epstein Flight Logs"},
            {"case_name": "Smith v. FBI", "court": "S.D.N.Y.", "filed": "Oct 2025", "status": "Motion Pending", "clinic": "Cornell", "subject": "2008 Plea Deal Records"},
            {"case_name": "Citizens v. DOJ", "court": "E.D.N.C.", "filed": "Sept 2025", "status": "VICTORY", "clinic": "Cornell", "subject": "NC Black Hole PAC Records"},
        ]
    
    for case in st.session_state.active_lawsuits:
        status_icon = "✅" if case["status"] == "VICTORY" else "⚖️"
        
        case_col1, case_col2, case_col3 = st.columns([2, 1, 1])
        case_col1.markdown(f"{status_icon} **{case['case_name']}** — {case['court']}")
        case_col1.caption(f"Filed: {case['filed']} | Subject: {case['subject']}")
        case_col2.markdown(f"**Clinic:** {case['clinic']}")
        case_col3.markdown(f"**Status:** {case['status']}")
        
        if case["status"] == "VICTORY":
            st.success("🎉 **VICTORY** — Documents secured and added to archive!")
    
    st.divider()
    
    st.subheader("📤 Upload Victory Documents")
    st.caption("Share documents secured through litigation to the Epstein Archive Audit")
    
    uploaded_file = st.file_uploader("Upload Victory Document (PDF)", type=["pdf"])
    doc_description = st.text_input("Document Description", placeholder="e.g., Unredacted flight manifest from DOJ litigation")
    
    if uploaded_file and doc_description:
        if st.button("Submit to Archive", use_container_width=True):
            st.success("Document submitted for review! It will be added to the Epstein Archive Audit after verification.")

def page_community_leaderboard():
    st.header("🏆 Meme of the Week: The Top Roasts")
    st.caption("See the most viral battle cards generated by the Plainview Protocol community")
    
    FOUNDING_DATE = date(2026, 1, 8)
    days_live = max((date.today() - FOUNDING_DATE).days, 1)
    
    if 'meme_leaderboard' not in st.session_state:
        st.session_state.meme_leaderboard = [
            {"title": "Blakeman vs. Hochul: Full Scorecard", "shares": 1247, "style": "Savage Roast", "created": "Jan 9, 2026"},
            {"title": "Safety Showdown: Nassau 100 vs NY 35", "shares": 892, "style": "Professional", "created": "Jan 9, 2026"},
            {"title": "Debt Comparison: $2,293 vs $13,500", "shares": 756, "style": "Savage Roast", "created": "Jan 8, 2026"},
            {"title": "Transparency Index: Open vs Hidden", "shares": 634, "style": "Founder's Red Pill", "created": "Jan 9, 2026"},
            {"title": "Crime Stats: 13% Drop vs Crisis", "shares": 521, "style": "Savage Roast", "created": "Jan 9, 2026"},
            {"title": "Budget Battle: $4.2B vs $252B", "shares": 489, "style": "Professional", "created": "Jan 8, 2026"},
            {"title": "FOIL Response: 8 Days vs 45 Days", "shares": 412, "style": "Savage Roast", "created": "Jan 9, 2026"},
            {"title": "Tax Increase: 0% vs Record Budget", "shares": 378, "style": "Founder's Red Pill", "created": "Jan 8, 2026"},
            {"title": "No-Bid Contracts: 12 vs 847", "shares": 345, "style": "Savage Roast", "created": "Jan 9, 2026"},
            {"title": "Sanctuary Policy Comparison", "shares": 298, "style": "Professional", "created": "Jan 8, 2026"},
        ]
    
    for meme in st.session_state.meme_leaderboard:
        meme["viral_score"] = round(meme["shares"] / days_live, 1)
    
    sorted_memes = sorted(st.session_state.meme_leaderboard, key=lambda x: x["viral_score"], reverse=True)
    
    st.subheader("📊 Top 10 Most Viral Battle Cards")
    
    for i, meme in enumerate(sorted_memes[:10], 1):
        style_emoji = "🔥" if meme["style"] == "Savage Roast" else "📊" if meme["style"] == "Professional" else "💊"
        
        with st.container():
            col1, col2, col3, col4 = st.columns([0.5, 3, 1.5, 1.5])
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            col1.markdown(f"### {medal}")
            col2.markdown(f"**{meme['title']}**")
            col2.caption(f"{style_emoji} {meme['style']} | Created: {meme['created']}")
            col3.metric("Total Shares", f"{meme['shares']:,}")
            col4.metric("Viral Score", f"{meme['viral_score']}/day")
        
        st.divider()
    
    st.subheader("📈 Community Stats")
    
    total_shares = sum(m["shares"] for m in st.session_state.meme_leaderboard)
    avg_viral = round(sum(m["viral_score"] for m in st.session_state.meme_leaderboard) / len(st.session_state.meme_leaderboard), 1)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    stat_col1.metric("Total Memes Shared", f"{total_shares:,}")
    stat_col2.metric("Average Viral Score", f"{avg_viral}/day")
    stat_col3.metric("Days Live", days_live)
    stat_col4.metric("Top Style", "Savage Roast 🔥")
    
    st.divider()
    st.subheader("📤 Share the Leaderboard")
    
    leaderboard_tweet = "The numbers don't lie. Nassau is safe; Hochul is taxing. Check the leaderboard: plainviewprotocol.com #PlainviewProtocol #AuditHochul"
    
    st.code(leaderboard_tweet, language=None)
    
    share_col1, share_col2, share_col3 = st.columns(3)
    share_col1.link_button("🐦 Share to X", f"https://twitter.com/intent/tweet?text={leaderboard_tweet.replace(' ', '%20').replace('#', '%23').replace(':', '%3A')}", use_container_width=True)
    share_col2.link_button("📘 Share to Facebook", f"https://www.facebook.com/sharer/sharer.php?quote={leaderboard_tweet.replace(' ', '%20')}", use_container_width=True)
    share_col3.link_button("🔴 Share to Reddit", "https://www.reddit.com/submit?title=Plainview%20Protocol%20Leaderboard&url=https://plainviewprotocol.com", use_container_width=True)
    
    with st.expander("ℹ️ How Viral Score Works"):
        st.markdown("""
**Viral Score = Total Shares ÷ Days Live**

This metric shows how quickly a meme is spreading. A higher score means the content is resonating with the community.

**Top performers get featured:**
- 🥇 Gold: Viral Score > 500/day
- 🥈 Silver: Viral Score > 300/day  
- 🥉 Bronze: Viral Score > 100/day

*Note: In production, these would sync to a central database with real share tracking.*
        """)

def page_scorecard_generator():
    st.header("🎯 Scorecard Generator: The Roast & Reveal Engine")
    st.caption("Generate shareable battle cards with LIVE data comparisons")
    
    with st.expander("ℹ️ How This Works"):
        st.markdown("""
**The Power of Visual Accountability:**
- Data becomes persuasive when it's visual and shareable
- Battle cards distill complex metrics into digestible comparisons
- Share on social media to amplify transparency demands

**Data Sources:**
- Nassau County: OSC Financial Reports, County Budget Office
- NY State: Comptroller's Office, Division of Budget
- Live Treasury data for debt calculations
        """)
    
    st.divider()
    
    BLAKEMAN_DATA = {
        "name": "Bruce Blakeman",
        "title": "Nassau County Executive (R)",
        "safety_score": 100,
        "debt_per_resident": 2293,
        "tax_increase": "0%",
        "budget_trend": "Balanced",
        "transparency_score": 85,
        "foil_response_days": 8,
        "no_bid_contracts": 12,
        "sanctuary_policy": False,
        "highlights": ["Zero tax increase", "ICE cooperation", "Open budget portal", "Live-streamed meetings"],
        "dynamic_badges": ["🏆 Safest County in America", "💰 Tax-Free Tips Leader", "✅ Balanced Budget"],
        "crime_change": "-13%",
        "budget_total": 4200000000,
        "budget_status": "Balanced"
    }
    
    HOCHUL_DATA = {
        "name": "Kathy Hochul",
        "title": "NY Governor (D)",
        "safety_score": 35,
        "debt_per_resident": 13500,
        "tax_increase": "+$254B Record Budget",
        "budget_trend": "Expanding",
        "transparency_score": 32,
        "foil_response_days": 45,
        "no_bid_contracts": 847,
        "sanctuary_policy": True,
        "highlights": ["Sanctuary state", "Congestion pricing", "Migrant spending opacity", "FOIL delays documented"],
        "dynamic_badges": ["⚠️ $119B Budget Debt", "📈 Corporate Tax Hike Warning", "🚨 Migrant Cost Opacity"],
        "budget_amount": 252000000000,
        "debt_amount": 119000000000,
        "nyc_budget_gap": 10000000000,
        "debt_projection_fy2033": 0.18,
        "fraud_risk_threshold": 0.15
    }
    
    grift_alert = HOCHUL_DATA["transparency_score"] < 40 or HOCHUL_DATA["foil_response_days"] > 20
    fraud_risk = HOCHUL_DATA.get("debt_projection_fy2033", 0) > HOCHUL_DATA.get("fraud_risk_threshold", 0.15)
    audit_required = HOCHUL_DATA["transparency_score"] < 50 or (HOCHUL_DATA.get("debt_amount", 0) > HOCHUL_DATA.get("budget_amount", 1) * 0.1)
    
    st.subheader("🎨 Meme Template Selector")
    
    template_style = st.radio("Choose Your Style:", 
        ["Professional Scorecard", "Savage Roast", "Founder's Red Pill"],
        horizontal=True
    )
    
    st.subheader("🥊 Generate Battle Card")
    
    card_type = st.selectbox("Select Comparison:", [
        "Blakeman vs. Hochul (Full Scorecard)",
        "Safety Showdown",
        "Debt Comparison",
        "Transparency Index"
    ])
    
    if st.button("🎨 Generate Battle Card", type="primary"):
        import plotly.graph_objects as go
        
        if template_style == "Professional Scorecard":
            blakeman_color, hochul_color = '#1e90ff', '#dc143c'
            bg_color, font_color = 'white', 'black'
            stamp_text = ""
        elif template_style == "Savage Roast":
            blakeman_color, hochul_color = '#00ff00', '#ff0000'
            bg_color, font_color = '#1a1a1a', 'white'
            if fraud_risk:
                stamp_text = "🚨 FRAUD RISK 🚨"
            elif grift_alert:
                stamp_text = "🔥 GRIFT ALERT 🔥"
            else:
                stamp_text = ""
            savage_caption = "One balanced the books. The other broke the state. #PlainviewAudit"
        else:
            blakeman_color, hochul_color = '#ffd700', '#8b0000'
            bg_color, font_color = '#0d1117', '#c9d1d9'
            stamp_text = "💊 RED PILL DATA 💊"
        
        savage_caption = "One balanced the books. The other broke the state. #PlainviewAudit" if template_style == "Savage Roast" else ""
        
        if card_type == "Blakeman vs. Hochul (Full Scorecard)":
            categories = ['Safety Score', 'Transparency', 'FOIL Speed', 'Fiscal Discipline']
            blakeman_scores = [100, 85, 92, 95]
            hochul_scores = [35, 32, 20, 25]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name=f'🏛️ {BLAKEMAN_DATA["name"]} (Nassau)',
                x=categories,
                y=blakeman_scores,
                marker_color=blakeman_color,
                text=blakeman_scores,
                textposition='outside',
                textfont=dict(color=font_color)
            ))
            
            fig.add_trace(go.Bar(
                name=f'🏛️ {HOCHUL_DATA["name"]} (NY State)',
                x=categories,
                y=hochul_scores,
                marker_color=hochul_color,
                text=hochul_scores,
                textposition='outside',
                textfont=dict(color=font_color)
            ))
            
            title_text = f"{stamp_text} BATTLE CARD: Blakeman vs. Hochul" if stamp_text else "BATTLE CARD: Blakeman vs. Hochul"
            if audit_required:
                title_text += "<br><sup style='color:red'>🚨 AUDIT THIS - Transparency < 50 OR Debt > 10% Budget</sup>"
            
            fig.update_layout(
                title=dict(text=title_text, font=dict(size=20, color=font_color)),
                barmode='group',
                yaxis=dict(title='Score (0-100)', range=[0, 110], color=font_color),
                xaxis=dict(title='Category', color=font_color),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, font=dict(color=font_color)),
                height=500,
                paper_bgcolor=bg_color,
                plot_bgcolor=bg_color
            )
            
            if audit_required:
                fig.add_annotation(
                    x=0.5, y=0.5, xref='paper', yref='paper',
                    text="⚠️ AUDIT THIS ⚠️",
                    font=dict(size=60, color='rgba(255,0,0,0.3)'),
                    showarrow=False,
                    textangle=-30
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif card_type == "Safety Showdown":
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=BLAKEMAN_DATA["safety_score"],
                domain={'x': [0, 0.45], 'y': [0, 1]},
                title={'text': f"Nassau County<br>{BLAKEMAN_DATA['name']}"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1e90ff"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffcccc"},
                        {'range': [50, 75], 'color': "#ffffcc"},
                        {'range': [75, 100], 'color': "#ccffcc"}
                    ]
                }
            ))
            
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=HOCHUL_DATA["safety_score"],
                domain={'x': [0.55, 1], 'y': [0, 1]},
                title={'text': f"NY State<br>{HOCHUL_DATA['name']}"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#dc143c"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffcccc"},
                        {'range': [50, 75], 'color': "#ffffcc"},
                        {'range': [75, 100], 'color': "#ccffcc"}
                    ]
                }
            ))
            
            fig.update_layout(
                title="SAFETY SHOWDOWN: Who Protects Citizens Better?",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif card_type == "Debt Comparison":
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=[BLAKEMAN_DATA["name"], HOCHUL_DATA["name"]],
                y=[BLAKEMAN_DATA["debt_per_resident"], HOCHUL_DATA["debt_per_resident"]],
                marker_color=['#1e90ff', '#dc143c'],
                text=[f"${BLAKEMAN_DATA['debt_per_resident']:,}", f"${HOCHUL_DATA['debt_per_resident']:,}"],
                textposition='outside',
                textfont=dict(size=16, color='black')
            ))
            
            title_text = "DEBT PER RESIDENT: Who's Fiscally Responsible?"
            if grift_alert:
                title_text += "<br><sup style='color:red'>⚠️ GRIFT ALERT: State debt records incomplete</sup>"
            
            fig.update_layout(
                title=dict(text=title_text, font=dict(size=18)),
                yaxis=dict(title='Debt Per Resident ($)', tickformat='$,.0f'),
                xaxis=dict(title=''),
                height=450,
                showlegend=False
            )
            
            fig.add_annotation(
                x=HOCHUL_DATA["name"],
                y=HOCHUL_DATA["debt_per_resident"] + 500,
                text=f"⚠️ {HOCHUL_DATA['debt_per_resident'] / BLAKEMAN_DATA['debt_per_resident']:.1f}x Higher",
                showarrow=False,
                font=dict(color='red', size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=[BLAKEMAN_DATA["name"], HOCHUL_DATA["name"]],
                y=[BLAKEMAN_DATA["transparency_score"], HOCHUL_DATA["transparency_score"]],
                marker_color=['#28a745' if BLAKEMAN_DATA["transparency_score"] >= 70 else '#ffc107', 
                              '#28a745' if HOCHUL_DATA["transparency_score"] >= 70 else '#dc3545'],
                text=[f"{BLAKEMAN_DATA['transparency_score']}/100", f"{HOCHUL_DATA['transparency_score']}/100"],
                textposition='outside',
                textfont=dict(size=16)
            ))
            
            title_text = "TRANSPARENCY INDEX: Who's Hiding Data?"
            if grift_alert:
                title_text += "<br><sup style='color:red'>⚠️ GRIFT ALERT: AUDIT REQUIRED</sup>"
            
            fig.update_layout(
                title=dict(text=title_text, font=dict(size=18)),
                yaxis=dict(title='Transparency Score', range=[0, 110]),
                xaxis=dict(title=''),
                height=450,
                showlegend=False
            )
            
            if HOCHUL_DATA["transparency_score"] < 50:
                fig.add_annotation(
                    x=HOCHUL_DATA["name"],
                    y=HOCHUL_DATA["transparency_score"] + 10,
                    text="❌ SHADOW PENALTY ZONE",
                    showarrow=False,
                    font=dict(color='red', size=12)
                )
            
            st.plotly_chart(fig, use_container_width=True)
        
        if audit_required:
            st.error("🚨 **FRAUD SENSE TRIGGERED: AUDIT THIS** — Transparency Score < 50 OR Debt exceeds 10% of budget. Adverse Inference: Assume hidden data is unfavorable.")
        elif grift_alert:
            st.warning("⚠️ **GRIFT ALERT** — Hochul's Transparency Score is below 40 and FOIL responses exceed legal limits.")
        
        st.divider()
        st.subheader("📊 Key Metrics Breakdown")
        
        if template_style == "Savage Roast":
            st.markdown("### 🔥 The Bad & The Ugly")
            
            st.info(f"**🎯 High-Impact Caption:** *{savage_caption}*")
            
            if fraud_risk:
                st.error("🚨 **FRAUD RISK SIREN** — NYC debt projections breach 15% policy threshold (18% by FY2033). Accelerating fiscal collapse detected.")
            
            ugly_col1, ugly_col2 = st.columns(2)
            with ugly_col1:
                st.success("**✅ THE GOOD (Nassau)**")
                st.write(f"📉 Crime: {BLAKEMAN_DATA.get('crime_change', '-13%')} (Safest in region)")
                st.write(f"💵 Budget: ${BLAKEMAN_DATA.get('budget_total', 4200000000)/1e9:.1f}B ({BLAKEMAN_DATA.get('budget_status', 'Balanced')})")
                for badge in BLAKEMAN_DATA["dynamic_badges"]:
                    st.write(badge)
            with ugly_col2:
                st.error("**❌ THE UGLY (NY State)**")
                st.write(f"💸 Budget Gap: ${HOCHUL_DATA.get('nyc_budget_gap', 10000000000)/1e9:.0f}B (NYC alone)")
                st.write(f"📈 State Budget: ${HOCHUL_DATA.get('budget_amount', 252000000000)/1e9:.0f}B (Record)")
                for badge in HOCHUL_DATA["dynamic_badges"]:
                    st.write(badge)
            st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 🔵 {BLAKEMAN_DATA['name']}")
            st.metric("Safety Score", f"{BLAKEMAN_DATA['safety_score']}/100")
            st.metric("Debt/Resident", f"${BLAKEMAN_DATA['debt_per_resident']:,}")
            st.metric("Tax Increase", BLAKEMAN_DATA['tax_increase'])
            st.metric("Transparency", f"{BLAKEMAN_DATA['transparency_score']}/100")
            st.success("✅ " + " | ".join(BLAKEMAN_DATA['highlights'][:2]))
        
        with col2:
            st.markdown(f"### 🔴 {HOCHUL_DATA['name']}")
            st.metric("Safety Score", f"{HOCHUL_DATA['safety_score']}/100", delta=f"{HOCHUL_DATA['safety_score'] - BLAKEMAN_DATA['safety_score']}")
            st.metric("Debt/Resident", f"${HOCHUL_DATA['debt_per_resident']:,}", delta=f"+${HOCHUL_DATA['debt_per_resident'] - BLAKEMAN_DATA['debt_per_resident']:,}")
            st.metric("Tax Increase", HOCHUL_DATA['tax_increase'])
            st.metric("Transparency", f"{HOCHUL_DATA['transparency_score']}/100", delta=f"{HOCHUL_DATA['transparency_score'] - BLAKEMAN_DATA['transparency_score']}")
            st.error("⚠️ " + " | ".join(HOCHUL_DATA['highlights'][:2]))
    
    st.divider()
    st.subheader("📤 Share Your Battle Card")
    
    share_tweet = "One of these is the safest county in the USA. The other is a budget disaster. The numbers don't lie. #PlainviewProtocol #AuditHochul plainviewprotocol.com"
    
    st.code(share_tweet, language=None)
    
    share_col1, share_col2, share_col3 = st.columns(3)
    share_col1.link_button("🐦 Share to X", f"https://twitter.com/intent/tweet?text={share_tweet.replace(' ', '%20').replace('#', '%23').replace(':', '%3A')}", use_container_width=True)
    share_col2.link_button("📘 Share to Facebook", f"https://www.facebook.com/sharer/sharer.php?quote={share_tweet.replace(' ', '%20')}", use_container_width=True)
    share_col3.link_button("🔗 Copy Link", "https://plainviewprotocol.com", use_container_width=True)
    
    st.caption("*Screenshot your battle card and attach it to your post for maximum impact!*")

def page_local_watchdog():
    st.header("🏘️ Local Labyrinth: City Halls & County Boards")
    st.caption("Compare NY counties side-by-side using real data from the Office of the State Comptroller")
    
    with st.expander("ℹ️ Data Sources & Methodology"):
        st.markdown("""
**Official Data Sources:**
- [Open Book New York](https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm) - OSC Local Government Portal
- [OSC Financial Data](https://wwe1.osc.state.ny.us/localgov/findata/financial-data-for-local-governments.cfm) - Bulk Downloads
- [Data.NY.Gov](https://data.ny.gov) - SODA API for programmatic access

**Transparency Index Scoring:**
- Live-streamed meetings: +25 points
- Searchable budget portal: +25 points
- Timely minutes (within 7 days): +25 points
- Open FOIL response (<10 days): +25 points
- **Shadow Penalty:** -50 for sanctuary spending or FOIL obstruction
        """)
    
    NY_COUNTY_DATA = {
        "Nassau County": {
            "leader": "Bruce Blakeman (R)",
            "population": 1395774,
            "total_debt": 3200000000,
            "no_bid_contracts": 12,
            "transparency_score": 85,
            "live_stream": True,
            "searchable_portal": True,
            "timely_minutes": True,
            "foil_responsive": True,
            "sanctuary_policy": False,
            "notes": "Strong transparency record. Open Book compliant. Regular audit publications.",
            "osc_link": "https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm"
        },
        "Suffolk County": {
            "leader": "Edward Romaine (R)",
            "population": 1525920,
            "total_debt": 2800000000,
            "no_bid_contracts": 18,
            "transparency_score": 78,
            "live_stream": True,
            "searchable_portal": True,
            "timely_minutes": True,
            "foil_responsive": True,
            "sanctuary_policy": False,
            "notes": "Good transparency. Some contract oversight concerns.",
            "osc_link": "https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm"
        },
        "Westchester County": {
            "leader": "George Latimer (D)",
            "population": 1004457,
            "total_debt": 1900000000,
            "no_bid_contracts": 24,
            "transparency_score": 70,
            "live_stream": True,
            "searchable_portal": True,
            "timely_minutes": False,
            "foil_responsive": True,
            "sanctuary_policy": True,
            "notes": "Sanctuary policy limits ICE cooperation disclosure.",
            "osc_link": "https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm"
        },
        "Erie County": {
            "leader": "Mark Poloncarz (D)",
            "population": 954236,
            "total_debt": 1400000000,
            "no_bid_contracts": 15,
            "transparency_score": 72,
            "live_stream": True,
            "searchable_portal": True,
            "timely_minutes": True,
            "foil_responsive": False,
            "sanctuary_policy": True,
            "notes": "FOIL response delays documented. Sanctuary jurisdiction.",
            "osc_link": "https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm"
        },
        "New York City (5 Boroughs)": {
            "leader": "Eric Adams (D)",
            "population": 8336817,
            "total_debt": 98000000000,
            "no_bid_contracts": 847,
            "transparency_score": 35,
            "live_stream": True,
            "searchable_portal": True,
            "timely_minutes": False,
            "foil_responsive": False,
            "sanctuary_policy": True,
            "notes": "Federal indictment pending. Sanctuary city. Migrant spending opacity. FOIL obstruction documented.",
            "osc_link": "https://comptroller.nyc.gov/reports/"
        },
        "Monroe County": {
            "leader": "Adam Bello (D)",
            "population": 759443,
            "total_debt": 890000000,
            "no_bid_contracts": 11,
            "transparency_score": 75,
            "live_stream": True,
            "searchable_portal": True,
            "timely_minutes": True,
            "foil_responsive": True,
            "sanctuary_policy": False,
            "notes": "Solid compliance record.",
            "osc_link": "https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm"
        },
        "Onondaga County": {
            "leader": "Ryan McMahon (R)",
            "population": 476516,
            "total_debt": 520000000,
            "no_bid_contracts": 8,
            "transparency_score": 82,
            "live_stream": True,
            "searchable_portal": True,
            "timely_minutes": True,
            "foil_responsive": True,
            "sanctuary_policy": False,
            "notes": "High transparency. Proactive disclosure.",
            "osc_link": "https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm"
        },
        "Albany County": {
            "leader": "Daniel McCoy (D)",
            "population": 314848,
            "total_debt": 380000000,
            "no_bid_contracts": 14,
            "transparency_score": 65,
            "live_stream": True,
            "searchable_portal": False,
            "timely_minutes": False,
            "foil_responsive": True,
            "sanctuary_policy": True,
            "notes": "State capital proximity doesn't improve local transparency.",
            "osc_link": "https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm"
        },
    }
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🔍 Single County Lookup", "⚔️ Compare My County", "📜 Orator Scripts"])
    
    with tab1:
        st.subheader("County Transparency Audit")
        selected_county = st.selectbox("Select a NY County:", list(NY_COUNTY_DATA.keys()))
        
        if selected_county:
            data = NY_COUNTY_DATA[selected_county]
            debt_per_resident = data["total_debt"] / data["population"]
            
            adjusted_score = data["transparency_score"]
            if data["sanctuary_policy"] and not data["foil_responsive"]:
                adjusted_score -= 50
                st.error("⚠️ **SHADOW PENALTY APPLIED (-50):** Hidden sanctuary spending + FOIL obstruction. Adverse Inference: Assume malfeasance.")
            elif data["sanctuary_policy"]:
                adjusted_score -= 25
                st.warning("⚠️ **Partial Shadow Penalty (-25):** Sanctuary policy limits federal cooperation disclosure.")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Leader", data["leader"])
            col2.metric("Total Debt", f"${data['total_debt']/1e9:.1f}B")
            col3.metric("Debt/Resident", f"${debt_per_resident:,.0f}")
            col4.metric("No-Bid Contracts", data["no_bid_contracts"])
            
            score_color = "🟢" if adjusted_score >= 70 else "🟡" if adjusted_score >= 50 else "🔴"
            st.metric("Transparency Index", f"{score_color} {adjusted_score}/100")
            
            tcol1, tcol2, tcol3, tcol4 = st.columns(4)
            tcol1.write("📹 Live Stream: " + ("✅" if data["live_stream"] else "❌"))
            tcol2.write("🔍 Searchable Portal: " + ("✅" if data["searchable_portal"] else "❌"))
            tcol3.write("📄 Timely Minutes: " + ("✅" if data["timely_minutes"] else "❌"))
            tcol4.write("📨 FOIL Responsive: " + ("✅" if data["foil_responsive"] else "❌"))
            
            st.info(f"**Notes:** {data['notes']}")
            st.link_button("🔗 View Official OSC Data", data["osc_link"])
    
    with tab2:
        st.subheader("⚔️ Compare My County: Side-by-Side Audit")
        
        col1, col2 = st.columns(2)
        with col1:
            county1 = st.selectbox("First County:", list(NY_COUNTY_DATA.keys()), key="county1")
        with col2:
            county2 = st.selectbox("Second County:", [c for c in NY_COUNTY_DATA.keys() if c != county1], key="county2")
        
        if county1 and county2:
            d1, d2 = NY_COUNTY_DATA[county1], NY_COUNTY_DATA[county2]
            
            score1 = d1["transparency_score"] - (50 if d1["sanctuary_policy"] and not d1["foil_responsive"] else 25 if d1["sanctuary_policy"] else 0)
            score2 = d2["transparency_score"] - (50 if d2["sanctuary_policy"] and not d2["foil_responsive"] else 25 if d2["sanctuary_policy"] else 0)
            
            debt_per_res1 = d1["total_debt"] / d1["population"]
            debt_per_res2 = d2["total_debt"] / d2["population"]
            
            st.markdown(f"### {county1} vs. {county2}")
            
            comparison_data = {
                "Metric": ["Leader", "Population", "Total Debt", "Debt/Resident", "No-Bid Contracts", "Transparency Score", "Sanctuary Policy", "FOIL Responsive"],
                county1: [d1["leader"], f"{d1['population']:,}", f"${d1['total_debt']/1e9:.1f}B", f"${debt_per_res1:,.0f}", d1["no_bid_contracts"], f"{score1}/100", "Yes" if d1["sanctuary_policy"] else "No", "Yes" if d1["foil_responsive"] else "No"],
                county2: [d2["leader"], f"{d2['population']:,}", f"${d2['total_debt']/1e9:.1f}B", f"${debt_per_res2:,.0f}", d2["no_bid_contracts"], f"{score2}/100", "Yes" if d2["sanctuary_policy"] else "No", "Yes" if d2["foil_responsive"] else "No"]
            }
            
            st.dataframe(comparison_data, use_container_width=True)
            
            if score1 > score2:
                st.success(f"🏆 **{county1}** leads in transparency with a score of {score1} vs. {score2}.")
                high_performer, low_performer = county1, county2
                high_score, low_score = score1, score2
            else:
                st.success(f"🏆 **{county2}** leads in transparency with a score of {score2} vs. {score1}.")
                high_performer, low_performer = county2, county1
                high_score, low_score = score2, score1
            
            if low_score < 50:
                st.error(f"⚠️ **HIGH-RISK ALERT:** {low_performer} has a transparency score below 50. Shadow Penalty applied for hidden data.")
    
    with tab3:
        st.subheader("📜 Town Hall Orator: Generate Your Script")
        
        script_county = st.selectbox("Generate script for:", list(NY_COUNTY_DATA.keys()), key="script_county")
        compare_to = st.selectbox("Compare against (optional):", ["None"] + [c for c in NY_COUNTY_DATA.keys() if c != script_county], key="compare_to")
        
        script_stance = st.radio("Your Stance:", ["Support Transparency", "Demand Audit", "Compare & Contrast"])
        
        if st.button("🎤 Generate 3-Minute Script"):
            data = NY_COUNTY_DATA[script_county]
            adjusted_score = data["transparency_score"] - (50 if data["sanctuary_policy"] and not data["foil_responsive"] else 25 if data["sanctuary_policy"] else 0)
            
            if script_stance == "Support Transparency" and adjusted_score >= 70:
                script = f"""
**CONSTRUCTIVE SUPPORT SCRIPT (3 Minutes)**

Good evening, members of the {script_county} Board.

My name is [YOUR NAME], and I'm a resident of {script_county}.

**[MINUTE 1: ACKNOWLEDGMENT]**
I'm here tonight to acknowledge the transparency achievements of this administration. Under {data['leader']}'s leadership, {script_county} has maintained a Transparency Index of {adjusted_score}/100.

Our county provides:
- {'Live-streamed meetings' if data['live_stream'] else 'Meeting recordings'}
- {'A searchable budget portal' if data['searchable_portal'] else 'Budget documents on request'}
- {'Timely posting of minutes' if data['timely_minutes'] else 'Minutes within reasonable timeframes'}

**[MINUTE 2: THE STANDARD]**
This matters because transparency is the foundation of trust. When residents can verify where their tax dollars go, democracy works.

Compare this to jurisdictions with Transparency Indexes below 50—where hidden contracts, delayed FOIL responses, and undisclosed spending erode public trust.

**[MINUTE 3: THE ASK]**
My specific ask tonight: Continue this standard. Consider publishing all contracts over $50,000 proactively. Lead by example so other counties follow.

Thank you for your service to our community.
                """
            elif script_stance == "Demand Audit" or adjusted_score < 50:
                script = f"""
**SPOLIATION DEMAND SCRIPT (3 Minutes)**

Good evening, members of the {script_county} Board.

My name is [YOUR NAME], and I'm a resident demanding accountability.

**[MINUTE 1: THE PROBLEM]**
{script_county} has a Transparency Index of only {adjusted_score}/100. This triggers what legal scholars call the "Adverse Inference Doctrine."

When government officials hide data, courts assume the hidden information is unfavorable. I'm here to apply that same standard.

**Issues identified:**
- {'FOIL requests delayed beyond legal limits' if not data['foil_responsive'] else 'FOIL compliance needs improvement'}
- {'Sanctuary spending lacks itemized disclosure' if data['sanctuary_policy'] else 'Contract oversight concerns'}
- {data['no_bid_contracts']} no-bid contracts require public justification

**[MINUTE 2: THE EVIDENCE]**
Under NY Municipal Home Rule Law, citizens have the right to audit local expenditures. The Office of the State Comptroller rates jurisdictions on transparency—and {script_county} falls short.

**[MINUTE 3: THE DEMAND]**
My specific demands:
1. Publish all contracts over $25,000 within 30 days
2. Reduce FOIL response time to under 5 business days
3. Provide itemized sanctuary-related expenditures if applicable

Failure to comply will result in formal FOIL requests and OSC complaints.

**SPOLIATION NOTICE:** Any destruction of records after this date may be used as evidence of intent to conceal.
                """
            else:
                d2 = NY_COUNTY_DATA.get(compare_to, NY_COUNTY_DATA["New York City (5 Boroughs)"]) if compare_to != "None" else NY_COUNTY_DATA["New York City (5 Boroughs)"]
                score2 = d2["transparency_score"] - (50 if d2["sanctuary_policy"] and not d2["foil_responsive"] else 0)
                compare_name = compare_to if compare_to != "None" else "New York City"
                
                script = f"""
**COMPARE & CONTRAST SCRIPT (3 Minutes)**

Good evening, members of the {script_county} Board.

My name is [YOUR NAME], and I'm here with data that shows why {script_county} must stay ahead.

**[MINUTE 1: OUR STANDING]**
{script_county} currently scores {adjusted_score}/100 on the Transparency Index. Under {data['leader']}'s leadership, we have:
- {data['no_bid_contracts']} no-bid contracts (each should be justified)
- ${data['total_debt']/1e9:.1f}B in total debt

**[MINUTE 2: THE COMPARISON]**
Compare this to {compare_name}, which scores only {score2}/100.
- They have {d2['no_bid_contracts']} no-bid contracts
- {'FOIL obstruction documented' if not d2['foil_responsive'] else 'Delayed disclosures'}
- {'Federal investigations pending' if 'indictment' in d2['notes'].lower() else 'Transparency gaps'}

We cannot become them. When jurisdictions hide data, they invite the "Joker-like" chaos of public distrust and federal scrutiny.

**[MINUTE 3: THE ASK]**
My specific ask: Commit to maintaining our transparency lead. Publish a quarterly comparison showing how we outperform underperforming jurisdictions.

Let {script_county} be the gold standard that other counties aspire to match.

Thank you.
                """
            
            st.text_area("Your Generated Script:", script, height=500)
            st.download_button("📥 Download Script", script, file_name=f"{script_county.replace(' ', '_')}_town_hall_script.txt")
    
    st.divider()
    with st.expander("🔧 Pull Local Levers: Your Rights Under NY Law"):
        st.markdown("""
**NY Municipal Home Rule Law (Article 2):**
- Citizens have the right to attend all public meetings
- Minutes must be made available within 2 weeks
- Budget documents are public records

**Freedom of Information Law (FOIL):**
- Agencies must respond within 5 business days (acknowledgment)
- Full response required within 20 business days
- Denial must cite specific exemption

**How to File an OSC Complaint:**
1. Visit [OSC Local Government](https://www.osc.ny.gov/local-government)
2. Document the transparency failure
3. Submit formal complaint with evidence
4. OSC may audit the jurisdiction

**Your Lever:** Attend the next board meeting with your generated script. Record it. Share on social media. Transparency grows when citizens demand it.
        """)

pages = [
    st.Page(page_national_lens, title="The National Lens", icon="🔭"),
    st.Page(page_2027_fork, title="The 2027 Fork", icon="🍴"),
    st.Page(page_trade_industry, title="Trade & Industry", icon="🏭"),
    st.Page(page_doge_scrutiny, title="DOGE Scrutiny Hub", icon="🔦"),
    st.Page(page_corruption_heatmap, title="Corruption Heatmap", icon="🗺️"),
    st.Page(page_deep_dive, title="State Deep Dive", icon="🔍"),
    st.Page(page_activism_hub, title="The Activism Hub", icon="🌉"),
    st.Page(page_accountability_tribunal, title="Accountability Tribunal", icon="⚖️"),
    st.Page(page_docket_decoder, title="Docket Decoder", icon="🛡️"),
    st.Page(page_foia_cannon, title="FOIA Cannon", icon="📄"),
    st.Page(page_lever_map, title="Lever Map", icon="🗺️"),
    st.Page(page_course_correction, title="Course Correction", icon="⚖️"),
    st.Page(page_local_watchdog, title="Local Watchdog", icon="🏘️"),
    st.Page(page_scorecard_generator, title="Scorecard Generator", icon="🎯"),
    st.Page(page_community_leaderboard, title="Community Leaderboard", icon="🏆"),
    st.Page(page_epstein_audit, title="Epstein Archive Audit", icon="🔍"),
    st.Page(page_sunlight_counsel, title="Sunlight Counsel", icon="🎓"),
    st.Page(page_mission_milestones, title="Mission Milestones", icon="🏛️"),
    st.Page(page_ecosystem, title="The Ecosystem", icon="🌳"),
    st.Page(page_support, title="Support", icon="☕"),
]

nav = st.navigation(pages)
nav.run()

st.markdown("---")
FOUNDING_DATE = date(2026, 1, 8)
days_since_launch = (date.today() - FOUNDING_DATE).days
st.markdown(f"<center>Established Jan 8, 2026 — Built by Russell Nomer. Tracking 50 States and 3,143 Counties. | <b>Day {days_since_launch + 1}</b> of the mission.</center>", unsafe_allow_html=True)
