"""
ICE Shield Module - V6.27
The Plainview Protocol

Stand with ICE support module with one-click gratitude emails
to DHS Public Engagement, plus digital badge generator.

"The mob has bullhorns; we have numbers."
"""

import streamlit as st
import urllib.parse
from datetime import datetime
from typing import Dict, Any
from badge_generator import get_badge_bytes

DHS_EMAILS = ["PublicEngagement@ice.dhs.gov", "Secretary@dhs.gov"]

SUPPORT_TEMPLATE = """To the Men and Women of ICE,

While the media amplifies the mob, I am writing to amplify the truth: You are the shield that protects our sovereignty.

I stand with the agents who are forced to make split-second decisions to protect themselves and enforce our nation's laws. Lawful enforcement is not persecution, and those who resist lawful orders bear responsibility for their choices.

Do not back down. Do not apologize for doing your job. The 3,143 County Sentinels have your back.

Respectfully,
{name}
{city}, {state}

---
Sent via The Plainview Protocol
plainviewprotocol.com"""

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming", "District of Columbia"
]

def get_support_counter() -> int:
    """Get current support counter value."""
    if "ice_support_counter" not in st.session_state:
        st.session_state.ice_support_counter = 1776
    return st.session_state.ice_support_counter

def increment_counter():
    """Increment the support counter."""
    if "ice_support_counter" not in st.session_state:
        st.session_state.ice_support_counter = 1776
    st.session_state.ice_support_counter += 1

def generate_mailto_link(name: str, city: str, state: str) -> str:
    """Generate mailto link with pre-filled support email."""
    body = SUPPORT_TEMPLATE.format(name=name, city=city, state=state)
    
    params = {
        "subject": "THANK YOU for Holding the Line (Citizen Support)",
        "body": body
    }
    
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    to_str = ",".join(DHS_EMAILS)
    
    return f"mailto:{to_str}?{query}"

SOCIAL_SHARE_TEXT = """I just sent my official support to DHS. The rule of law is non-negotiable. Join me and stand with the agents who protect us. #StandWithICE #RuleOfLaw #PlainviewProtocol"""

def get_twitter_share_url(text: str) -> str:
    """Generate Twitter share URL."""
    encoded_text = urllib.parse.quote(text)
    return f"https://twitter.com/intent/tweet?text={encoded_text}"

def get_facebook_share_url() -> str:
    """Generate Facebook share URL."""
    return "https://www.facebook.com/sharer/sharer.php?u=https://plainviewprotocol.com"

def render_ice_shield():
    """Render the ICE Shield support page."""
    
    if "badge_unlocked" not in st.session_state:
        st.session_state.badge_unlocked = False
    
    st.markdown("""
    <style>
    .shield-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        border-left: 5px solid #4a90d9;
        margin-bottom: 20px;
    }
    .shield-header h1 {
        color: white;
        margin: 0;
    }
    .thin-blue-line {
        height: 5px;
        background: linear-gradient(to right, #1a1a2e, #4a90d9, #1a1a2e);
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="shield-header">
        <h1>🛡️ ICE Shield — Stand with Law Enforcement</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("V6.26 — Shield of Gratitude Module")
    
    st.markdown('<div class="thin-blue-line"></div>', unsafe_allow_html=True)
    
    st.info("""
    *"The mob has bullhorns; we have numbers. Every email sent is a reminder to 
    Washington that for every protestor in the street, there are a thousand 
    citizens at work who support the rule of law."*
    
    — Russell David Nomer, Founder
    """)
    
    st.divider()
    
    counter = get_support_counter()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📧 Support Letters Sent", f"{counter:,}")
    col2.metric("🛡️ Sentinels Active", "3,143")
    col3.metric("🇺🇸 States Represented", "50")
    
    st.divider()
    
    st.subheader("📧 Send Official Support to DHS")
    st.caption("One-click email to DHS Public Engagement")
    
    st.warning("""
    **How it works:** Enter your information below, then click the button to 
    open your email client with the support letter pre-filled. Your email goes 
    directly to DHS as genuine constituent communication.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", placeholder="John Smith")
        city = st.text_input("Your City", placeholder="Plainview")
    
    with col2:
        state = st.selectbox("Your State", options=["Select State..."] + US_STATES)
    
    form_complete = name and city and state != "Select State..."
    
    if form_complete:
        mailto_url = generate_mailto_link(name, city, state)
        
        st.markdown(f"""
        <a href="{mailto_url}" target="_blank" onclick="incrementCounter()" style="
            display: inline-block;
            padding: 20px 40px;
            background: linear-gradient(135deg, #1a5276 0%, #2e86ab 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
            width: 100%;
            border: 2px solid #4a90d9;
        ">🛡️ SEND OFFICIAL SUPPORT TO DHS</a>
        """, unsafe_allow_html=True)
        
        if st.button("✅ I Sent My Email — Update Counter & Unlock Badge", use_container_width=True):
            increment_counter()
            st.session_state.badge_unlocked = True
            st.success(f"Thank you! Counter updated to {get_support_counter():,} support letters. Badge unlocked!")
            st.balloons()
    else:
        st.error("⚠️ Please complete all fields to activate the support button.")
    
    if st.session_state.badge_unlocked:
        st.divider()
        
        st.subheader("🛡️ Your 'Stand with ICE' Digital Badge")
        st.caption("V6.27 — Visual Shield Unlocked!")
        
        st.success("""
        *"A silent supporter is invisible. A Sentinel with a shield is a signal. 
        Wear this badge online to let the mob know they do not speak for America. 
        The silent majority is now visible."*
        
        — Russell David Nomer, Founder
        """)
        
        try:
            badge_bytes = get_badge_bytes()
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(badge_bytes, caption="Your Stand with ICE Badge", width=300)
            
            with col2:
                st.markdown("**Download & Share:**")
                
                st.download_button(
                    "🛡️ Download Your Badge (PNG)",
                    data=badge_bytes,
                    file_name="stand_with_ice_badge.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                st.divider()
                
                st.markdown("**One-Click Social Share:**")
                
                twitter_url = get_twitter_share_url(SOCIAL_SHARE_TEXT)
                st.link_button("🐦 Share on X (Twitter)", twitter_url, use_container_width=True)
                
                facebook_url = get_facebook_share_url()
                st.link_button("📘 Share on Facebook", facebook_url, use_container_width=True)
            
            st.info("""
            **How to Use Your Badge:**
            1. Download the PNG file
            2. Set it as your profile picture on X, Facebook, or Instagram
            3. Share the social post to amplify the message
            4. Every badge displayed is a signal to the silent majority
            """)
            
        except Exception as e:
            st.warning("Badge generation is loading. Please refresh in a moment.")
    
    st.divider()
    
    st.subheader("📜 Preview: The Support Letter")
    
    preview_name = name if name else "[Your Name]"
    preview_city = city if city else "[Your City]"
    preview_state = state if state != "Select State..." else "[Your State]"
    
    preview_text = SUPPORT_TEMPLATE.format(
        name=preview_name,
        city=preview_city,
        state=preview_state
    )
    
    st.text_area("Letter Preview:", preview_text, height=250)
    
    st.divider()
    
    st.subheader("🏛️ Why Your Voice Matters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **Morale Reinforcement**
        
        Agents on the ground face daily hostility from activists and media. 
        Your email proves that the "Silent Majority" is no longer silent. 
        Every message is read by real people at DHS.
        """)
    
    with col2:
        st.info("""
        **Narrative Counter-Weight**
        
        When DHS sees thousands of emails from real citizens in real towns 
        supporting lawful enforcement, it provides the political cover 
        necessary for agents to stand firm.
        """)
    
    with st.expander("ℹ️ Transparency: Email Verification"):
        st.markdown("""
        **Why We Require City and State:**
        
        - Ensures every email looks like genuine constituent communication
        - Prevents spam filters from blocking mass-generated emails
        - Creates geographic diversity that politicians notice
        - Distinguishes real citizen support from bot campaigns
        
        **Your Information:**
        - Is NOT stored in any database
        - Is only used to populate YOUR email
        - You send directly from your own email client
        - We never see your email address
        """)
    
    st.divider()
    
    st.markdown("""
    **🛡️ The Sentinel's Shield:**
    
    Law enforcement officers take an oath to protect and serve. When they 
    execute lawful orders, they deserve the support of law-abiding citizens. 
    This module ensures that support is visible, documented, and undeniable.
    
    *Hold the line. Back the badge.*
    """)
