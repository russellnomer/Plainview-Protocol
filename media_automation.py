"""
Media Automation Hub - V8.8
The Plainview Protocol

Press Blast mailto generator, independent media database,
and one-click media outreach tools.

"One email is a complaint; ten thousand emails is a movement."
"""

import streamlit as st
import json
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any

def load_media_targets() -> Dict[str, Any]:
    """Load media targets from JSON file."""
    try:
        with open("media_targets.json", "r") as f:
            return json.load(f)
    except Exception:
        return {"mainstream_networks": [], "independent_media": [], "email_template": {}}

def generate_mailto_link(
    to_emails: List[str],
    bcc_emails: List[str],
    subject: str,
    body: str
) -> str:
    """Generate mailto link with pre-filled fields."""
    params = {
        "subject": subject,
        "body": body
    }
    
    if bcc_emails:
        params["bcc"] = ",".join(bcc_emails)
    
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    to_str = ",".join(to_emails) if to_emails else ""
    
    return f"mailto:{to_str}?{query}"

def generate_press_blast_body(
    name: str,
    location: str,
    relationship: str,
    deceased_name: str,
    facility_name: str
) -> str:
    """Generate personalized press blast email body."""
    body = f"""ATTN: Investigative Producer / Assignment Desk,

My name is {name}, and I am a resident of {location}.

In 2020, I lost my {relationship}, {deceased_name}, at {facility_name} following the state's March 25th directive. For years, my family has been a statistic—a number hidden by an administration that prioritized book deals over transparency.

Today, as Andrew Cuomo launches his 2026 comeback, I am not just grieving; I am auditing.

I have registered my loved one on the Plainview Protocol Victim's Memorial Registry, a forensic database of those lost to mismanagement. We are demanding a full audit of the 2026 Campaign Funds to ensure no resources from the 2020-21 "cover-up" era are being used to fuel this political resurgence.

Key Facts:
- The March 25, 2020 DOH Directive required nursing homes to admit COVID+ patients
- The Jan 2021 AG Report found deaths were undercounted by approximately 50%
- Thousands of internal communications remain unreleased

We are ready to go on record. We have the receipts, and we have the numbers. Will you help us ask the question?

Respectfully,
{name}
Member, The 3,143 County Sentinels
plainviewprotocol.com"""
    return body

def render_media_automation():
    """Render the Media Automation Hub dashboard."""
    st.header("📧 Media Automation Hub — V8.8")
    st.caption("One-Click Press Blast & Independent Media Database")
    
    st.info("""
    *"The mainstream media ignored us in 2020. They can't ignore us now if we 
    flood their inboxes with the truth. One email is a complaint; ten thousand 
    emails is a movement. Send it."*
    
    — Russell David Nomer, Founder
    """)
    
    st.divider()
    
    media_data = load_media_targets()
    mainstream = media_data.get("mainstream_networks", [])
    independent = media_data.get("independent_media", [])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📺 Major Networks", len(mainstream))
    col2.metric("📰 Independent Outlets", len(independent))
    col3.metric("📧 Total Contacts", len(mainstream) + len(independent))
    
    st.divider()
    
    tabs = st.tabs(["📧 Press Blast", "📰 Independent Media", "📋 Email Preview"])
    
    with tabs[0]:
        st.subheader("📧 Press Blast — One-Click Media Contact")
        st.caption("Send your story to all major NY networks simultaneously")
        
        st.warning("**How it works:** Fill in your details below, then click the button to open your email client with everything pre-filled. The network emails will be in BCC to protect your privacy.")
        
        with st.form("press_blast_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name")
                location = st.text_input("Your Borough/Town")
                relationship = st.selectbox(
                    "Relationship to Loved One",
                    ["Mother", "Father", "Grandmother", "Grandfather", "Spouse", "Aunt", "Uncle"]
                )
            
            with col2:
                deceased_name = st.text_input("Loved One's Name")
                facility_name = st.text_input("Nursing Home Facility")
            
            submitted = st.form_submit_button("🚀 Prepare Press Blast", use_container_width=True)
        
        if submitted and name and deceased_name:
            subject = "[URGENT] New Evidence: Families of COVID Victims Demand Audit of Cuomo 2026 Campaign"
            body = generate_press_blast_body(
                name,
                location or "New York",
                relationship,
                deceased_name,
                facility_name or "[Facility Name]"
            )
            
            bcc_list = []
            for network in mainstream:
                bcc_list.extend(network.get("emails", []))
            
            mailto_url = generate_mailto_link([], bcc_list, subject, body)
            
            st.success("✅ Press Blast ready! Click below to open your email client.")
            
            st.markdown(f"""
            <a href="{mailto_url}" target="_blank" style="
                display: inline-block;
                padding: 15px 30px;
                background-color: #dc3545;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 18px;
                text-align: center;
                width: 100%;
            ">📧 SEND PRESS BLAST TO ALL NETWORKS</a>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            st.markdown("**Networks included in BCC:**")
            for network in mainstream:
                st.markdown(f"- {network['name']}")
    
    with tabs[1]:
        st.subheader("📰 Independent Media Database")
        st.caption("Friendly outlets covering NY corruption and accountability")
        
        search_query = st.text_input("🔍 Search outlets...", placeholder="e.g., Substack, podcast, investigative")
        
        platform_filter = st.selectbox(
            "Filter by Platform:",
            ["All Platforms"] + list(set(m.get("platform", "Unknown") for m in independent))
        )
        
        filtered_media = independent
        if search_query:
            filtered_media = [m for m in filtered_media if 
                search_query.lower() in m.get("name", "").lower() or
                search_query.lower() in m.get("focus", "").lower() or
                search_query.lower() in m.get("platform", "").lower()
            ]
        
        if platform_filter != "All Platforms":
            filtered_media = [m for m in filtered_media if m.get("platform") == platform_filter]
        
        for outlet in filtered_media:
            with st.expander(f"📰 {outlet['name']} — {outlet.get('platform', 'Unknown')}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Type:** {outlet.get('type', 'Unknown')}")
                    st.markdown(f"**Focus:** {outlet.get('focus', 'N/A')}")
                    st.markdown(f"**Contact:** {outlet.get('contact', 'N/A')}")
                
                with col2:
                    contact = outlet.get('contact', '')
                    if '@' in contact and 'via' not in contact.lower():
                        st.code(contact)
                        
                        subject = "[URGENT] Families of COVID Victims Demand Audit"
                        mailto = f"mailto:{contact}?subject={urllib.parse.quote(subject)}"
                        st.link_button("📧 Contact", mailto, use_container_width=True)
        
        if not filtered_media:
            st.info("No outlets match your search criteria.")
    
    with tabs[2]:
        st.subheader("📋 Full Email Preview")
        st.caption("Review before sending")
        
        preview_name = st.text_input("Your Name", key="preview_name", value="[Your Name]")
        preview_location = st.text_input("Location", key="preview_loc", value="[Your Town]")
        preview_relationship = st.text_input("Relationship", key="preview_rel", value="[Mother/Father]")
        preview_deceased = st.text_input("Deceased Name", key="preview_dec", value="[Loved One]")
        preview_facility = st.text_input("Facility", key="preview_fac", value="[Nursing Home]")
        
        full_body = generate_press_blast_body(
            preview_name,
            preview_location,
            preview_relationship,
            preview_deceased,
            preview_facility
        )
        
        st.text_area("Email Body:", full_body, height=400)
        
        st.download_button(
            "📥 Download Email Template",
            full_body,
            file_name="press_blast_email.txt",
            mime="text/plain"
        )
    
    with st.expander("ℹ️ Transparency: Media Outreach Guidelines"):
        st.markdown("""
        **Why BCC?**
        Using BCC (Blind Carbon Copy) protects your privacy and prevents 
        networks from seeing each other's addresses, which is standard 
        practice for mass media outreach.
        
        **Email Addresses Used:**
        All email addresses are publicly available assignment desk and 
        tip line contacts published by the networks themselves.
        
        **Best Practices:**
        - Personalize your story with specific details
        - Attach the Fact Sheet from the Press Kit page
        - Follow up if no response within 48 hours
        - Track your outreach in the Producer Log
        
        **Legal Note:**
        Sending unsolicited emails to public tip lines is protected 
        free speech. All statements should be factual and documented.
        """)
    
    st.divider()
    
    st.markdown("""
    **🏛️ The Sentinel's Megaphone:**
    
    The mainstream media missed the story in 2020. With thousands of families 
    sending personalized, fact-backed emails, they cannot miss it in 2026. 
    Your voice, combined with verified data, becomes undeniable.
    
    *One email is a complaint; ten thousand emails is a movement.*
    """)
