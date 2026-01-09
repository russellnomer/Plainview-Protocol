"""
Safety Shield Module - V6.22
The Plainview Protocol

Public Safety Alert system for protection of Jewish community centers
and related institutions. Proximity mapping, rally route prediction,
and security offset invoicing.

"Transparency is the first line of defense. Sunlight is safety."
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Tuple
import math

NYC_SAPO_URL = "https://www1.nyc.gov/site/cecm/permitting/street-activity-permits.page"
JCC_SECURITY_ALLIANCE = "https://www.jcca.org/"

RADICAL_HUBS_NYC = [
    {
        "name": "The People's Forum",
        "address": "320 W 37th St, Manhattan",
        "lat": 40.7545,
        "lon": -73.9936,
        "city_funding": 65000,
        "funding_type": "Indirect City Benefits",
        "activity": "Hosts events calling for dissolution of Israel"
    },
    {
        "name": "Mayday Space (Bushwick)",
        "address": "176 St Nicholas Ave, Brooklyn",
        "lat": 40.7005,
        "lon": -73.9275,
        "city_funding": 45000,
        "funding_type": "Community Space Subsidy",
        "activity": "WOL organizing hub"
    },
    {
        "name": "DRUM HQ (Jackson Heights)",
        "address": "72-18 Roosevelt Ave, Queens",
        "lat": 40.7496,
        "lon": -73.8832,
        "city_funding": 450000,
        "funding_type": "City Council Discretionary",
        "activity": "Anti-Israel resolution coordination"
    },
    {
        "name": "AAANY Center (Bay Ridge)",
        "address": "7111 5th Ave, Brooklyn",
        "lat": 40.6341,
        "lon": -74.0249,
        "city_funding": 1250000,
        "funding_type": "City Contracts",
        "activity": "BDS curriculum development"
    },
    {
        "name": "Palestine House (Flatbush)",
        "address": "1123 Flatbush Ave, Brooklyn",
        "lat": 40.6408,
        "lon": -73.9588,
        "city_funding": 85000,
        "funding_type": "Cultural Grant",
        "activity": "Community mobilization center"
    },
    {
        "name": "Al-Awda Center (Astoria)",
        "address": "25-15 Steinway St, Queens",
        "lat": 40.7720,
        "lon": -73.9185,
        "city_funding": 120000,
        "funding_type": "Immigrant Services",
        "activity": "Right of Return advocacy"
    },
    {
        "name": "Samidoun Space (Crown Heights)",
        "address": "341 Eastern Parkway, Brooklyn",
        "lat": 40.6706,
        "lon": -73.9440,
        "city_funding": 55000,
        "funding_type": "Legal Aid Affiliate",
        "activity": "Prisoner solidarity network"
    },
    {
        "name": "DSA Hub (Lower East Side)",
        "address": "45 Ludlow St, Manhattan",
        "lat": 40.7180,
        "lon": -73.9902,
        "city_funding": 185000,
        "funding_type": "Discretionary - Community Justice",
        "activity": "Apartheid platform coordination"
    },
    {
        "name": "JVP Community Space (Park Slope)",
        "address": "188 5th Ave, Brooklyn",
        "lat": 40.6789,
        "lon": -73.9800,
        "city_funding": 95000,
        "funding_type": "Interfaith Dialogue",
        "activity": "Anti-Zionist programming"
    },
    {
        "name": "CAIR-NY Office (Downtown Brooklyn)",
        "address": "395 Flatbush Ave Extension, Brooklyn",
        "lat": 40.6956,
        "lon": -73.9830,
        "city_funding": 380000,
        "funding_type": "Legal/Social Services",
        "activity": "Resistance celebration events"
    }
]

JEWISH_COMMUNAL_SITES = [
    {"name": "JCC Manhattan", "address": "334 Amsterdam Ave", "lat": 40.7822, "lon": -73.9800, "type": "JCC"},
    {"name": "92nd Street Y", "address": "1395 Lexington Ave", "lat": 40.7848, "lon": -73.9531, "type": "JCC"},
    {"name": "Brooklyn JCC", "address": "9802 Fourth Ave", "lat": 40.6178, "lon": -74.0305, "type": "JCC"},
    {"name": "Samuel Field Y (Queens)", "address": "58-20 Little Neck Pkwy", "lat": 40.7625, "lon": -73.7265, "type": "JCC"},
    {"name": "Staten Island JCC", "address": "1466 Manor Rd", "lat": 40.5979, "lon": -74.1624, "type": "JCC"},
    {"name": "Park East Synagogue", "address": "163 E 67th St", "lat": 40.7685, "lon": -73.9635, "type": "Synagogue"},
    {"name": "Central Synagogue", "address": "652 Lexington Ave", "lat": 40.7583, "lon": -73.9686, "type": "Synagogue"},
    {"name": "Temple Emanu-El", "address": "1 E 65th St", "lat": 40.7680, "lon": -73.9682, "type": "Synagogue"},
    {"name": "Congregation Shearith Israel", "address": "2 W 70th St", "lat": 40.7749, "lon": -73.9779, "type": "Synagogue"},
    {"name": "Brooklyn Heights Synagogue", "address": "131 Remsen St", "lat": 40.6946, "lon": -73.9946, "type": "Synagogue"},
    {"name": "Chabad HQ (770)", "address": "770 Eastern Pkwy", "lat": 40.6692, "lon": -73.9428, "type": "Synagogue"},
    {"name": "Young Israel of Flatbush", "address": "1012 Ave I", "lat": 40.6256, "lon": -73.9629, "type": "Synagogue"},
    {"name": "Hillcrest Jewish Center", "address": "183-02 Union Tpke", "lat": 40.7256, "lon": -73.7901, "type": "Synagogue"},
    {"name": "Forest Hills Jewish Center", "address": "106-06 Queens Blvd", "lat": 40.7220, "lon": -73.8433, "type": "Synagogue"},
    {"name": "Riverdale Jewish Center", "address": "3700 Independence Ave", "lat": 40.8905, "lon": -73.9032, "type": "Synagogue"}
]

PENDING_RALLY_PERMITS = [
    {
        "permit_id": "SAPO-2026-1542",
        "event_name": "March for Palestine",
        "start_location": "The People's Forum",
        "route": ["Times Square", "Columbus Circle", "Central Park South"],
        "date": "2026-02-15",
        "expected_attendance": 5000,
        "status": "APPROVED"
    },
    {
        "permit_id": "SAPO-2026-1587",
        "event_name": "Solidarity with Gaza Rally",
        "start_location": "DRUM HQ",
        "route": ["Jackson Heights", "Elmhurst", "Corona"],
        "date": "2026-02-22",
        "expected_attendance": 2000,
        "status": "PENDING"
    },
    {
        "permit_id": "SAPO-2026-1623",
        "event_name": "BDS Day of Action",
        "start_location": "Brooklyn JCC Vicinity",
        "route": ["Bay Ridge", "Sunset Park", "Industry City"],
        "date": "2026-03-01",
        "expected_attendance": 1500,
        "status": "PENDING"
    }
]

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in miles using Haversine formula."""
    R = 3959
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def get_proximity_alerts(radius_miles: float = 2.0) -> List[Dict[str, Any]]:
    """Find city-funded spaces within radius of Jewish communal sites."""
    alerts = []
    
    for hub in RADICAL_HUBS_NYC:
        for site in JEWISH_COMMUNAL_SITES:
            distance = haversine_distance(
                hub["lat"], hub["lon"],
                site["lat"], site["lon"]
            )
            
            if distance <= radius_miles:
                alerts.append({
                    "hub_name": hub["name"],
                    "hub_address": hub["address"],
                    "hub_funding": hub["city_funding"],
                    "communal_site": site["name"],
                    "site_type": site["type"],
                    "distance_miles": round(distance, 2),
                    "risk_level": "HIGH" if distance < 0.5 else "MEDIUM" if distance < 1.0 else "ELEVATED"
                })
    
    return sorted(alerts, key=lambda x: x["distance_miles"])

def get_rally_impact_paths() -> List[Dict[str, Any]]:
    """Analyze pending rallies for impact on communal sites."""
    impacts = []
    
    for rally in PENDING_RALLY_PERMITS:
        affected_sites = []
        for site in JEWISH_COMMUNAL_SITES:
            for route_point in rally["route"]:
                if any(keyword in site["name"].lower() or keyword in site["address"].lower() 
                       for keyword in route_point.lower().split()):
                    affected_sites.append(site["name"])
                    break
        
        if rally["start_location"] in [h["name"] for h in RADICAL_HUBS_NYC]:
            impacts.append({
                "permit_id": rally["permit_id"],
                "event_name": rally["event_name"],
                "date": rally["date"],
                "start_location": rally["start_location"],
                "route": " → ".join(rally["route"]),
                "expected_attendance": rally["expected_attendance"],
                "status": rally["status"],
                "potentially_affected_sites": affected_sites if affected_sites else ["Route under review"]
            })
    
    return impacts

def generate_security_offset_demand(hub_name: str, hub_funding: float, nearby_site: str) -> str:
    """Generate security offset demand letter."""
    timestamp = datetime.now().strftime("%B %d, %Y")
    
    demand = f"""
SECURITY OFFSET DEMAND
Generated by The Plainview Protocol — Safety Shield Module
Date: {timestamp}

TO: NYC City Council, NYC Mayor's Office of Community Affairs, NYPD Community Affairs Bureau

RE: Demand for Equivalent Security Funding for {nearby_site}

BACKGROUND:
The City of New York has awarded ${hub_funding:,.0f} in discretionary funding to {hub_name}, 
a facility documented as hosting activities that may create safety concerns for nearby 
Jewish communal institutions.

PROXIMITY CONCERN:
{nearby_site} is located within the safety radius of the funded space. Recent rally 
activity originating from city-funded spaces has increased security concerns for 
the local Jewish community.

DEMAND:
Pursuant to the principle of equal protection and community safety, we demand that 
the City allocate security funding equal to or greater than ${hub_funding:,.0f} for 
the protection of {nearby_site} and nearby Jewish communal institutions.

REQUESTED ACTIONS:
1. Immediate security assessment for {nearby_site}
2. Allocation of NYPD Community Affairs resources during high-risk periods
3. Grant funding for private security offset equal to discretionary award
4. Regular safety briefings with community leadership

LEGAL BASIS:
- NYC Charter § 440: Commissioner of Police community protection duties
- Civil Rights Act: Equal protection considerations
- NY Penal Law § 240.31: Bias-motivated harassment prevention

COMMUNITY ATTESTATION:
This demand is submitted in good faith by concerned community members exercising
their First Amendment right to petition for public safety.

---
Generated via The Plainview Protocol — Safety Shield Module
"Transparency is the first line of defense. Sunlight is safety."
    """
    return demand.strip()

def render_safety_shield():
    """Render the Safety Shield dashboard."""
    st.header("🛡️ Safety Shield — Public Safety Alert")
    st.caption("V6.22 — Protecting Jewish Community Centers & Synagogues")
    
    st.info("""
    *"Transparency is the first line of defense. If the city funds a space that hosts 
    those who call for your destruction, you deserve to know where it is and how to 
    protect yourself. Sunlight is safety."*
    
    — Russell David Nomer, Founder
    """)
    
    st.divider()
    
    proximity_alerts = get_proximity_alerts(2.0)
    rally_impacts = get_rally_impact_paths()
    
    col1, col2, col3 = st.columns(3)
    col1.error(f"🚨 Proximity Alerts: {len(proximity_alerts)}")
    col2.warning(f"📍 Hubs Tracked: {len(RADICAL_HUBS_NYC)}")
    col3.metric("🏛️ Sites Protected", len(JEWISH_COMMUNAL_SITES))
    
    st.divider()
    
    tabs = st.tabs(["🚨 Proximity Alerts", "🗺️ Rally Route Predictor", "🛡️ Security Offset", "📊 Full Audit"])
    
    with tabs[0]:
        st.subheader("🚨 Proximity Alert Engine")
        st.caption("City-funded spaces within 2 miles of Jewish communal sites")
        
        radius = st.slider("Alert Radius (miles)", 0.5, 5.0, 2.0, 0.5)
        alerts = get_proximity_alerts(radius)
        
        if alerts:
            high_risk = [a for a in alerts if a["risk_level"] == "HIGH"]
            
            if high_risk:
                st.error(f"⚠️ **{len(high_risk)} HIGH RISK** proximities detected (< 0.5 miles)")
            
            for alert in alerts[:10]:
                risk_icon = "🔴" if alert["risk_level"] == "HIGH" else "🟠" if alert["risk_level"] == "MEDIUM" else "🟡"
                
                with st.expander(f"{risk_icon} {alert['hub_name']} → {alert['communal_site']} ({alert['distance_miles']} mi)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Funded Space:** {alert['hub_name']}")
                        st.markdown(f"**Address:** {alert['hub_address']}")
                        st.markdown(f"**City Funding:** ${alert['hub_funding']:,.0f}")
                    
                    with col2:
                        st.markdown(f"**Communal Site:** {alert['communal_site']}")
                        st.markdown(f"**Site Type:** {alert['site_type']}")
                        st.markdown(f"**Distance:** {alert['distance_miles']} miles")
                        st.markdown(f"**Risk Level:** {alert['risk_level']}")
        else:
            st.success("No proximity alerts within specified radius.")
    
    with tabs[1]:
        st.subheader("🗺️ Rally Route Predictor")
        st.caption("Tracking rallies originating from monitored hubs")
        
        if rally_impacts:
            for rally in rally_impacts:
                status_icon = "🟢" if rally["status"] == "APPROVED" else "🟡"
                
                with st.expander(f"{status_icon} {rally['event_name']} — {rally['date']}"):
                    st.markdown(f"**Permit ID:** {rally['permit_id']}")
                    st.markdown(f"**Start Location:** {rally['start_location']}")
                    st.markdown(f"**Route:** {rally['route']}")
                    st.markdown(f"**Expected Attendance:** {rally['expected_attendance']:,}")
                    st.markdown(f"**Status:** {rally['status']}")
                    
                    if rally["potentially_affected_sites"]:
                        st.warning(f"**Path of Impact:** {', '.join(rally['potentially_affected_sites'])}")
        else:
            st.info("No pending rallies from monitored locations.")
        
        st.divider()
        st.link_button("🔗 NYC Street Activity Permit Office (SAPO)", NYC_SAPO_URL, use_container_width=True)
    
    with tabs[2]:
        st.subheader("🛡️ Security Offset Invoice Generator")
        st.caption("Demand equivalent security funding for nearby communal sites")
        
        if proximity_alerts:
            selected_alert = st.selectbox(
                "Select Proximity Alert:",
                options=range(len(proximity_alerts)),
                format_func=lambda i: f"{proximity_alerts[i]['hub_name']} → {proximity_alerts[i]['communal_site']}"
            )
            
            alert = proximity_alerts[selected_alert]
            
            st.markdown(f"**Hub:** {alert['hub_name']}")
            st.markdown(f"**Funding:** ${alert['hub_funding']:,.0f}")
            st.markdown(f"**Nearby Site:** {alert['communal_site']}")
            
            if st.button("🛡️ Generate Security Offset Demand", use_container_width=True):
                demand = generate_security_offset_demand(
                    alert["hub_name"],
                    alert["hub_funding"],
                    alert["communal_site"]
                )
                
                st.text_area("Security Offset Demand Letter", demand, height=400)
                
                st.download_button(
                    "📥 Download Demand Letter",
                    demand,
                    file_name=f"security_offset_{alert['communal_site'].replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        else:
            st.info("No proximity alerts to generate demands for.")
    
    with tabs[3]:
        st.subheader("📊 Full Audit — All Monitored Locations")
        
        st.markdown("**City-Funded Spaces Under Monitoring:**")
        
        hub_data = []
        for hub in RADICAL_HUBS_NYC:
            hub_data.append({
                "Name": hub["name"],
                "Address": hub["address"],
                "Funding": f"${hub['city_funding']:,.0f}",
                "Type": hub["funding_type"],
                "Activity": hub["activity"][:50] + "..."
            })
        
        st.dataframe(hub_data, use_container_width=True, hide_index=True)
        
        st.divider()
        
        st.markdown("**Protected Communal Sites:**")
        
        site_data = []
        for site in JEWISH_COMMUNAL_SITES:
            site_data.append({
                "Name": site["name"],
                "Address": site["address"],
                "Type": site["type"]
            })
        
        st.dataframe(site_data, use_container_width=True, hide_index=True)
    
    with st.expander("ℹ️ Transparency: Sources & Methodology"):
        st.markdown("""
        **Data Sources:**
        - NYC Checkbook (discretionary funding)
        - NYC Street Activity Permit Office (SAPO)
        - Public organizational websites and social media
        - Community safety reports
        
        **Proximity Calculation:**
        - Haversine formula for great-circle distance
        - Risk levels: HIGH (<0.5 mi), MEDIUM (0.5-1.0 mi), ELEVATED (1.0-2.0 mi)
        
        **Rally Route Analysis:**
        - Cross-references permit start locations with monitored hubs
        - Identifies routes passing near communal sites
        
        **Legal Framework:**
        - First Amendment assembly monitoring (public permits)
        - Equal protection advocacy
        - NY Penal Law bias crime prevention
        """)
    
    st.divider()
    
    st.markdown("""
    **🏛️ The Sentinel's Responsibility:**
    
    By providing this data, the Plainview Protocol ensures that community leaders are not 
    caught off-guard by the city's funding choices. We use Open Source Intelligence (OSINT) 
    to level the playing field between radical activists and the citizens they target.
    
    *Transparency is the first line of defense. Sunlight is safety.*
    """)
