"""
Press Kit Generator - V8.7
The Plainview Protocol

One-click fact sheet generation, producer outreach logging,
and media pressure mapping for journalist engagement.

"Journalists need facts, not just feelings."
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any

FACT_SHEET_DATA = {
    "title": "FACT SHEET: Accountability Audit of the Cuomo Administration",
    "subtitle": "Evidence of Senior Life-Safety Mismanagement and 2026 Campaign Transparency",
    "source": "Plainview Protocol Forensic Audit (V8.7)",
    "sections": {
        "march_25_directive": {
            "title": "1. The March 25, 2020 Directive",
            "order": "The NY Department of Health issued an advisory stating that nursing homes 'must admit' or 'readmit' residents even if they tested positive for COVID-19.",
            "restriction": "The order explicitly prohibited facilities from requiring a hospitalized resident, who was determined to be medically stable, to be tested for COVID-19 prior to admission.",
            "impact": "Between March 25 and May 8, 2020 (when the order was rescinded), approximately 6,326 COVID-positive patients were admitted to nursing homes under this directive."
        },
        "undercounting": {
            "title": "2. Undercounting and Data Manipulation",
            "ag_finding": "A January 2021 report by the NY Attorney General found that nursing home deaths were undercounted by approximately 50% because the administration excluded residents who died after being transferred to a hospital.",
            "frozen_data": "Top aides to the Governor reportedly 'froze' or altered a July 2020 health department report to hide the true death toll from state legislators and the public.",
            "book_deal": "During the height of the crisis, the Governor secured a $5.1 million book deal for a memoir on 'leadership,' while his staff worked to suppress the actual casualty figures."
        },
        "audit_demand": {
            "title": "3. The 2026 Audit Demand",
            "financial_scrutiny": "Current demands for a Forensic Audit focus on whether any resources or personnel involved in the 2020-21 data suppression are now connected to the current 2026 political resurgence.",
            "legislative_record": "The Plainview Protocol identifies a 'Spoliation Gap' in public records—thousands of emails and private memos regarding the March 25 directive remain unreleased to the public."
        }
    }
}

NY_NEWS_OUTLETS = [
    {"name": "NY Times", "type": "Print/Digital", "region": "Statewide", "email": "tips@nytimes.com", "status": "Not Contacted"},
    {"name": "NY Post", "type": "Print/Digital", "region": "NYC Metro", "email": "tips@nypost.com", "status": "Not Contacted"},
    {"name": "NY Daily News", "type": "Print/Digital", "region": "NYC Metro", "email": "tips@nydailynews.com", "status": "Not Contacted"},
    {"name": "Newsday", "type": "Print/Digital", "region": "Long Island", "email": "tips@newsday.com", "status": "Not Contacted"},
    {"name": "Times Union (Albany)", "type": "Print/Digital", "region": "Capital Region", "email": "news@timesunion.com", "status": "Not Contacted"},
    {"name": "Buffalo News", "type": "Print/Digital", "region": "Western NY", "email": "tips@buffnews.com", "status": "Not Contacted"},
    {"name": "Syracuse Post-Standard", "type": "Print/Digital", "region": "Central NY", "email": "tips@syracuse.com", "status": "Not Contacted"},
    {"name": "Democrat & Chronicle", "type": "Print/Digital", "region": "Rochester", "email": "tips@democratandchronicle.com", "status": "Not Contacted"},
    {"name": "NY1", "type": "TV News", "region": "NYC Metro", "email": "ny1tips@charter.com", "status": "Not Contacted"},
    {"name": "WABC-TV", "type": "TV News", "region": "NYC Metro", "email": "news@abc7ny.com", "status": "Not Contacted"},
    {"name": "WCBS-TV", "type": "TV News", "region": "NYC Metro", "email": "tips@cbsnews.com", "status": "Not Contacted"},
    {"name": "WNBC-TV", "type": "TV News", "region": "NYC Metro", "email": "tips@nbcuni.com", "status": "Not Contacted"},
    {"name": "PIX11", "type": "TV News", "region": "NYC Metro", "email": "tips@pix11.com", "status": "Not Contacted"},
    {"name": "Spectrum News NY1", "type": "Cable News", "region": "Statewide", "email": "tips@spectrumlocalnews.com", "status": "Not Contacted"},
    {"name": "City & State NY", "type": "Political", "region": "Statewide", "email": "tips@cityandstateny.com", "status": "Not Contacted"}
]

TIMELINE_EVENTS = [
    {"date": "March 25, 2020", "event": "DOH Directive issued requiring nursing homes to accept COVID+ patients"},
    {"date": "May 8, 2020", "event": "Directive rescinded after 6,326 COVID+ admissions"},
    {"date": "July 2020", "event": "Health department report allegedly 'frozen' by top aides"},
    {"date": "October 2020", "event": "$5.1M book deal signed during ongoing crisis"},
    {"date": "January 28, 2021", "event": "NY AG Report reveals 50% undercount of nursing home deaths"},
    {"date": "February 2021", "event": "AP investigation confirms 15,000+ deaths, not 8,500 reported"},
    {"date": "August 24, 2021", "event": "Governor resigns amid scandals"},
    {"date": "2026", "event": "Political resurgence triggers renewed accountability demands"}
]

def generate_fact_sheet_text() -> str:
    """Generate plain text fact sheet for journalists."""
    timestamp = datetime.now().strftime("%B %d, %Y")
    
    fact_sheet = f"""
═══════════════════════════════════════════════════════════════════
{FACT_SHEET_DATA['title'].upper()}
═══════════════════════════════════════════════════════════════════

Subject: {FACT_SHEET_DATA['subtitle']}
Source: {FACT_SHEET_DATA['source']}
Date Generated: {timestamp}

═══════════════════════════════════════════════════════════════════

{FACT_SHEET_DATA['sections']['march_25_directive']['title']}

THE ORDER:
{FACT_SHEET_DATA['sections']['march_25_directive']['order']}

THE RESTRICTION:
{FACT_SHEET_DATA['sections']['march_25_directive']['restriction']}

THE IMPACT:
{FACT_SHEET_DATA['sections']['march_25_directive']['impact']}

═══════════════════════════════════════════════════════════════════

{FACT_SHEET_DATA['sections']['undercounting']['title']}

THE AG FINDING:
{FACT_SHEET_DATA['sections']['undercounting']['ag_finding']}

THE "FROZEN" DATA:
{FACT_SHEET_DATA['sections']['undercounting']['frozen_data']}

THE BOOK DEAL:
{FACT_SHEET_DATA['sections']['undercounting']['book_deal']}

═══════════════════════════════════════════════════════════════════

{FACT_SHEET_DATA['sections']['audit_demand']['title']}

FINANCIAL SCRUTINY:
{FACT_SHEET_DATA['sections']['audit_demand']['financial_scrutiny']}

LEGISLATIVE RECORD:
{FACT_SHEET_DATA['sections']['audit_demand']['legislative_record']}

═══════════════════════════════════════════════════════════════════

TIMELINE OF KEY EVENTS:

"""
    for event in TIMELINE_EVENTS:
        fact_sheet += f"• {event['date']}: {event['event']}\n"
    
    fact_sheet += """
═══════════════════════════════════════════════════════════════════

AUDIT DEMANDS:

1. Full release of all internal DOH communications (March-August 2020)
2. Unredacted emails regarding nursing home admission policy
3. Book deal correspondence and use of state resources
4. Complete accounting of death reporting methodology changes
5. Transparency on 2026 campaign personnel connections to 2020 administration

═══════════════════════════════════════════════════════════════════

FOR MORE INFORMATION:
The Plainview Protocol: plainviewprotocol.com
Senior Justice Trigger: Full civil action templates available
Discovery Tracker: 8 document categories remain MISSING or WITHHELD

═══════════════════════════════════════════════════════════════════

"Journalists need facts, not just feelings. By providing the specific orders 
and report dates, you turn a 'sad story' into a 'breaking investigation.'"

— The Plainview Protocol, Forensic Audit V8.7

═══════════════════════════════════════════════════════════════════
"""
    return fact_sheet.strip()

def generate_producer_email(outlet_name: str, journalist_name: str = "") -> str:
    """Generate email template for news producers."""
    timestamp = datetime.now().strftime("%B %d, %Y")
    
    email = f"""
Subject: FACT SHEET: Forensic Audit of Cuomo Administration — 2026 Accountability Demand

Dear {journalist_name or 'News Producer'},

I am writing to provide your newsroom with verified documentation regarding the 
ongoing accountability demands surrounding Andrew Cuomo's 2026 political activities.

ATTACHED: The Plainview Protocol Fact Sheet (V8.7)

This document contains:
• The exact language of the March 25, 2020 DOH Directive
• The NY Attorney General's January 2021 finding of 50% death undercount
• Timeline of data manipulation allegations
• Current FOIA status of unreleased documents

KEY STORY ANGLE:
Thousands of New York families are now using the Plainview Protocol's "Senior Justice 
Trigger" to demand a forensic audit connecting 2020 data suppression to 2026 campaign 
activities. This is not political opposition—it is documented accountability.

I am available for interview or can connect you with affected families who have 
added their stories to the Victim's Memorial Registry.

Thank you for your commitment to investigative journalism.

Respectfully,
[Your Name]
[Your Contact Information]

---
Fact Sheet generated via The Plainview Protocol
"Journalists need facts, not just feelings."
"""
    return email.strip()

def render_press_kit():
    """Render the Press Kit Generator dashboard."""
    st.header("📄 Press Kit Generator — V8.7")
    st.caption("Journalist Fact Sheets & Producer Outreach Tools")
    
    st.info("""
    *"Journalists need facts, not just feelings. By providing the specific orders 
    and report dates, you turn a 'sad story' into a 'breaking investigation.' 
    Use the Fact Sheet to back them into a corner of truth."*
    
    — Russell David Nomer, Founder
    """)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📰 NY Outlets", len(NY_NEWS_OUTLETS))
    col2.metric("📅 Timeline Events", len(TIMELINE_EVENTS))
    col3.metric("📋 Audit Demands", 5)
    
    st.divider()
    
    tabs = st.tabs(["📄 Fact Sheet", "📧 Producer Outreach", "🗺️ Media Pressure Map", "📅 Timeline"])
    
    with tabs[0]:
        st.subheader("📄 One-Click Journalist Fact Sheet")
        st.caption("Download verified documentation for media outreach")
        
        st.markdown("### Preview:")
        
        with st.expander("1. The March 25, 2020 Directive", expanded=True):
            data = FACT_SHEET_DATA['sections']['march_25_directive']
            st.error(f"**THE ORDER:** {data['order']}")
            st.warning(f"**THE RESTRICTION:** {data['restriction']}")
            st.info(f"**THE IMPACT:** {data['impact']}")
        
        with st.expander("2. Undercounting and Data Manipulation"):
            data = FACT_SHEET_DATA['sections']['undercounting']
            st.error(f"**AG FINDING:** {data['ag_finding']}")
            st.warning(f"**FROZEN DATA:** {data['frozen_data']}")
            st.info(f"**BOOK DEAL:** {data['book_deal']}")
        
        with st.expander("3. The 2026 Audit Demand"):
            data = FACT_SHEET_DATA['sections']['audit_demand']
            st.warning(f"**FINANCIAL SCRUTINY:** {data['financial_scrutiny']}")
            st.info(f"**LEGISLATIVE RECORD:** {data['legislative_record']}")
        
        st.divider()
        
        fact_sheet_text = generate_fact_sheet_text()
        
        st.download_button(
            "📄 Download Journalist Fact Sheet",
            fact_sheet_text,
            file_name="plainview_protocol_fact_sheet_v87.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with tabs[1]:
        st.subheader("📧 Producer Outreach Log")
        st.caption("Track which newsrooms have received the Fact Sheet")
        
        if "outreach_log" not in st.session_state:
            st.session_state.outreach_log = {}
        
        st.markdown("**Generate Email for Outlet:**")
        
        selected_outlet = st.selectbox(
            "Select News Outlet:",
            options=range(len(NY_NEWS_OUTLETS)),
            format_func=lambda i: f"{NY_NEWS_OUTLETS[i]['name']} ({NY_NEWS_OUTLETS[i]['region']})"
        )
        
        outlet = NY_NEWS_OUTLETS[selected_outlet]
        journalist_name = st.text_input("Journalist/Producer Name (optional)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Type:** {outlet['type']}")
            st.markdown(f"**Email:** {outlet['email']}")
        with col2:
            st.markdown(f"**Region:** {outlet['region']}")
            status = st.session_state.outreach_log.get(outlet['name'], "Not Contacted")
            st.markdown(f"**Status:** {status}")
        
        if st.button("📧 Generate Producer Email", use_container_width=True):
            email = generate_producer_email(outlet['name'], journalist_name)
            st.text_area("Email Template", email, height=350)
            
            st.download_button(
                "📥 Download Email",
                email,
                file_name=f"producer_email_{outlet['name'].replace(' ', '_')}.txt",
                mime="text/plain"
            )
        
        st.divider()
        
        st.markdown("**Update Outreach Status:**")
        new_status = st.selectbox(
            "Mark as:",
            ["Not Contacted", "Email Sent", "Responded", "Interview Scheduled", "Story Published"]
        )
        
        if st.button("✅ Update Status"):
            st.session_state.outreach_log[outlet['name']] = new_status
            st.success(f"Updated {outlet['name']} to: {new_status}")
    
    with tabs[2]:
        st.subheader("🗺️ Media Pressure Map")
        st.caption("Tracking coverage of the audit demand across New York")
        
        regions = {}
        for outlet in NY_NEWS_OUTLETS:
            region = outlet['region']
            if region not in regions:
                regions[region] = {"total": 0, "contacted": 0}
            regions[region]["total"] += 1
            if st.session_state.get("outreach_log", {}).get(outlet['name']) in ["Email Sent", "Responded", "Interview Scheduled", "Story Published"]:
                regions[region]["contacted"] += 1
        
        st.markdown("**Coverage by Region:**")
        
        for region, counts in regions.items():
            pct = (counts['contacted'] / counts['total']) * 100 if counts['total'] > 0 else 0
            st.progress(pct / 100, text=f"{region}: {counts['contacted']}/{counts['total']} outlets ({pct:.0f}%)")
        
        st.divider()
        
        contacted_count = sum(1 for o in NY_NEWS_OUTLETS if st.session_state.get("outreach_log", {}).get(o['name']) in ["Email Sent", "Responded", "Interview Scheduled", "Story Published"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Outlets Contacted", contacted_count)
        col2.metric("Total Outlets", len(NY_NEWS_OUTLETS))
        col3.metric("Coverage %", f"{(contacted_count/len(NY_NEWS_OUTLETS))*100:.0f}%")
        
        st.info("💡 **Goal:** Contact all 15 major NY news outlets with the Fact Sheet to maximize audit demand coverage.")
    
    with tabs[3]:
        st.subheader("📅 Timeline of Key Events")
        st.caption("Chronological evidence for journalists")
        
        for event in TIMELINE_EVENTS:
            icon = "🔴" if "Directive" in event['event'] or "undercount" in event['event'] else "🟡" if "froze" in event['event'] or "book" in event['event'] else "🔵"
            st.markdown(f"{icon} **{event['date']}:** {event['event']}")
    
    with st.expander("ℹ️ Transparency: Press Kit Guidelines"):
        st.markdown("""
        **Why This Works:**
        By attaching this Fact Sheet to your email, you are doing the journalist's 
        work for them, making it nearly impossible for a producer to ignore the story. 
        You are providing the evidentiary integrity that defines the Plainview Protocol.
        
        **Best Practices:**
        - Attach the Fact Sheet to all media outreach
        - Follow up within 48 hours if no response
        - Offer to connect journalists with affected families
        - Track all outreach in the Producer Log
        
        **Verification:**
        All facts are sourced from public records:
        - NY DOH Advisory (March 25, 2020)
        - NY AG Report (January 28, 2021)
        - Associated Press Investigation (February 2021)
        - Public book deal disclosures
        """)
    
    st.divider()
    
    st.markdown("""
    **🏛️ Weaponizing the Truth:**
    
    By providing verified facts to journalists, you transform personal grief into 
    investigative leads. The Fact Sheet ensures that every newsroom in New York 
    has the documentation needed to pursue the accountability story.
    
    *Journalists need facts, not just feelings.*
    """)
