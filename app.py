import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import xml.etree.ElementTree as ET
import os
import time

st.set_page_config(
    page_title="The Plainview Protocol",
    page_icon="🇺🇸",
    layout="wide"
)

with open("sources.json", "r") as f:
    SOURCES = json.load(f)

try:
    with open("system_status.json", "r") as f:
        SYSTEM_STATUS = json.load(f)
        is_system_online = all(val == "OK" for val in SYSTEM_STATUS.values())
except FileNotFoundError:
    SYSTEM_STATUS = {"treasury": "Unknown", "senate": "Unknown", "wiki": "Unknown"}
    is_system_online = True

@st.cache_data(ttl=3600)
def get_live_debt():
    """Fetches live debt from US Treasury API. Fallback: Hardcoded Projection."""
    fallback_debt = 36500000000000.00
    try:
        url = SOURCES["treasury_debt"]
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            debt_str = data["data"][0]["tot_pub_debt_out_amt"]
            return float(debt_str)
    except Exception:
        pass
    return fallback_debt

@st.cache_data(ttl=3600)
def get_senate_votes():
    """Fetches Senate XML feed. Fallback: Generic Message."""
    fallback_votes = ["Vote data currently unavailable - Check back later", "System Maintenance"]
    votes = []
    try:
        url = SOURCES["senate_feed"]
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for vote in root.findall(".//vote")[:5]:
                question = vote.find("question")
                if question is not None:
                    votes.append(question.text)
    except Exception:
        pass
    
    if not votes:
        return fallback_votes
    return votes

@st.cache_data(ttl=86400)
def get_reps(state_name):
    """Scrapes Wikipedia for House Reps. Fallback: Placeholder."""
    fallback_df = pd.DataFrame({"Representative": ["Rep. Doe"], "District": ["1"], "Party": ["N/A"]})
    try:
        url = SOURCES["wiki_reps"]
        dfs = pd.read_html(url, match="District") 
        for df in dfs:
            if "District" in df.columns and "Member" in df.columns:
                clean_df = df[['District', 'Member', 'Party']].copy()
                clean_df = clean_df[clean_df['District'].str.contains(state_name, case=False, na=False)]
                
                if not clean_df.empty:
                    return clean_df
    except Exception as e:
        pass
    return fallback_df

@st.cache_data(ttl=3600)
def get_tariff_revenue():
    """Fetches tariff/customs revenue from Treasury API. Fallback: FY2025 Estimate."""
    fallback_tariff = 195000000000.00
    try:
        url = SOURCES.get("treasury_tariffs", "")
        if url:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data.get("data") and len(data["data"]) > 0:
                    for key in ["customs_duties_amount", "current_month_gross_amt", "current_fytd_gross_amt"]:
                        if key in data["data"][0]:
                            return float(data["data"][0][key]) * 1000000
    except Exception:
        pass
    return fallback_tariff

STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"
]

STATE_POPS = {
    "California": 39000000, "Texas": 30000000, "Florida": 22000000, "New York": 19000000,
}
US_POP = 333000000

st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0d3b66; }
    h1, h2, h3 { color: #0d3b66; }
    .stButton>button { background-color: #b22222; color: white; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🇺🇸 Plainview Protocol")
st.sidebar.caption("v3.2 | Self-Healing Architecture")

selected_state = st.sidebar.selectbox("Select Your State", STATES, index=31)
selected_focus = st.sidebar.selectbox("Select Focus", ["All", "Border Security", "Veterans First", "Education & Skills", "Crime & Safety", "Trade & Tariffs"])

st.sidebar.divider()
if is_system_online:
    st.sidebar.success("🟢 System Status: Online")
else:
    st.sidebar.warning("⚠️ System Status: Degraded")

st.sidebar.divider()
st.sidebar.markdown("### Fuel the Mission")
st.sidebar.link_button("☕ Support Russell", "https://buymeacoffee.com/russellnomer")

page = st.radio("Navigate", ["The National Lens", "The 2027 Fork", "Tariff Tracker", "The Activism Hub", "Leader Scorecard", "Support"], horizontal=True, label_visibility="collapsed")

if page == "The National Lens":
    st.header(f"📍 State of the Union: {selected_state}")
    
    live_debt = get_live_debt()
    
    if 'debt_base' not in st.session_state:
        st.session_state.debt_base = live_debt
        st.session_state.debt_start_time = time.time()
    
    tick_rate = 15000
    elapsed = time.time() - st.session_state.debt_start_time
    ticking_debt = st.session_state.debt_base + (tick_rate * elapsed)
    
    st.markdown("""
    <style>
    .debt-ticker {
        background: linear-gradient(135deg, #b22222 0%, #8b0000 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 2.2em;
        font-weight: bold;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(
        f"<div class='debt-ticker'>💰 Real-Time National Debt (Ticking): ${ticking_debt:,.0f}</div>",
        unsafe_allow_html=True
    )
    
    st.caption("⏱️ Ticks based on ~$15,000/second average rate (~$2T annual deficit). Actual daily figures from U.S. Treasury.")
    
    pop = STATE_POPS.get(selected_state, 6000000)
    state_share_debt = (live_debt / US_POP) * pop
    
    border_multiplier = 1.6 if selected_state in ["Texas", "Arizona", "New Mexico", "California"] else 1.0
    immigration_burden = (150700000000 / US_POP) * pop * border_multiplier
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🇺🇸 Base Debt (Treasury)", f"${live_debt:,.0f}")
    col2.metric(f"{selected_state}'s Share of Debt", f"${state_share_debt:,.0f}")
    col3.metric("State Immigration Burden", f"${immigration_burden:,.0f}", delta="Est. Annual Cost", delta_color="inverse")
    
    st.info(f"**Data Logic:** {selected_state} burden calculated using a {border_multiplier}x multiplier based on geographic exposure to border policy gaps.")
    
    if st.button("🔄 Refresh Ticker"):
        st.session_state.debt_base = live_debt
        st.session_state.debt_start_time = time.time()
        st.rerun()

elif page == "The 2027 Fork":
    st.header("🛤️ The Fork in the Road: 2024-2030")
    
    live_debt = get_live_debt() / 1e12
    
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    status_quo = [live_debt * (1.05**i) for i in range(len(years))]
    reform = [live_debt * (1.01**i) for i in range(len(years))]
    
    df_chart = pd.DataFrame({"Year": years, "Status Quo (Crisis)": status_quo, "Reform (Accountability)": reform})
    
    fig = px.line(df_chart, x="Year", y=["Status Quo (Crisis)", "Reform (Accountability)"], 
                  color_discrete_map={"Status Quo (Crisis)": "red", "Reform (Accountability)": "blue"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    savings = (status_quo[-1] - reform[-1]) * 1000
    st.success(f"💰 **Potential Savings by 2030:** ${savings:,.0f} Billion through fiscal accountability.")

elif page == "Tariff Tracker":
    st.header("🇺🇸 Bringing Money Home: The Tariff Offset")
    
    tariff_revenue = get_tariff_revenue()
    immigration_cost = 150700000000
    
    pop = STATE_POPS.get(selected_state, 6000000)
    state_dividend = (tariff_revenue / US_POP) * pop
    per_capita_dividend = tariff_revenue / US_POP
    
    col1, col2 = st.columns(2)
    col1.metric("💵 Total Tariff Revenue (FY To Date)", f"${tariff_revenue:,.0f}")
    col2.metric(f"🎁 {selected_state}'s Plainview Dividend", f"${state_dividend:,.0f}")
    
    st.caption("*This is foreign money entering the US Treasury through trade policy.*")
    
    st.divider()
    st.subheader("⚖️ The Debate: Pain vs. Gain")
    
    pain_col, gain_col = st.columns(2)
    
    with pain_col:
        st.markdown("### 😰 The Pain: Importers' Cost")
        st.warning("Businesses relying on foreign manufacturing face higher costs ($500k+/yr for some). Consumer prices may rise on imported goods.")
    
    with gain_col:
        st.markdown("### 💪 The Gain: American Strength")
        st.success("Incentivizes domestic production, creates jobs, and funds Veteran/Border priorities. Foreign nations pay into our Treasury.")
    
    st.divider()
    st.subheader("📊 The Offset Strategy")
    
    offset_data = pd.DataFrame({
        "Category": ["Immigration Cost", "Tariff Revenue"],
        "Amount (Billions)": [immigration_cost / 1e9, tariff_revenue / 1e9]
    })
    
    fig = px.bar(offset_data, x="Category", y="Amount (Billions)", 
                 color="Category",
                 color_discrete_map={"Immigration Cost": "#b22222", "Tariff Revenue": "#0d3b66"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    net_position = tariff_revenue - immigration_cost
    if net_position >= 0:
        st.success(f"✅ **In the Black:** Tariff revenue exceeds immigration cost by ${net_position/1e9:.1f}B")
    else:
        st.error(f"❌ **In the Red:** Immigration cost exceeds tariff revenue by ${abs(net_position)/1e9:.1f}B")
        st.info("Increasing tariff enforcement or reducing policy gaps could close this deficit.")
    
    st.divider()
    st.subheader("🌉 Bridge Builder: Trade Edition")
    st.markdown("**Concerned about rising prices?** Ask your reps to use tariff revenue to cut income tax, not just spend it.")
    
    trade_template = f"In {selected_state}, we support smart trade policy. Use tariff revenue to cut our taxes, not grow government. #PlainviewProtocol #FairTrade"
    st.code(trade_template, language=None)
    st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={trade_template.replace(' ', '%20').replace('#', '%23')}")

elif page == "The Activism Hub":
    st.header("🌉 The Bridge Builder: Facts Over Rage")
    
    tab1, tab2, tab3 = st.tabs(["Veterans First", "Border Security", "Education"])
    
    with tab1:
        st.write("Compare the cost of housing a homeless veteran vs. federal waste.")
        st.info("In 2024, approx 35,000 veterans experienced homelessness. The cost to house them is a fraction of the $150B immigration burden.")
        tweet_text = f"In {selected_state}, we believe Veterans come first. Why is the budget prioritizing waste over heroes? Fix it now. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    with tab2:
        st.write("Secure borders ensure safe communities and fiscal sanity.")
        tweet_text = f"Security is not optional. {selected_state} taxpayers are footing the bill for unsecured borders. Enforce the law. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    st.divider()
    
    st.subheader("Draft Your Message")
    user_input = st.text_area("Vent your frustration here (we will make it professional):")
    if st.button("Rewrite Kindly"):
        if user_input:
            cleaned = user_input.replace("hate", "am concerned about").replace("idiots", "officials").replace("destroying", "negatively impacting")
            final_msg = f"{cleaned}. I respectfully urge you to prioritize domestic security and the rule of law."
            st.success("✅ Ready to Send:")
            st.code(final_msg, language=None)

elif page == "Leader Scorecard":
    st.header("🏛️ Real-Time Democracy Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📜 Latest Senate Actions")
        votes = get_senate_votes()
        for v in votes:
            st.text(f"• {v}")
            
    with col2:
        st.subheader(f"👥 Your {selected_state} Reps")
        reps_df = get_reps(selected_state)
        st.dataframe(reps_df, hide_index=True)
        
    st.caption("Data fetched live from Senate.gov and Wikipedia public records.")

elif page == "Support":
    st.header("☕ Sustain the Mission")
    st.write("This tool is free, ad-free, and uncensorable thanks to supporters like you.")
    
    c1, c2, c3 = st.columns(3)
    c1.link_button("Donate via PayPal", "https://paypal.com")
    c2.link_button("Buy Russell a Coffee", "https://buymeacoffee.com/russellnomer")
    c3.link_button("Fork on GitHub", "https://github.com")

st.markdown("---")
st.markdown("<center>Built by Russell Nomer in Plainview, NY | <i>Truth, Kindness, Security</i></center>", unsafe_allow_html=True)
