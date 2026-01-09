"""
Social Ammo Module - V6.29
The Plainview Protocol

Reply scripts and social counter-measures for the information war.

"The lie spreads because it is easy. The truth wins when we make it repeatable."
"""

import streamlit as st

FACT_CHECK_LINK = "https://plainviewprotocol.com"

REPLY_SCRIPTS = {
    "physics": {
        "name": "⚡ The Physics Check",
        "best_for": "Posts claiming she was 'unarmed'",
        "script": """Stop the spin. She wasn't 'unarmed'—she was driving a 4,300-lb weapon. Physics shows that a vehicle at acceleration force hits harder than a bullet. The agent didn't shoot a driver; he stopped a deadly projectile. The data is clear: {link} #StandWithICE #PlainviewProtocol"""
    },
    "law": {
        "name": "⚖️ The Law & Order",
        "best_for": "Posts claiming 'police brutality'",
        "script": """Federal law is not a suggestion. 8 CFR 287.8 explicitly authorizes deadly force when a vehicle is used to threaten life. She made the choice to turn her car into a weapon; the agent made the choice to go home to his family. We stand with the rule of law. Read the statute: {link} #RuleOfLaw"""
    },
    "visual": {
        "name": "🎯 The Visual Nuke",
        "best_for": "Image-heavy Instagram/TikTok posts",
        "script": """⚠️ FACT CHECK: The 'Just Driving Away' narrative is false. Forensic analysis proves the vehicle was an active deadly threat. Don't fall for the emotional manipulation—look at the ballistics and the law. Receipts attached. 👇 {link}"""
    }
}

HASHTAGS = "#FactCheck #RuleOfLaw #SupportICE #PlainviewProtocol"

def get_script_with_link(script_key: str, custom_link: str = None) -> str:
    """Get a script with the link appended."""
    link = custom_link or FACT_CHECK_LINK
    script = REPLY_SCRIPTS[script_key]["script"]
    return script.format(link=link)

def render_ammo_box():
    """Render the Social Ammo Box UI."""
    st.subheader("⚔️ Social Counter-Measures")
    st.caption("V6.29 — The Ammo Box")
    
    st.success("""
    *"The lie spreads because it is easy. The truth wins when we make it repeatable. 
    Copy the script. Post the card. Hold the line in the comments section."*
    
    — Russell David Nomer, Founder
    """)
    
    st.divider()
    
    st.markdown("**🎯 Reply Guy Scripts — Copy & Fire:**")
    
    st.info("""
    **How to deploy:** Copy a script below, paste it as a reply to viral misinformation, 
    and the link will render the Fact Check Card as a preview image on X/Twitter.
    """)
    
    for key, data in REPLY_SCRIPTS.items():
        with st.container():
            st.markdown(f"### {data['name']}")
            st.caption(f"Best for: {data['best_for']}")
            
            full_script = get_script_with_link(key)
            
            st.text_area(
                f"Script ({key})",
                full_script,
                height=120,
                key=f"script_{key}",
                label_visibility="collapsed"
            )
            
            st.markdown(f"""
            <div style="margin-bottom: 20px;">
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("**🎯 Quick Deploy — Target List:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Navigate to deploy scripts:**
        - Go to **Mamdani Watchdog** for NYC targets
        - Check **BDS Clawback Tracker** for funding ties
        """)
    
    with col2:
        st.markdown("""
        **Top viral accounts to monitor:**
        - Progressive lawmakers
        - Activist media outlets
        - Local protest organizers
        """)
    
    st.divider()
    
    st.markdown("**📋 Full Hashtag Pack:**")
    st.code(HASHTAGS, language=None)
    
    with st.expander("ℹ️ Deployment Strategy"):
        st.markdown("""
        **Goal: Generate a "Ratio"**
        
        A "Ratio" occurs when the counter-response gets more engagement 
        than the original false claim.
        
        **Tactics:**
        1. **Speed:** Be first to reply with data
        2. **Consistency:** Use the same scripts for message discipline
        3. **Visual:** The Fact Check Card renders as a preview image
        4. **Numbers:** When thousands use the same script, algorithms amplify
        
        **The Wall of Truth:** By arming Sentinels with standardized, 
        high-quality data, you create unified messaging that cannot be ignored.
        """)
