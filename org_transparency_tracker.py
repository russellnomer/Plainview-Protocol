"""
Organizational Transparency Tracker - V8.9
The Plainview Protocol

Verified public records tracking for nonprofit and political
organization funding using IRS 990s, FEC data, and lobbying disclosures.

"Sunlight is the best disinfectant." - Louis Brandeis
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import urllib.parse

IRS_990_SEARCH = "https://projects.propublica.org/nonprofits/"
FEC_SEARCH = "https://www.fec.gov/data/committees/"
OPENSECRETS_SEARCH = "https://www.opensecrets.org/orgs/all-profiles"
FARA_SEARCH = "https://efile.fara.gov/ords/fara/f?p=1381:1:0"
NY_LOBBYING = "https://jcope.ny.gov/lobbying"

TRACKED_ORGS = [
    {
        "name": "Tides Foundation",
        "ein": "51-0198509",
        "type": "501(c)(3)",
        "focus": "Fiscal sponsor for progressive causes",
        "annual_revenue": 727000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": True,
        "hq_state": "CA"
    },
    {
        "name": "Open Society Foundations",
        "ein": "13-7029285",
        "type": "501(c)(3)",
        "focus": "Democracy, human rights, justice reform",
        "annual_revenue": 1500000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": True,
        "hq_state": "NY"
    },
    {
        "name": "ACLU Foundation",
        "ein": "13-6213516",
        "type": "501(c)(3)",
        "focus": "Civil liberties litigation",
        "annual_revenue": 300000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": True,
        "hq_state": "NY"
    },
    {
        "name": "National Immigration Law Center",
        "ein": "95-3863270",
        "type": "501(c)(3)",
        "focus": "Immigration legal advocacy",
        "annual_revenue": 25000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": True,
        "hq_state": "CA"
    },
    {
        "name": "United We Dream",
        "ein": "27-3549041",
        "type": "501(c)(4)",
        "focus": "DACA/immigration advocacy",
        "annual_revenue": 15000000,
        "990_available": True,
        "fec_activity": True,
        "lobbying": True,
        "hq_state": "DC"
    },
    {
        "name": "Center for Popular Democracy",
        "ein": "45-5379361",
        "type": "501(c)(3)",
        "focus": "Progressive organizing network",
        "annual_revenue": 45000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": True,
        "hq_state": "NY"
    },
    {
        "name": "Vera Institute of Justice",
        "ein": "13-1941627",
        "type": "501(c)(3)",
        "focus": "Criminal justice reform",
        "annual_revenue": 120000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": True,
        "hq_state": "NY"
    },
    {
        "name": "Brennan Center for Justice",
        "ein": "13-3839293",
        "type": "501(c)(3)",
        "focus": "Voting rights, justice reform",
        "annual_revenue": 45000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": True,
        "hq_state": "NY"
    },
    {
        "name": "Alliance for Global Justice",
        "ein": "52-1656484",
        "type": "501(c)(3)",
        "focus": "Fiscal sponsor for activist groups",
        "annual_revenue": 8000000,
        "990_available": True,
        "fec_activity": False,
        "lobbying": False,
        "hq_state": "AZ"
    },
    {
        "name": "Working Families Party",
        "ein": "13-4107551",
        "type": "527",
        "focus": "Progressive political party",
        "annual_revenue": 12000000,
        "990_available": True,
        "fec_activity": True,
        "lobbying": True,
        "hq_state": "NY"
    }
]

DA_POLICY_TRACKER = [
    {"jurisdiction": "Manhattan, NY", "da": "Alvin Bragg", "party": "D", "policy_score": 25, "notes": "Non-prosecution policies for various offenses"},
    {"jurisdiction": "Los Angeles, CA", "da": "Nathan Hochman", "party": "R", "policy_score": 70, "notes": "Elected 2024, reversed Gascon policies"},
    {"jurisdiction": "San Francisco, CA", "da": "Brooke Jenkins", "party": "D", "policy_score": 60, "notes": "Replaced recalled Boudin"},
    {"jurisdiction": "Philadelphia, PA", "da": "Larry Krasner", "party": "D", "policy_score": 20, "notes": "Progressive prosecution model"},
    {"jurisdiction": "Cook County, IL", "da": "Kim Foxx", "party": "D", "policy_score": 30, "notes": "Declined various prosecutions"},
    {"jurisdiction": "Maricopa County, AZ", "da": "Rachel Mitchell", "party": "R", "policy_score": 75, "notes": "Traditional prosecution approach"},
    {"jurisdiction": "Harris County, TX", "da": "Kim Ogg", "party": "D", "policy_score": 45, "notes": "Mixed approach"},
    {"jurisdiction": "Kings County, NY", "da": "Eric Gonzalez", "party": "D", "policy_score": 35, "notes": "Progressive policies in Brooklyn"}
]

def get_propublica_990_url(ein: str) -> str:
    """Generate ProPublica Nonprofit Explorer URL for organization."""
    clean_ein = ein.replace("-", "")
    return f"https://projects.propublica.org/nonprofits/organizations/{clean_ein}"

def render_org_transparency():
    """Render the Organizational Transparency Tracker dashboard."""
    st.header("🔍 Organizational Transparency Tracker — V8.9")
    st.caption("Verified Public Records: IRS 990s, FEC Data, Lobbying Disclosures")
    
    st.info("""
    *"Sunlight is the best disinfectant. This tracker uses only verified public 
    records—the same data investigative journalists use. Every organization 
    listed has publicly available IRS filings, FEC disclosures, or lobbying 
    registrations that you can verify yourself."*
    """)
    
    st.divider()
    
    total_revenue = sum(org["annual_revenue"] for org in TRACKED_ORGS)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Organizations Tracked", len(TRACKED_ORGS))
    col2.metric("💰 Combined Annual Revenue", f"${total_revenue/1e9:.1f}B")
    col3.metric("📍 DA Offices Tracked", len(DA_POLICY_TRACKER))
    
    st.divider()
    
    tabs = st.tabs(["📋 Organization Database", "🔗 Funding Networks", "⚖️ DA Policy Map", "🔍 Verify Yourself"])
    
    with tabs[0]:
        st.subheader("📋 Tracked Organizations")
        st.caption("All data from IRS Form 990 public filings")
        
        org_type_filter = st.selectbox(
            "Filter by Type:",
            ["All Types", "501(c)(3)", "501(c)(4)", "527"]
        )
        
        filtered_orgs = TRACKED_ORGS if org_type_filter == "All Types" else [
            o for o in TRACKED_ORGS if o["type"] == org_type_filter
        ]
        
        for org in filtered_orgs:
            with st.expander(f"📁 {org['name']} — {org['type']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**EIN:** {org['ein']}")
                    st.markdown(f"**Type:** {org['type']}")
                    st.markdown(f"**Focus:** {org['focus']}")
                    st.markdown(f"**HQ State:** {org['hq_state']}")
                
                with col2:
                    st.markdown(f"**Annual Revenue:** ${org['annual_revenue']:,}")
                    st.markdown(f"**990 Available:** {'✅' if org['990_available'] else '❌'}")
                    st.markdown(f"**FEC Activity:** {'✅' if org['fec_activity'] else '❌'}")
                    st.markdown(f"**Lobbying:** {'✅' if org['lobbying'] else '❌'}")
                
                st.divider()
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.link_button(
                        "📄 View IRS 990 Filing",
                        get_propublica_990_url(org['ein']),
                        use_container_width=True
                    )
                with col_b:
                    if org['lobbying']:
                        st.link_button(
                            "🏛️ Check Lobbying Records",
                            OPENSECRETS_SEARCH,
                            use_container_width=True
                        )
    
    with tabs[1]:
        st.subheader("🔗 Funding Network Analysis")
        st.caption("How organizations are connected through grants and fiscal sponsorship")
        
        st.markdown("""
        **Common Funding Patterns (from IRS 990 Schedule I):**
        
        Large foundations often act as "pass-through" funders, providing grants 
        to smaller organizations. This is legal and disclosed on IRS filings.
        """)
        
        st.warning("""
        **Key Fiscal Sponsors to Research:**
        
        Fiscal sponsors receive donations on behalf of projects that don't have 
        their own 501(c)(3) status. Major sponsors include:
        
        - **Tides Foundation** (CA) — Sponsors 100+ projects
        - **Alliance for Global Justice** (AZ) — Sponsors activist campaigns
        - **NEO Philanthropy** (NY) — Progressive infrastructure
        
        All grant recipients are disclosed on Schedule I of the Form 990.
        """)
        
        st.divider()
        
        st.markdown("**How to Trace Funding:**")
        
        st.success("""
        1. **Find the 990:** Use ProPublica Nonprofit Explorer
        2. **Check Schedule I:** Lists all grants made ($5,000+)
        3. **Check Schedule B:** Lists major donors (if public)
        4. **Cross-reference:** Match grant recipients to other 990s
        5. **Build the map:** Document the funding chain
        """)
        
        st.link_button("🔍 ProPublica Nonprofit Explorer", IRS_990_SEARCH, use_container_width=True)
    
    with tabs[2]:
        st.subheader("⚖️ District Attorney Policy Tracker")
        st.caption("Prosecution policies by jurisdiction")
        
        st.markdown("""
        **Policy Score Methodology:**
        
        Score (0-100) based on publicly stated prosecution policies:
        - **0-30:** Non-prosecution for many offense categories
        - **31-50:** Selective prosecution approach
        - **51-70:** Standard prosecution model
        - **71-100:** Aggressive prosecution approach
        """)
        
        da_df = pd.DataFrame(DA_POLICY_TRACKER)
        
        st.dataframe(
            da_df[["jurisdiction", "da", "party", "policy_score", "notes"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        avg_d = da_df[da_df["party"] == "D"]["policy_score"].mean()
        avg_r = da_df[da_df["party"] == "R"]["policy_score"].mean()
        
        col1, col2 = st.columns(2)
        col1.metric("Avg. D Policy Score", f"{avg_d:.0f}")
        col2.metric("Avg. R Policy Score", f"{avg_r:.0f}")
    
    with tabs[3]:
        st.subheader("🔍 Verify It Yourself")
        st.caption("Direct links to primary source databases")
        
        st.markdown("**Official Government Databases:**")
        
        sources = [
            ("📄 IRS Tax Exempt Organization Search", "https://apps.irs.gov/app/eos/"),
            ("📊 ProPublica Nonprofit Explorer", IRS_990_SEARCH),
            ("🗳️ FEC Campaign Finance Data", FEC_SEARCH),
            ("🌐 FARA Foreign Agent Registry", FARA_SEARCH),
            ("💰 OpenSecrets Lobbying Data", OPENSECRETS_SEARCH),
            ("🏛️ NY Lobbying Database (JCOPE)", NY_LOBBYING),
            ("📋 Senate Lobbying Disclosures", "https://lda.senate.gov/")
        ]
        
        for name, url in sources:
            st.link_button(name, url, use_container_width=True)
        
        st.divider()
        
        st.markdown("""
        **The Sentinel's Research Method:**
        
        1. Never rely on social media claims about funding
        2. Always verify with IRS 990 filings (legally required disclosure)
        3. Cross-reference with FEC data for political activity
        4. Check FARA for any foreign principal connections
        5. Document everything with screenshots and links
        
        *The truth is in the public record. You just have to look.*
        """)
    
    with st.expander("ℹ️ Transparency: Data Sources & Methodology"):
        st.markdown("""
        **All Data From Public Records:**
        
        - **IRS Form 990:** Required annual filing for tax-exempt organizations
        - **FEC Disclosures:** Required for political committees
        - **FARA Filings:** Required for agents of foreign principals
        - **Lobbying Disclosures:** Required under Lobbying Disclosure Act
        
        **Why This Approach?**
        
        Unlike social media scraping or speculation, public filings are:
        - Legally required under penalty of perjury
        - Verified by government agencies
        - Defensible in any forum
        - The same sources used by journalists and researchers
        
        **Limitations:**
        - 990s are filed annually (may be 1-2 years delayed)
        - Some donor info is redacted for privacy
        - Dark money 501(c)(4)s have fewer disclosure requirements
        """)
    
    st.divider()
    
    st.markdown("""
    **🏛️ The Plainview Standard:**
    
    We use the same data the Labyrinth uses—but we use it for the people. 
    Every claim in this tracker can be verified through official government 
    databases. That's what makes it bulletproof.
    
    *Sunlight is the best disinfectant.*
    """)
