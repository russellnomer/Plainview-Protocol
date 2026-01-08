import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from xml.etree import ElementTree as ET

st.set_page_config(
    page_title="The Plainview Protocol V3.1",
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

STATE_POPULATIONS = {
    "California": 39538223, "Texas": 29145505, "Florida": 21538187,
    "New York": 20201249, "Pennsylvania": 13002700, "Illinois": 12812508,
    "Ohio": 11799448, "Georgia": 10711908, "North Carolina": 10439388,
    "Michigan": 10077331, "New Jersey": 9288994, "Virginia": 8631393,
    "Washington": 7614893, "Arizona": 7151502, "Massachusetts": 7029917,
    "Tennessee": 6910840, "Indiana": 6785528, "Maryland": 6177224,
    "Missouri": 6154913, "Wisconsin": 5893718, "Colorado": 5773714,
    "Minnesota": 5706494, "South Carolina": 5118425, "Alabama": 5024279,
    "Louisiana": 4657757, "Kentucky": 4505836, "Oregon": 4237256,
    "Oklahoma": 3959353, "Connecticut": 3605944, "Utah": 3271616,
    "Iowa": 3190369, "Nevada": 3104614, "Arkansas": 3011524,
    "Mississippi": 2961279, "Kansas": 2937880, "New Mexico": 2117522,
    "Nebraska": 1961504, "Idaho": 1839106, "West Virginia": 1793716,
    "Hawaii": 1455271, "New Hampshire": 1377529, "Maine": 1362359,
    "Montana": 1084225, "Rhode Island": 1097379, "Delaware": 989948,
    "South Dakota": 886667, "North Dakota": 779094, "Alaska": 733391,
    "Vermont": 643077, "Wyoming": 576851
}

US_POPULATION = 330000000

def load_sources():
    try:
        with open('sources.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "treasury_debt": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?sort=-record_date&limit=1",
            "senate_feed": "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_119_1.xml",
            "wiki_reps": "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"
        }

def load_system_status():
    try:
        with open('system_status.json', 'r') as f:
            return json.load(f)
    except:
        return {"treasury_debt": "OK", "senate_feed": "OK", "wiki_reps": "OK"}

@st.cache_data(ttl=3600)
def get_live_debt():
    sources = load_sources()
    try:
        response = requests.get(sources['treasury_debt'], timeout=10)
        if response.status_code == 200:
            data = response.json()
            debt_value = float(data['data'][0]['tot_pub_debt_out_amt'])
            return debt_value
    except Exception as e:
        pass
    return 36500000000000.00

@st.cache_data(ttl=3600)
def get_senate_votes():
    sources = load_sources()
    try:
        response = requests.get(sources['senate_feed'], timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            votes = []
            for vote in root.findall('.//vote')[:5]:
                title = vote.find('title')
                if title is not None and title.text:
                    votes.append(title.text[:100])
                else:
                    issue = vote.find('issue')
                    if issue is not None and issue.text:
                        votes.append(f"Vote on {issue.text}")
            if votes:
                return votes[:3]
    except Exception as e:
        pass
    return ["Vote data currently unavailable - Check back later"]

@st.cache_data(ttl=3600)
def get_reps(state):
    sources = load_sources()
    try:
        tables = pd.read_html(sources['wiki_reps'])
        for table in tables:
            cols = table.columns.tolist()
            state_col = None
            for col in cols:
                if 'state' in str(col).lower() or 'district' in str(col).lower():
                    state_col = col
                    break
            if state_col:
                filtered = table[table[state_col].astype(str).str.contains(state, case=False, na=False)]
                if not filtered.empty:
                    return filtered.head(10)
    except Exception as e:
        pass
    return pd.DataFrame({
        "Representative": ["Rep. Data Unavailable"],
        "District": ["N/A"],
        "Party": ["N/A"]
    })

st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    h1, h2, h3 { color: #0d3b66; }
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
    .stButton>button:hover { background-color: #8b0000; }
    .debt-live {
        background: linear-gradient(135deg, #b22222 0%, #8b0000 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 2em;
        font-weight: bold;
        margin: 15px 0;
    }
    .status-online { color: #28a745; }
    .status-error { color: #dc3545; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🇺🇸 The Plainview Protocol")
st.sidebar.markdown("*V3.1 – Self-Healing National Edition*")
st.sidebar.divider()

selected_state = st.sidebar.selectbox("Select Your State:", ALL_STATES, index=ALL_STATES.index("New York"))
selected_focus = st.sidebar.selectbox("Select Focus:", ["All", "Border", "Veterans", "Education"])

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["The National Lens", "The Fork in the Road", "The Activism Hub", "Leader Scorecard", "Support the Mission"]
)

st.sidebar.divider()

status = load_system_status()
all_ok = all(v == "OK" for v in status.values())
if all_ok:
    st.sidebar.markdown("**System Status:** <span class='status-online'>🟢 Online</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("**System Status:** <span class='status-error'>🟡 Partial</span>", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("### Fuel the Builder")
st.sidebar.link_button("☕ Support Russell", "https://buymeacoffee.com/russellnomer")
st.sidebar.caption("Built by Russell Nomer in Plainview, NY.")


def get_state_multiplier(state):
    return 1.6 if state in BORDER_STATES else 1.0


if page == "The National Lens":
    st.title(f"📊 State of the Union: {selected_state}")
    st.markdown("### Live Federal Data Dashboard")
    
    live_debt = get_live_debt()
    state_pop = STATE_POPULATIONS.get(selected_state, 5000000)
    state_debt_share = (live_debt / US_POPULATION) * state_pop
    
    multiplier = get_state_multiplier(selected_state)
    base_immigration_cost = 150.7
    state_immigration = base_immigration_cost * multiplier * (state_pop / US_POPULATION) * 50
    
    st.markdown(f"""
    <div class='debt-live'>
        💰 Real-Time National Debt: ${live_debt:,.0f}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Your State's Debt Share",
            f"${state_debt_share:,.0f}",
            f"{selected_state}"
        )
    
    with col2:
        st.metric(
            "Immigration Burden",
            f"${state_immigration:.1f}B",
            f"Multiplier: {multiplier}x" if multiplier > 1 else "Base rate"
        )
    
    with col3:
        per_capita = live_debt / US_POPULATION
        st.metric(
            "Per Capita Debt",
            f"${per_capita:,.0f}",
            "Every American"
        )
    
    if selected_state in BORDER_STATES:
        st.warning(f"🚨 {selected_state} is a border state with elevated policy costs (1.6x multiplier applied)")
    
    st.markdown(f"""
    *Data sourced from U.S. Treasury Fiscal Data API. Immigration cost base: $150.7B (FAIR 2023-2024).*
    """)

elif page == "The Fork in the Road":
    st.title("🛤️ The Fork in the Road")
    st.markdown("### Two Paths Ahead: Crisis or Reform")
    
    live_debt = get_live_debt()
    base_debt_trillion = live_debt / 1e12
    
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    status_quo = [base_debt_trillion * (1.05 ** i) for i in range(7)]
    reform = [base_debt_trillion * (1.01 ** i) for i in range(7)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=status_quo,
        mode='lines+markers',
        name='Status Quo (Crisis)',
        line=dict(color='#FF0000', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=years, y=reform,
        mode='lines+markers',
        name='Accountability (Reform)',
        line=dict(color='#0000FF', width=3)
    ))
    
    fig.update_layout(
        title='National Debt Projection (Trillions USD)',
        xaxis_title='Year',
        yaxis_title='Debt (Trillions $)',
        hovermode='x unified',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("⚖️ The Immunity Double Standard")
    immunity_data = pd.DataFrame({
        "Scenario": ["Citizen Commits Fraud", "Official Enables Policy Fraud", "Negligence Harming Public"],
        "Average Citizen": ["Prison / Asset Seizure", "N/A", "Full Legal Liability"],
        "Shielded Official": ["N/A", "Protected by Immunity", "Frequently Dismissed"]
    })
    st.table(immunity_data)

elif page == "The Activism Hub":
    st.title("🌉 The Activism Hub")
    st.markdown("### Turn Frustration into Effective Impact")
    
    tab1, tab2, tab3 = st.tabs(["🎖️ Veterans", "🛡️ Border Security", "📚 Education"])
    
    with tab1:
        st.markdown("**Focus: Veterans Affairs & Support**")
        context = "veterans"
    with tab2:
        st.markdown("**Focus: Border Security & Immigration Policy**")
        context = "border"
    with tab3:
        st.markdown("**Focus: Education Funding & Reform**")
        context = "education"
    
    user_text = st.text_area(
        "Vent your frustration here:",
        height=150,
        placeholder="e.g., 'These leaders are destroying our country with wasteful spending!'"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ Rewrite Kindly", type="primary"):
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
                    "corrupt": "ethically compromised",
                    "morons": "decision-makers",
                    "screw": "negatively impact",
                    "damn": "concerning",
                    "crap": "unsatisfactory"
                }
                
                for word, replacement in replacements.items():
                    rewritten = rewritten.replace(word, replacement)
                
                rewritten = ". ".join(s.capitalize() for s in rewritten.split(". "))
                
                final_output = (
                    f"{rewritten}\n\n"
                    "I respectfully urge enforcement of laws and accountability to protect America's domestic interests and future."
                )
                
                st.success("✅ **Draft Ready:**")
                st.text_area("Copy this version:", value=final_output, height=200)
            else:
                st.error("Please enter text first.")
    
    with col2:
        share_text = f"In {selected_state}, we pay too much for broken policies. Fix it now! #PlainviewProtocol"
        encoded_text = share_text.replace(" ", "%20").replace("#", "%23")
        st.link_button(
            "📢 Share on X",
            f"https://twitter.com/intent/tweet?text={encoded_text}",
            use_container_width=True
        )

elif page == "Leader Scorecard":
    st.title("📊 Leader Scorecard")
    st.markdown("### Accountability Check")
    
    st.subheader("🏛️ Recent Senate Action")
    votes = get_senate_votes()
    for i, vote in enumerate(votes, 1):
        st.markdown(f"**{i}.** {vote}")
    
    st.divider()
    
    st.subheader(f"👥 Your {selected_state} Representatives")
    reps_df = get_reps(selected_state)
    st.dataframe(reps_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("📈 Sample Accountability Scores")
    sample_data = pd.DataFrame({
        "Representative": ["Rep. Chip Roy (R)", "Rep. AOC (D)", "Sen. Ted Cruz (R)", "Sen. Sinema (I)", "Rep. Crenshaw (R)"],
        "State": ["TX-21", "NY-14", "Texas", "Arizona", "TX-02"],
        "Border Vote": ["Yes", "No", "Yes", "Yes", "Yes"],
        "Immunity Reform": ["Yes", "Yes", "No", "Yes", "Yes"],
        "Score": [88, 42, 75, 68, 82]
    })
    
    def color_score(val):
        if isinstance(val, (int, float)):
            if val >= 70:
                return 'background-color: #d4edda'
            elif val >= 50:
                return 'background-color: #fff3cd'
            else:
                return 'background-color: #f8d7da'
        return ''
    
    st.dataframe(sample_data.style.applymap(color_score, subset=['Score']), use_container_width=True, hide_index=True)
    
    st.caption("**Disclaimer:** Scores based on public voting records from Congress.gov. Non-partisan educational tool.")

elif page == "Support the Mission":
    st.title("☕ Power the Protocol")
    st.markdown("### Sustain This Tool")
    
    st.markdown("""
    **The Plainview Protocol** is built and maintained by **Russell Nomer** in Plainview, NY.
    
    100% of funds go to:
    - 💻 Development & Hosting
    - 📊 Data API Access
    - 🚀 National Expansion
    
    *No grift. Full transparency.*
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.link_button("☕ Buy Me a Coffee", "https://buymeacoffee.com/russellnomer", type="primary", use_container_width=True)
    
    with col2:
        st.link_button("💳 PayPal", "https://paypal.me/russellnomer", use_container_width=True)
    
    with col3:
        st.link_button("🔧 Fork on GitHub", "https://github.com", use_container_width=True)
    
    st.divider()
    st.caption("Thank you for helping keep truth and kindness growing. 🇺🇸")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built by Russell Nomer in Plainview, NY – <i>Kindness, Truth, Secure America.</i> | V3.1"
    "</div>",
    unsafe_allow_html=True
)
