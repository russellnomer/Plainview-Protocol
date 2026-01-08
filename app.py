import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="The Plainview Protocol: Truth, Kindness, & Security",
    page_icon="🇺🇸",
    layout="wide"
)

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
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🇺🇸 Navigation")
page = st.sidebar.radio(
    "Select a Page:",
    ["The Local Lens", "The 2027 Fork in the Road", "The Bridge Builder"]
)

st.markdown("<h1 class='main-header'>The Plainview Protocol: Truth, Kindness, & Security</h1>", unsafe_allow_html=True)


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
        import re
        pattern = re.compile(re.escape(angry_term), re.IGNORECASE)
        result = pattern.sub(kind_term, result)
    
    closing = "\n\nI respectfully urge enforcement of laws and accountability to protect America's domestic interests and future."
    
    if not result.strip().endswith(closing.strip()):
        result = result.strip() + closing
    
    return result


if page == "The Local Lens":
    st.header("📍 How Federal Costs Hit Home in Plainview")
    st.markdown("*Your Wallet Impact*")
    
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
        county = st.text_input(
            "Your County",
            value="Nassau County, NY"
        )
    
    st.markdown("---")
    
    debt_interest_rate = 0.18
    waste_gap_rate = 0.05
    
    debt_interest_share = annual_taxes * debt_interest_rate
    waste_gap_share = annual_taxes * waste_gap_rate
    
    st.subheader(f"Your Federal Tax Breakdown for {county}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Your Share to Debt Interest",
            value=f"${debt_interest_share:,.2f}",
            delta="18% of taxes",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="Your Share to Waste/Gaps",
            value=f"${waste_gap_share:,.2f}",
            delta="5% of taxes",
            delta_color="inverse"
        )
    
    with col3:
        total_impact = debt_interest_share + waste_gap_share
        st.metric(
            label="Total Accountability Gap",
            value=f"${total_impact:,.2f}",
            delta="23% of taxes",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    st.markdown("""
    <div class='info-box'>
    <h4>📊 What This Means</h4>
    <ul>
        <li><strong>Debt Interest (18%):</strong> 2026 projection estimates federal interest payments approaching $1 trillion annually</li>
        <li><strong>Waste/Policy Gaps (5%):</strong> Includes unchecked burdens like the $150.7B net annual immigration cost per FAIR/House reports</li>
    </ul>
    <p><strong>This could fund local roads, schools, or security. Accountability protects taxpayer dollars and America's future.</strong></p>
    </div>
    """, unsafe_allow_html=True)


elif page == "The 2027 Fork in the Road":
    st.header("🔀 Two Paths Ahead: Crisis or Reform")
    st.markdown("*Future Outlook*")
    
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


st.markdown("---")
st.markdown("""
<div class='footer'>
    <p>🇺🇸 Built by Russell Nomer in Plainview, NY – Kindness, truth, secure America. 🇺🇸</p>
</div>
""", unsafe_allow_html=True)
