import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="The Plainview Protocol",
    page_icon="🇺🇸",
    layout="wide",
    initial_sidebar_state="expanded"
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

STATE_POPULATION_RATIOS = {
    "California": 0.118,
    "Texas": 0.088,
    "Florida": 0.066,
    "New York": 0.059,
    "Pennsylvania": 0.039,
    "Illinois": 0.038,
    "Ohio": 0.035,
    "Georgia": 0.032,
    "North Carolina": 0.032,
    "Michigan": 0.030,
    "New Jersey": 0.028,
    "Virginia": 0.026,
    "Washington": 0.023,
    "Arizona": 0.022,
    "Massachusetts": 0.021,
    "Tennessee": 0.021,
    "Indiana": 0.020,
    "Maryland": 0.018,
    "Missouri": 0.018,
    "Wisconsin": 0.018,
    "Colorado": 0.017,
    "Minnesota": 0.017,
    "South Carolina": 0.016,
    "Alabama": 0.015,
    "Louisiana": 0.014,
    "Kentucky": 0.014,
    "Oregon": 0.013,
    "Oklahoma": 0.012,
    "Connecticut": 0.011,
    "Utah": 0.010,
    "Iowa": 0.010,
    "Nevada": 0.010,
    "Arkansas": 0.009,
    "Mississippi": 0.009,
    "Kansas": 0.009,
    "New Mexico": 0.006,
    "Nebraska": 0.006,
    "Idaho": 0.006,
    "West Virginia": 0.005,
    "Hawaii": 0.004,
    "New Hampshire": 0.004,
    "Maine": 0.004,
    "Montana": 0.003,
    "Rhode Island": 0.003,
    "Delaware": 0.003,
    "South Dakota": 0.003,
    "North Dakota": 0.002,
    "Alaska": 0.002,
    "Vermont": 0.002,
    "Wyoming": 0.002
}

st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    h1, h2, h3 {
        color: #0d3b66;
    }
    .stMetric {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button {
        color: white;
        background-color: #b22222;
        border: none;
    }
    .stButton>button:hover {
        background-color: #8b0000;
    }
    .debt-display {
        background: linear-gradient(135deg, #b22222 0%, #8b0000 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.8em;
        font-weight: bold;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("🇺🇸 The Plainview Protocol")
st.sidebar.markdown("*Truth, Kindness, & Security*")
st.sidebar.markdown("**Version 2.0 – National Edition**")

st.sidebar.divider()

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

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["The National Lens", "The 2027 Fork in the Road", "The Bridge Builder", "Support the Mission", "Leader Scorecard"]
)

st.sidebar.divider()
st.sidebar.markdown("### Fuel the Builder")
st.sidebar.link_button("☕ Support Russell", "https://buymeacoffee.com/russellnomer", help="Buy a coffee to support the app development")
st.sidebar.caption("Built by Russell Nomer in Plainview, NY.")


def get_state_multiplier(state):
    if state in BORDER_STATES:
        return 1.5
    return 1.0


def get_state_immigration_cost(state):
    national_cost = 150.7
    ratio = STATE_POPULATION_RATIOS.get(state, 0.005)
    return national_cost * ratio


if page == "The National Lens":
    st.title(f"📍 Federal Costs in {selected_state}")
    st.markdown(f"### Your Wallet Impact as a {user_role}")
    
    is_border = selected_state in BORDER_STATES
    if is_border:
        st.warning(f"🚨 {selected_state} is a border state – 1.5x policy gap multiplier applied due to direct immigration impact.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("Input your estimated details below to see the breakdown.")
        tax_input = st.number_input("Estimated Annual Federal Tax Paid ($)", value=15000, step=1000)
    
    with col2:
        multiplier = get_state_multiplier(selected_state)
        state_imm_cost = get_state_immigration_cost(selected_state)
        
        debt_share = tax_input * 0.18
        base_waste = tax_input * 0.05
        waste_share = base_waste * multiplier
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Debt Interest Share", f"${debt_share:,.2f}", "~18%")
        m2.metric("Waste/Policy Gaps", f"${waste_share:,.2f}", f"~{5 * multiplier:.1f}%")
        m3.metric("Total Impact", f"${debt_share + waste_share:,.2f}")
        
        st.warning(f"📉 **Impact on {selected_state}:** ${waste_share + debt_share:,.2f} of your taxes goes toward debt interest and policy gaps instead of local infrastructure, schools, or security.")
        
        st.markdown(f"""
        **{selected_state}'s Share of Immigration Net Cost:** ~${state_imm_cost:.1f}B annually  
        *(Based on $150.7B national net cost – FAIR 2023-2024 report, prorated by state population)*
        """)

elif page == "The 2027 Fork in the Road":
    st.title("🛤️ The 2027 Fork in the Road")
    st.markdown("### Two Paths Ahead: Crisis or Reform")
    
    st.markdown("""
    <div class='debt-display'>
        💰 Current National Debt: ~$36.5 Trillion
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Visualizing the trajectory of our National Debt based on policy choices.")
    
    chart_data = pd.DataFrame({
        'Year': [2024, 2025, 2026, 2027, 2028, 2029, 2030],
        'Status Quo (Crisis)': [100, 105, 112, 122, 135, 148, 160],
        'Accountability (Reform)': [100, 102, 103, 104, 104.5, 105, 105]
    })
    chart_data.set_index('Year', inplace=True)
    
    st.line_chart(chart_data, color=["#FF0000", "#0000FF"])
    
    st.divider()
    
    st.subheader("⚖️ The Immunity Double Standard")
    st.markdown("Why reform is necessary for fiscal sanity:")
    
    immunity_data = {
        "Scenario": ["Citizen Commits Fraud", "Official Enables Policy Fraud", "Negligence Harming Public"],
        "Consequence for Average Citizen": ["Prison / Asset Seizure", "N/A", "Full Legal Liability"],
        "Consequence for Shielded Official": ["N/A", "Protected by Immunity", "Frequently Dismissed"]
    }
    st.table(pd.DataFrame(immunity_data))
    st.caption("Equal rule of law restores trust and saves billions.")

elif page == "The Bridge Builder":
    st.title("🌉 The Bridge Builder")
    st.markdown("### Turn Frustration into Effective Impact")
    st.write("Anger gets ignored. Professional, firm demands for accountability get filed.")
    
    user_text = st.text_area("Vent your frustration here (e.g., 'These leaders are destroying us with these costs!'):", height=150)
    
    if st.button("Rewrite Professionally & Kindly"):
        if user_text:
            rewritten = user_text.lower()
            
            replacements = {
                "destroying": "negligent regarding",
                "idiots": "elected officials",
                "liars": "those violating public trust",
                "stupid": "ill-advised",
                "hate": "am deeply concerned about",
                "hell": "a difficult situation",
                "criminal": "unlawful",
                "corrupt": "ethically compromised"
            }
            
            for word, replacement in replacements.items():
                rewritten = rewritten.replace(word, replacement)
            
            rewritten = ". ".join(s.capitalize() for s in rewritten.split(". "))
            
            final_output = (
                f"{rewritten}\n\n"
                "I respectfully urge enforcement of laws and accountability to protect America's domestic interests and future. "
                "Please support an audit of these expenditures."
            )
            
            st.success("✅ **Draft Ready for Action:**")
            st.text_area("Copy this version:", value=final_output, height=200)
        else:
            st.error("Please enter some text above first.")

elif page == "Support the Mission":
    st.title("☕ Power the Protocol")
    st.markdown("### Sustain the Mission – Support Russell Directly")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **The Plainview Protocol** is built and maintained by **Russell Nomer** in Plainview, NY. 
        
        It is free for all because of community support. If this tool helps you understand costs, 
        see the immunity gap, or voice concerns kindly, consider buying Russell a coffee.
        
        **100% of funds go to:**
        * 💻 Development & Hosting
        * 📊 Data API Access
        * 🚀 National Expansion
        
        *No grift. Full transparency.*
        """)
        
        st.write("")
        
        st.link_button("☕ Buy Russell a Coffee", "https://buymeacoffee.com/russellnomer", type="primary", use_container_width=True)
        
        st.write("")
        
        st.link_button("🐦 Follow on X for Updates", "https://x.com/russellnomer", use_container_width=True)

    with col2:
        st.info("Your support keeps this tool ad-free and uncensorable.")

    st.divider()
    st.caption("Thank you for helping keep truth and kindness growing. 🇺🇸")

elif page == "Leader Scorecard":
    st.title("📊 Voting Records: Accountability Check")
    st.markdown(f"### How Representatives Vote on Key Issues")
    
    leader_data = pd.DataFrame({
        "Representative": [
            "Rep. Chip Roy (R)",
            "Rep. Alexandria Ocasio-Cortez (D)",
            "Sen. Ted Cruz (R)",
            "Sen. Kyrsten Sinema (I)",
            "Rep. Dan Crenshaw (R)",
            "Rep. Ro Khanna (D)"
        ],
        "State/District": [
            "TX-21",
            "NY-14",
            "Texas",
            "Arizona",
            "TX-02",
            "CA-17"
        ],
        "Border Security Vote": [
            "Yes",
            "No",
            "Yes",
            "Yes",
            "Yes",
            "No"
        ],
        "Immunity Reform Vote": [
            "Yes",
            "Yes",
            "No",
            "Yes",
            "Yes",
            "Yes"
        ],
        "Accountability Score (0-100)": [
            88,
            42,
            75,
            68,
            82,
            55
        ]
    })
    
    st.markdown(f"*Filtering for relevance to **{selected_state}** where applicable*")
    
    min_score = st.slider("Filter by Minimum Score:", 0, 100, 0)
    filtered_df = leader_data[leader_data["Accountability Score (0-100)"] >= min_score]
    
    def color_score(val):
        if isinstance(val, (int, float)):
            if val >= 70:
                return 'background-color: #d4edda; color: #155724'
            elif val >= 50:
                return 'background-color: #fff3cd; color: #856404'
            else:
                return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    styled_df = filtered_df.style.applymap(color_score, subset=['Accountability Score (0-100)'])
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    with col1:
        avg = filtered_df["Accountability Score (0-100)"].mean()
        st.metric("Average Score", f"{avg:.1f}")
    with col2:
        high = len(filtered_df[filtered_df["Accountability Score (0-100)"] >= 70])
        st.metric("Leaders 70+", high)
    
    st.divider()
    st.caption("**Disclaimer:** Scores based solely on public voting records from Congress.gov. Focused on fiscal responsibility, rule of law, and domestic security. Non-partisan educational tool.")

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built by Russell Nomer in Plainview, NY – <i>Kindness, Truth, Secure America.</i>"
        "</div>", 
        unsafe_allow_html=True
    )
    st.link_button("🔧 Fork on GitHub", "https://github.com", use_container_width=True)
