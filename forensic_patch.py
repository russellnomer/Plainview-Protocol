"""
Forensic Patch for The Plainview Protocol V8.3

Routing fixes and session state management for reliable navigation.

Features:
- Catch-all route handler redirecting invalid URLs to Mission Control
- Session state exclusive navigation
- Deep Dive dropdown index fix for all 62 NY counties
"""

import streamlit as st
from typing import List, Optional, Dict, Any

VALID_PAGES = [
    "Mission Control",
    "The National Lens", 
    "The 2027 Fork",
    "Trade & Industry",
    "DOGE Scrutiny Hub",
    "Corruption Heatmap",
    "State Deep Dive",
    "The Activism Hub",
    "Accountability Tribunal",
    "Docket Decoder",
    "FOIA Cannon",
    "Sentinel Training",
    "Lever Map",
    "Course Correction",
    "Local Watchdog",
    "Scorecard Generator",
    "Community Leaderboard",
    "Citizen Reel",
    "Foreign Influence",
    "FARA Reporter",
    "Shadow Watch",
    "Revolving Door",
    "Ethics Reporter",
    "Epstein Archive Audit",
    "Agency Portal",
    "Sunlight Counsel",
    "Mission Milestones",
    "The Ecosystem",
    "Support",
    "Audit Logs",
    "Protocol Pulse"
]

NY_COUNTIES_COMPLETE = [
    "Albany County", "Allegany County", "Bronx County", "Broome County",
    "Cattaraugus County", "Cayuga County", "Chautauqua County", "Chemung County",
    "Chenango County", "Clinton County", "Columbia County", "Cortland County",
    "Delaware County", "Dutchess County", "Erie County", "Essex County",
    "Franklin County", "Fulton County", "Genesee County", "Greene County",
    "Hamilton County", "Herkimer County", "Jefferson County", "Kings County",
    "Lewis County", "Livingston County", "Madison County", "Monroe County",
    "Montgomery County", "Nassau County", "New York County", "New York City (5 Boroughs)",
    "Niagara County", "Oneida County", "Onondaga County", "Ontario County",
    "Orange County", "Orleans County", "Oswego County", "Otsego County",
    "Putnam County", "Queens County", "Rensselaer County", "Richmond County",
    "Rockland County", "St. Lawrence County", "Saratoga County", "Schenectady County",
    "Schoharie County", "Schuyler County", "Seneca County", "Steuben County",
    "Suffolk County", "Sullivan County", "Tioga County", "Tompkins County",
    "Ulster County", "Warren County", "Washington County", "Wayne County",
    "Westchester County", "Wyoming County", "Yates County"
]


def init_routing_state():
    """Initialize session state for navigation."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Mission Control"
    
    if 'deep_dive_state' not in st.session_state:
        st.session_state.deep_dive_state = None
    
    if 'selected_county_index' not in st.session_state:
        st.session_state.selected_county_index = 0
    
    if 'navigation_history' not in st.session_state:
        st.session_state.navigation_history = []
    
    if 'last_valid_page' not in st.session_state:
        st.session_state.last_valid_page = "Mission Control"


def validate_page_route(page_name: str) -> bool:
    """Validate that a page exists in the valid pages list."""
    return page_name in VALID_PAGES


def safe_navigate(page_name: str) -> str:
    """
    Safe navigation with fallback to Mission Control.
    Returns the actual page to navigate to.
    """
    if validate_page_route(page_name):
        st.session_state.current_page = page_name
        st.session_state.last_valid_page = page_name
        st.session_state.navigation_history.append(page_name)
        if len(st.session_state.navigation_history) > 50:
            st.session_state.navigation_history = st.session_state.navigation_history[-50:]
        return page_name
    else:
        st.session_state.current_page = "Mission Control"
        return "Mission Control"


def catch_all_redirect():
    """
    Catch-all handler that redirects invalid routes to Mission Control.
    Call this at the start of your main app.
    """
    init_routing_state()
    
    current = st.session_state.get('current_page', 'Mission Control')
    
    if not validate_page_route(current):
        st.session_state.current_page = "Mission Control"
        st.warning(f"Page '{current}' not found. Redirecting to Mission Control.")
        st.rerun()


def get_county_index(county_name: str, county_list: List[str]) -> int:
    """
    Get the index of a county in a list, with fallback to 0.
    Fixes dropdown index issues for all 62 NY counties.
    """
    try:
        return county_list.index(county_name)
    except ValueError:
        return 0


def safe_county_selectbox(label: str, county_data: Dict[str, Any], 
                          key: str = None) -> Optional[str]:
    """
    Safe county selectbox with index persistence.
    Ensures Chemung and all 62 NY counties work correctly.
    """
    county_list = list(county_data.keys())
    
    session_key = f"county_index_{key}" if key else "county_index_default"
    if session_key not in st.session_state:
        st.session_state[session_key] = 0
    
    current_index = st.session_state[session_key]
    if current_index >= len(county_list):
        current_index = 0
    
    selected = st.selectbox(
        label,
        county_list,
        index=current_index,
        key=key
    )
    
    if selected:
        new_index = get_county_index(selected, county_list)
        st.session_state[session_key] = new_index
    
    return selected


def set_deep_dive_state(state_abbrev: str):
    """Set the deep dive state for state-level analysis."""
    st.session_state.deep_dive_state = state_abbrev


def clear_deep_dive_state():
    """Clear the deep dive state and return to national view."""
    st.session_state.deep_dive_state = None


def get_navigation_breadcrumb() -> str:
    """Get a breadcrumb string for current navigation."""
    history = st.session_state.get('navigation_history', [])
    if len(history) >= 2:
        return f"{history[-2]} > {history[-1]}"
    elif history:
        return history[-1]
    return "Mission Control"


def render_back_button(fallback_page: str = "Mission Control"):
    """Render a back button that uses navigation history."""
    history = st.session_state.get('navigation_history', [])
    
    if len(history) > 1:
        previous_page = history[-2]
        if st.button(f"← Back to {previous_page}"):
            st.session_state.navigation_history.pop()
            st.session_state.current_page = previous_page
            st.rerun()
    else:
        if st.button(f"← Back to {fallback_page}"):
            safe_navigate(fallback_page)
            st.rerun()


def verify_county_data_integrity(county_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify county data integrity and fill missing fields.
    Ensures all 62 NY counties have required fields.
    """
    required_fields = [
        'leader', 'population', 'total_debt', 'no_bid_contracts',
        'transparency_score', 'live_stream', 'searchable_portal',
        'timely_minutes', 'foil_responsive', 'sanctuary_policy',
        'notes', 'osc_link'
    ]
    
    defaults = {
        'leader': 'Unknown',
        'population': 0,
        'total_debt': 0,
        'no_bid_contracts': 0,
        'transparency_score': 50,
        'live_stream': False,
        'searchable_portal': False,
        'timely_minutes': False,
        'foil_responsive': True,
        'sanctuary_policy': False,
        'notes': 'Data pending verification',
        'osc_link': 'https://wwe2.osc.state.ny.us/transparency/LocalGov/LocalGovIntro.cfm'
    }
    
    verified_data = {}
    for county, data in county_data.items():
        county_entry = {}
        for field in required_fields:
            county_entry[field] = data.get(field, defaults[field])
        verified_data[county] = county_entry
    
    return verified_data
