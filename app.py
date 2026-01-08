import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import re

st.set_page_config(
    page_title="The Plainview Protocol: Truth, Kindness, & Security",
    page_icon="🇺🇸",
    layout="wide"
)

ALL_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

BORDER_STATES = ["Texas", "Arizona", "California", "New Mexico"]

st.markdown("""
<style>
    .main-header {
        color: #002868;
        text-align: center;
        border-bottom: 3px solid #BF0A30;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .metric-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #002868;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .footer {
        text-align: center;
        color: #002868;
        border-top: 2px solid #BF0A30;
        padding-top: 15px;
        margin-top: 30px;
        font-style: italic;
    }
    .info-box {
        background-color: #f0f4f8;
        border: 1px solid #002868;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    .rewrite-box {
        background-color: #e8f4e8;
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
    }
    .debt-clock {
        background: linear-gradient(135deg, #BF0A30 0%, #8B0000 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .support-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #002868;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🇺🇸 Navigation")

st.sidebar.markdown("---")
selected_state = st.sidebar.selectbox(
    "Select Your State:",
    ALL_STATES,
    index=ALL_STATES.index("New York")
)

user_role = st.sidebar.selectbox(
    "Your Role:",
    ["Taxpayer", "Business Owner", "Concerned Citizen"],
    index=0
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select a Page:",
    [
        "The National Lens",
        "The 2027 Fork in the Road",
        "The Bridge Builder",
        "Support the Protocol",
        "Leader Scorecard",
        "Support the Creator"
    ]
)

st.markdown("<h1 class='main-header'>The Plainview Protocol: Truth, Kindness, & Security</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666;'>Version 2.0 | Viewing as: <strong>{user_role}</strong> in <strong>{selected_state}</strong></p>", unsafe_allow_html=True)


def rewrite_professionally(text):
    """Rewrite angry text into professional, kind language."""
    if not text.strip():
        return ""
    
    replacements = {
        "destroying": "undermining",
        "destroy": "undermine",
        "idiots": "leaders",
        "idiot": "leader",
        "liars": "those violating public trust",
        "liar": "one violating public trust",
        "stupid": "misguided",
        "corrupt": "ethically compromised",
        "criminals": "those acting unlawfully",
        "criminal": "one acting unlawfully",
        "stealing": "misappropriating",
        "steal": "misappropriate",
        "thieves": "those misappropriating funds",
        "thief": "one misappropriating funds",
        "hate": "am deeply concerned about",
        "hated": "was deeply concerned about",
        "damn": "significant",
        "damned": "significant",
        "hell": "unacceptable situation",
        "crap": "concerning matter",
        "craziness": "dysfunction",
        "crazy": "dysfunctional",
        "insane": "unreasonable",
        "ridiculous": "concerning",
        "outrageous": "deeply troubling",
        "disgusting": "unacceptable",
        "terrible": "inadequate",
        "horrible": "deeply problematic",
        "worst": "most concerning",
        "evil": "harmful",
        "crooked": "acting with conflicts of interest",
        "scumbag": "individual of concern",
        "scumbags": "individuals of concern",
        "moron": "decision-maker",
        "morons": "decision-makers",
        "incompetent": "negligent",
        "failed": "has not fulfilled duties",
        "failure": "shortcoming",
        "betrayed": "failed to uphold commitments to",
        "betraying": "failing to uphold commitments to",
        "screwing": "negatively impacting",
        "screw": "negatively impact",
        "screwed": "negatively impacted",
    }
    
    result = text
    for angry_term, kind_term in replacements.items():
        pattern = re.compile(re.escape(angry_term), re.IGNORECASE)
        result = pattern.sub(kind_term, result)
    
    closing = "\n\nI respectfully urge enforcement of laws and accountability to protect America's domestic interests and future."
    
    if not result.strip().endswith(closing.strip()):
        result = result.strip() + closing
    
    return result


def get_state_multiplier(state):
    """Get waste/gap multiplier based on state (border states have higher impact)."""
    if state in BORDER_STATES:
        return 1.5
    return 1.0


if page == "The National Lens":
    st.header(f"📍 How Federal Costs Hit Home in {selected_state}")
    st.markdown("*Your Wallet Impact*")
    
    is_border_state = selected_state in BORDER_STATES
    if is_border_state:
        st.info(f"🚨 {selected_state} is a border state with higher direct policy gap impacts (1.5x multiplier applied)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        annual_taxes = st.number_input(
            "Estimated Annual Federal Taxes Paid ($)",
            min_value=0,
            max_value=1000000,
            value=15000,
            step=500
        )
    
    with col2:
        st.markdown(f"**State:** {selected_state}")
        st.markdown(f"**Role:** {user_role}")
        st.markdown(f"**Policy Gap Multiplier:** {get_state_multiplier(selected_state)}x")
    
    st.markdown("---")
    
    debt_interest_rate = 0.18
    base_waste_gap_rate = 0.05
    state_multiplier = get_state_multiplier(selected_state)
    adjusted_waste_gap_rate = base_waste_gap_rate * state_multiplier
    
    debt_interest_share = annual_taxes * debt_interest_rate
    waste_gap_share = annual_taxes * adjusted_waste_gap_rate
    
    st.subheader(f"Your Federal Tax Breakdown for {selected_state}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Your Share to Debt Interest",
            value=f"${debt_interest_share:,.2f}",
            delta="~18% of taxes",
            delta_color="inverse"
        )
    
    with col2:
        waste_pct = adjusted_waste_gap_rate * 100
        st.metric(
            label="Your Share to Waste & Policy Gaps",
            value=f"${waste_gap_share:,.2f}",
            delta=f"~{waste_pct:.1f}% of taxes",
            delta_color="inverse"
        )
    
    with col3:
        total_impact = debt_interest_share + waste_gap_share
        total_pct = (debt_interest_rate + adjusted_waste_gap_rate) * 100
        st.metric(
            label="Total Accountability Gap",
            value=f"${total_impact:,.2f}",
            delta=f"~{total_pct:.1f}% of taxes",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    st.markdown(f"""
    <div class='info-box'>
    <h4>📊 What This Means for {selected_state}</h4>
    <p>Based on <strong>$150.7 Billion</strong> net annual taxpayer cost of illegal immigration (FAIR 2023-2024 report) 
    and rising debt interest (~$1T annually projected 2026).</p>
    <ul>
        <li><strong>Debt Interest (~18%):</strong> Federal interest payments approaching $1 trillion annually by 2026</li>
        <li><strong>Waste/Policy Gaps ({waste_pct:.1f}%):</strong> {"Border state multiplier applied due to direct immigration impact" if is_border_state else "Base rate for policy gap costs"}</li>
    </ul>
    <p><strong>Accountability protects families and futures.</strong></p>
    </div>
    """, unsafe_allow_html=True)


elif page == "The 2027 Fork in the Road":
    st.header("🔀 Two Paths Ahead: Crisis or Reform")
    st.markdown("*Future Outlook*")
    
    st.markdown("""
    <div class='debt-clock'>
        💰 Current National Debt: ~$36.5 Trillion
    </div>
    """, unsafe_allow_html=True)
    
    debt_placeholder = st.empty()
    
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    status_quo = [100, 105, 112, 120, 130, 140, 152]
    accountability = [100, 102, 104, 105, 106, 107, 108]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=status_quo,
        mode='lines+markers',
        name='Status Quo',
        line=dict(color='#BF0A30', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=accountability,
        mode='lines+markers',
        name='Accountability Path',
        line=dict(color='#002868', width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title='Debt-to-GDP Ratio Projections (2024-2030)',
        xaxis_title='Year',
        yaxis_title='Debt-to-GDP (%)',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("⚖️ Immunity Double Standard")
    
    immunity_data = {
        "Scenario": [
            "Fraud / Enabling Fraud",
            "Public-Harming Negligence"
        ],
        "Average Citizen Consequence": [
            "Fines, Prison, Asset Seizure",
            "Full Liability"
        ],
        "Shielded Official Consequence": [
            "Often Protected by Immunity",
            "Frequently Dismissed"
        ]
    }
    
    df = pd.DataFrame(immunity_data)
    
    st.table(df)
    
    st.markdown("""
    <div class='info-box'>
    <h4>🏛️ Equal Rule of Law</h4>
    <p><strong>Equal rule of law restores trust, saves billions, secures borders.</strong></p>
    <p>When accountability applies equally to all citizens and officials alike, we strengthen the foundations of our republic and ensure taxpayer resources are protected.</p>
    </div>
    """, unsafe_allow_html=True)


elif page == "The Bridge Builder":
    st.header("🌉 Turn Concern into Impact")
    st.markdown("*Effective Voice*")
    
    st.markdown("""
    Express your concerns about policy issues below. This tool helps transform 
    strong emotions into professional, impactful communication that decision-makers 
    are more likely to hear and respond to.
    """)
    
    user_input = st.text_area(
        "Share your thoughts here (e.g., borders, fraud, immunity, costs):",
        height=150,
        placeholder="Type your concerns here... Don't worry about the tone - we'll help make it professional and impactful."
    )
    
    if st.button("✨ Rewrite Professionally & Kindly", type="primary"):
        if user_input.strip():
            rewritten = rewrite_professionally(user_input)
            
            st.markdown("---")
            st.subheader("📝 Your Professional Message")
            
            st.markdown(f"""
            <div class='rewrite-box'>
            {rewritten.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
            st.code(rewritten, language=None)
            
            st.info("📋 Copy the text above to use in emails, letters, or official communications.")
        else:
            st.warning("Please enter some text to rewrite.")
    
    st.markdown("---")
    
    with st.expander("💡 Tips for Effective Advocacy"):
        st.markdown("""
        - **Be Specific:** Reference specific policies, costs, or incidents
        - **Stay Factual:** Use data and statistics when possible
        - **Propose Solutions:** Suggest concrete actions
        - **Be Respectful:** Kind language is more persuasive
        - **Follow Up:** Persistence shows commitment
        """)


elif page == "Support the Protocol":
    st.header("💪 Sustain the Movement – Zero Grift, Full Transparency")
    st.markdown("*Help Keep This Free and Uncensorable*")
    
    st.markdown("""
    <div class='support-card'>
    <h3>🇺🇸 Your Support Makes a Difference</h3>
    <p>The Plainview Protocol is built on a foundation of transparency, accountability, and citizen empowerment. 
    Your support helps maintain and expand this platform nationwide.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💵 Donate")
        st.markdown("Support hosting and data access costs.")
        st.link_button(
            "Donate via PayPal",
            "https://www.paypal.com",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.markdown("### 🤝 Sponsor")
        st.markdown("Become an official sponsor of the Protocol.")
        st.link_button(
            "Become a Sponsor",
            "mailto:sponsor@plainviewprotocol.com",
            type="primary",
            use_container_width=True
        )
    
    with col3:
        st.markdown("### 🔧 Build Your Own")
        st.markdown("Fork and customize for your state.")
        st.link_button(
            "Fork on GitHub",
            "https://github.com",
            type="primary",
            use_container_width=True
        )
    
    st.markdown("---")
    
    st.markdown("""
    <div class='info-box'>
    <h4>📋 Our Commitment</h4>
    <ul>
        <li><strong>All funds go to:</strong> Hosting, data access, and platform expansion</li>
        <li><strong>No salaries:</strong> This is a volunteer-driven initiative</li>
        <li><strong>Full transparency:</strong> Financial reports available upon request</li>
        <li><strong>Uncensorable:</strong> Decentralized approach ensures the message persists</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


elif page == "Leader Scorecard":
    st.header("📊 Know Your Leaders: Voting Records on Key Issues")
    st.markdown("*Fact-Based Accountability*")
    
    st.markdown(f"Showing representatives relevant to **{selected_state}**")
    
    leader_data = {
        "Representative": [
            "Rep. John Smith (R)",
            "Rep. Jane Doe (D)",
            "Sen. Michael Johnson (R)",
            "Sen. Sarah Williams (D)",
            "Rep. Robert Brown (R)",
            "Rep. Emily Davis (D)"
        ],
        "State/District": [
            "TX-23",
            "CA-52",
            "Arizona",
            "New York",
            "Florida-7",
            "Pennsylvania-1"
        ],
        "Border Security Vote": [
            "Yes",
            "No",
            "Yes",
            "No",
            "Yes",
            "Abstain"
        ],
        "Immunity/Fraud Reform Vote": [
            "Yes",
            "Yes",
            "No",
            "Yes",
            "Yes",
            "No"
        ],
        "Accountability Score (0-100)": [
            85,
            45,
            70,
            55,
            90,
            40
        ]
    }
    
    df = pd.DataFrame(leader_data)
    
    min_score = st.slider("Filter by Minimum Accountability Score:", 0, 100, 0)
    filtered_df = df[df["Accountability Score (0-100)"] >= min_score]
    
    def highlight_scores(val):
        if isinstance(val, int):
            if val >= 70:
                return 'background-color: #d4edda; color: #155724'
            elif val >= 50:
                return 'background-color: #fff3cd; color: #856404'
            else:
                return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    styled_df = filtered_df.style.applymap(
        highlight_scores,
        subset=['Accountability Score (0-100)']
    )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        avg_score = filtered_df["Accountability Score (0-100)"].mean()
        st.metric("Average Accountability Score", f"{avg_score:.1f}")
    
    with col2:
        high_scorers = len(filtered_df[filtered_df["Accountability Score (0-100)"] >= 70])
        st.metric("Leaders Scoring 70+", high_scorers)
    
    st.markdown("""
    <div class='info-box'>
    <h4>📝 Disclaimer</h4>
    <p>Scores based solely on <strong>public voting records from Congress.gov</strong>. 
    Focused on fiscal responsibility, rule of law, and domestic security. 
    <strong>Non-partisan educational tool.</strong></p>
    <p><em>Data shown is illustrative. For actual voting records, visit 
    <a href="https://www.congress.gov" target="_blank">Congress.gov</a>.</em></p>
    </div>
    """, unsafe_allow_html=True)


elif page == "Support the Creator":
    st.header("☕ Sustain the Mission – Support Russell Directly")
    
    st.markdown("""
    <div class='support-card'>
    <p style='font-size: 1.1em;'>The Plainview Protocol is built and maintained by <strong>Russell Nomer</strong> in Plainview, NY. 
    It's free for all because of community support.</p>
    <p>If this tool helps you understand costs, see the immunity gap, or voice concerns kindly, 
    consider buying Russell a coffee.</p>
    <p><strong>100% of funds go to development, hosting, and expansion—no grift, full transparency.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ☕ Buy a Coffee")
        st.markdown("Direct support for development and hosting.")
        st.link_button(
            "Buy Russell a Coffee",
            "https://buymeacoffee.com/russellnomer",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.markdown("### 📱 Follow for Updates")
        st.markdown("Stay informed on new features and expansions.")
        st.link_button(
            "Follow on X",
            "https://x.com/russellnomer",
            type="secondary",
            use_container_width=True
        )
    
    with col3:
        st.markdown("### 💻 View the Source")
        st.markdown("See how it's built and fork your own version.")
        st.link_button(
            "View Live App Source",
            "https://replit.com/@russellnomer/The-Plainview-Protocol",
            type="secondary",
            use_container_width=True
        )
    
    st.markdown("---")
    
    st.markdown("""
    <div class='info-box' style='text-align: center;'>
    <h4>🙏 Thank you for helping keep truth and kindness growing. 🇺🇸</h4>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>🇺🇸 Built by Russell Nomer in Plainview, NY – Kindness, truth, secure America. 🇺🇸</p>
    <p><em>Fork this project to create your state's version.</em></p>
</div>
""", unsafe_allow_html=True)
