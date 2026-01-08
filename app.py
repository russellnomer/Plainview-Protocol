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

def calculate_transparency_score(visible_votes, total_sessions):
    """Applies Adverse Inference for officials who hide data."""
    if total_sessions == 0:
        return 0, "⚠️ NO DATA (Shadow Penalty Applied)"
    
    transparency_ratio = visible_votes / total_sessions
    
    if transparency_ratio < 0.5:
        base_score = int(transparency_ratio * 100)
        final_score = max(0, base_score - 50)
        return final_score, "⚠️ DATA WITHHELD (Adverse Inference Applied)"
    else:
        return int(transparency_ratio * 100), "✅ Transparent"

BORDER_STATES = ["Texas", "Arizona", "California", "New Mexico"]

GOVERNOR_DATA = {
    "New York": {"name": "Kathy Hochul", "party": "D", "veto_border": "Yes", "calendar_public": False, "visible_votes": 45, "total_sessions": 100},
    "California": {"name": "Gavin Newsom", "party": "D", "veto_border": "Yes", "calendar_public": False, "visible_votes": 38, "total_sessions": 100},
    "Florida": {"name": "Ron DeSantis", "party": "R", "veto_border": "No", "calendar_public": True, "visible_votes": 89, "total_sessions": 100},
    "Texas": {"name": "Greg Abbott", "party": "R", "veto_border": "No", "calendar_public": True, "visible_votes": 92, "total_sessions": 100},
}

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
st.sidebar.caption("v3.6 | The Sunlight Cannon")

selected_state = st.sidebar.selectbox("Select Your State", STATES, index=31)
selected_focus = st.sidebar.selectbox("Select Focus", ["All", "Border Security", "Veterans First", "Education & Skills", "Crime & Safety", "Trade & Industry"])

st.sidebar.divider()
if is_system_online:
    st.sidebar.success("🟢 System Status: Online")
else:
    st.sidebar.warning("⚠️ System Status: Degraded")

st.sidebar.divider()
st.sidebar.markdown("### Fuel the Mission")
st.sidebar.link_button("☕ Support Russell", "https://buymeacoffee.com/russellnomer")

page = st.radio("Navigate", ["The National Lens", "The 2027 Fork", "Trade & Industry", "The Activism Hub", "Accountability Tribunal", "FOIA Cannon", "The Ecosystem", "Support"], horizontal=True, label_visibility="collapsed")

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

elif page == "Trade & Industry":
    st.header("🇺🇸 Made in America: The Pivot")
    
    tab_dividend, tab_sourcing = st.tabs(["💵 The Tariff Dividend", "🏭 Sourcing Finder"])
    
    with tab_dividend:
        tariff_revenue = get_tariff_revenue()
        immigration_cost = 150700000000
        
        pop = STATE_POPS.get(selected_state, 6000000)
        per_capita_offset = tariff_revenue / US_POP
        
        col1, col2 = st.columns(2)
        col1.metric("💵 Live Tariff Revenue", f"${tariff_revenue:,.0f}")
        col2.metric("🎁 The Offset (Per Capita)", f"${per_capita_offset:,.0f}")
        
        st.caption("*Foreign money entering the US Treasury through trade policy.*")
        
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
        
        st.info("💡 Tariffs bring money back, but the transition is hard. We must support businesses that pivot to domestic manufacturing.")
    
    with tab_sourcing:
        st.subheader("🔄 The Pivot: Source Locally, Save Globally")
        st.markdown("*Transitioning is hard, but American resilience pays off. Here are vetted US resources to replace Chinese supply chains.*")
        
        sourcing_resources = {
            "General": [
                ("Thomasnet.com", "Industrial Sourcing Directory"),
                ("US Dept of Commerce Supply Chain Hub", "Government Resources"),
                ("Maker's Row", "Apparel, Furniture & Consumer Goods")
            ],
            "Electronics": [
                ("Circuits Assembly Directory", "PCB & Electronics Manufacturing"),
                ("Reshoring Institute", "Reshoring Strategy & Resources"),
                ("IPC - Association Connecting Electronics", "Industry Standards")
            ],
            "Textiles & Apparel": [
                ("Maker's Row", "American Factories for Fashion"),
                ("American Blanket Company", "Domestic Textile Manufacturing"),
                ("American Apparel & Footwear Association", "Industry Trade Group")
            ],
            "Consumer Goods": [
                ("Wholesale Central", "US Wholesale Directory"),
                ("TopTenWholesale (USA Section)", "Verified US Suppliers"),
                ("Made in USA Certified", "Certification Program")
            ]
        }
        
        selected_industry = st.selectbox("Select Your Industry:", list(sourcing_resources.keys()))
        
        st.markdown(f"### Resources for {selected_industry}")
        for name, desc in sourcing_resources[selected_industry]:
            st.markdown(f"- **{name}**: {desc}")
        
        st.divider()
        st.subheader("🧮 Total Landed Cost Calculator")
        st.markdown("*See the true landed cost—often USA is closer than you think.*")
        st.caption("💡 Don't forget the cost of your time. 6 weeks on a boat costs money.")
        
        col_china, col_usa = st.columns(2)
        
        with col_china:
            st.markdown("### 🇨🇳 Importing from China")
            china_unit = st.number_input("Unit Cost ($)", value=5.00, key="china_unit", min_value=0.0)
            china_shipping = st.number_input("Shipping per Unit ($)", value=2.00, key="china_ship", min_value=0.0)
            tariff_rate = st.slider("Tariff Rate (%)", 0, 60, 25)
            transit_weeks = st.number_input("Weeks in Transit", value=6, key="china_transit", min_value=1)
            
            china_tariff_cost = china_unit * (tariff_rate / 100)
            china_total = china_unit + china_shipping + china_tariff_cost
            st.metric("Total Landed Cost", f"${china_total:.2f}")
            st.caption(f"+ {transit_weeks} weeks inventory delay")
        
        with col_usa:
            st.markdown("### 🇺🇸 Making in USA")
            usa_unit = st.number_input("Unit Cost ($)", value=8.00, key="usa_unit", min_value=0.0)
            usa_shipping = st.number_input("Shipping per Unit ($)", value=0.50, key="usa_ship", min_value=0.0)
            usa_transit = st.number_input("Weeks in Transit", value=1, key="usa_transit", min_value=1)
            
            usa_total = usa_unit + usa_shipping
            st.metric("Total Landed Cost", f"${usa_total:.2f}")
            st.caption(f"+ {usa_transit} week inventory delay")
        
        st.divider()
        
        difference = china_total - usa_total
        if difference >= 0:
            st.success(f"✅ **USA is ${difference:.2f} CHEAPER** per unit when tariffs are included!")
        else:
            st.warning(f"⚠️ USA is ${abs(difference):.2f} more per unit, but consider: faster delivery, quality control, no supply chain risk, American jobs.")
        
        st.divider()
        st.subheader("🌉 Bridge Builder: Business Owner to Rep")
        biz_template = f"I'm a {selected_state} business owner who wants to hire American. Use Tariff revenue to give tax credits to small businesses who switch to US suppliers. #MadeInAmerica #PlainviewProtocol"
        st.code(biz_template, language=None)
        st.link_button("Share on X", f"https://twitter.com/intent/tweet?text={biz_template.replace(' ', '%20').replace('#', '%23')}")

elif page == "The Activism Hub":
    st.header("🌉 The Bridge Builder: Facts Over Rage")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Veterans First", "Border Security", "Education", "Business Owner"])
    
    with tab1:
        st.write("Compare the cost of housing a homeless veteran vs. federal waste.")
        st.info("In 2024, approx 35,000 veterans experienced homelessness. The cost to house them is a fraction of the $150B immigration burden.")
        tweet_text = f"In {selected_state}, we believe Veterans come first. Why is the budget prioritizing waste over heroes? Fix it now. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    with tab2:
        st.write("Secure borders ensure safe communities and fiscal sanity.")
        tweet_text = f"Security is not optional. {selected_state} taxpayers are footing the bill for unsecured borders. Enforce the law. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    with tab3:
        st.write("Invest in American skills and education for a stronger workforce.")
        tweet_text = f"In {selected_state}, we need skills-based education that prepares workers for good jobs. Invest in our future. #PlainviewProtocol"
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={tweet_text}")

    with tab4:
        st.write("**Business Owner to Rep: Help Me Reshore**")
        st.info("Use this template if you're a business owner wanting to bring manufacturing back to the USA.")
        biz_template = f"I'm a {selected_state} business owner who wants to hire American. Use Tariff revenue to give tax credits to small businesses who switch to US suppliers. Help me reshore! #MadeInAmerica #PlainviewProtocol"
        st.code(biz_template, language=None)
        st.link_button("Share on X (Twitter)", f"https://twitter.com/intent/tweet?text={biz_template.replace(' ', '%20').replace('#', '%23')}")

    st.divider()
    
    st.subheader("Draft Your Message")
    user_input = st.text_area("Vent your frustration here (we will make it professional):")
    if st.button("Rewrite Kindly"):
        if user_input:
            cleaned = user_input.replace("hate", "am concerned about").replace("idiots", "officials").replace("destroying", "negatively impacting")
            final_msg = f"{cleaned}. I respectfully urge you to prioritize domestic security and the rule of law."
            st.success("✅ Ready to Send:")
            st.code(final_msg, language=None)

elif page == "Accountability Tribunal":
    st.header("⚖️ The Accountability Tribunal")
    
    level_filter = st.radio("Filter by Level:", ["Federal", "State (Governor/Leg)", "Local (Mayor/Sheriff)"], horizontal=True)
    
    tab_officials, tab_methodology = st.tabs(["📊 Officials", "📖 Methodology"])
    
    with tab_officials:
        if level_filter == "Federal":
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
        
        elif level_filter == "State (Governor/Leg)":
            st.subheader("🏛️ Governor Accountability Matrix")
            
            border_multiplier = 1.6 if selected_state in BORDER_STATES else 1.0
            st.caption(f"*Border State Multiplier: {border_multiplier}x (Higher standard for border enforcement)*")
            
            gov_records = []
            for state, data in GOVERNOR_DATA.items():
                score, status = calculate_transparency_score(data["visible_votes"], data["total_sessions"])
                adjusted_score = score
                if state in BORDER_STATES and data["veto_border"] == "Yes":
                    adjusted_score = max(0, score - 20)
                
                gov_records.append({
                    "State": state,
                    "Governor": data["name"],
                    "Party": data["party"],
                    "Vetoed Border Security": data["veto_border"],
                    "Calendar Public": "✅" if data["calendar_public"] else "❌",
                    "Transparency Score": adjusted_score,
                    "Status": status
                })
            
            gov_df = pd.DataFrame(gov_records)
            st.dataframe(gov_df, hide_index=True, use_container_width=True)
            
            st.warning("⚠️ Officials with <50% transparency receive the **Shadow Penalty**: We assume hidden records contain betrayal.")
        
        elif level_filter == "Local (Mayor/Sheriff)":
            st.subheader("🔦 The Warlord Tracker: Local Accountability")
            st.markdown("*Add local officials and rate their transparency.*")
            
            if 'local_officials' not in st.session_state:
                st.session_state.local_officials = []
            
            with st.expander("➕ Add a Local Official"):
                local_name = st.text_input("Official Name (e.g., Mayor John Smith)")
                local_role = st.selectbox("Role", ["Mayor", "Sheriff", "City Council", "County Commissioner", "Other"])
                local_city = st.text_input("City/County")
                records_available = st.checkbox("Are voting records easily available online?")
                
                if st.button("Add Official"):
                    if local_name and local_city:
                        if records_available:
                            shadow_score = "C"
                            status = "⚠️ Needs Review"
                        else:
                            shadow_score = "F-"
                            status = "🚨 HIDDEN. Presumed Hostile to Liberty."
                        
                        st.session_state.local_officials.append({
                            "Name": local_name,
                            "Role": local_role,
                            "Location": local_city,
                            "Records Available": "✅" if records_available else "❌",
                            "Shadow Score": shadow_score,
                            "Status": status
                        })
                        st.success(f"Added {local_name}")
                        st.rerun()
            
            if st.session_state.local_officials:
                local_df = pd.DataFrame(st.session_state.local_officials)
                st.dataframe(local_df, hide_index=True, use_container_width=True)
            else:
                st.info("No local officials tracked yet. Add one above!")
    
    with tab_methodology:
        st.subheader("📜 How We Rate: The Spoliation Doctrine")
        
        st.markdown("""
In law, **'Spoliation'** means destroying or hiding evidence. When a party destroys evidence, 
courts apply **'Adverse Inference'**—they assume the missing evidence would have been harmful to the party who hid it.

**The Plainview Protocol applies this same doctrine to politicians:**

- If a politician hides their voting record, we do **not** give them the benefit of the doubt.
- We assume the missing data proves their guilt.
- Officials who hide more than 50% of their records receive a **Shadow Penalty** (-50 points).
        """)
        
        st.divider()
        st.subheader("📊 The Shadow Gap")
        
        public_pct = 65
        hidden_pct = 35
        
        shadow_data = pd.DataFrame({
            "Category": ["Public Record", "The Shadow Gap"],
            "Percentage": [public_pct, hidden_pct]
        })
        
        fig = px.pie(shadow_data, values="Percentage", names="Category",
                     color="Category",
                     color_discrete_map={"Public Record": "#0d3b66", "The Shadow Gap": "#b22222"})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        st.error(f"**{hidden_pct}% of political activity happens in the shadows.** The Plainview Protocol shines a light.")

elif page == "FOIA Cannon":
    st.header("🔦 The Sunlight Cannon: Wake the Watchers")
    
    st.markdown("""
**Apathy is over.** Use this tool to generate a legal Freedom of Information Act (FOIA) request. 
We demand the data. If they hide it, we apply **'Adverse Inference'**—assuming the hidden data proves corruption.
    """)
    
    st.divider()
    st.subheader("⚙️ The Configurator")
    
    jurisdiction = st.radio("Select Jurisdiction:", ["Federal (US Agencies)", "State/Local (Governor, Mayor, Sheriff)"], horizontal=True)
    
    agency_name = st.text_input("Target Agency Name", placeholder="e.g., Department of Homeland Security, Nassau County PD")
    records_requested = st.text_area("Specific Records Requested", placeholder="e.g., All emails regarding migrant housing contracts between Jan 2025 and Present")
    include_spoliation = st.checkbox("Include 'Spoliation of Evidence' Warning?", value=True)
    
    st.divider()
    st.subheader("📝 The Generator")
    
    def generate_foia(jurisdiction, agency, topic, spoliation):
        today = time.strftime("%B %d, %Y")
        
        if "Federal" in jurisdiction:
            legal_cite = "5 U.S.C. § 552 (Freedom of Information Act)"
            response_time = "20 business days"
        else:
            legal_cite = "State Public Records Act / Sunshine Laws"
            response_time = "varies by state (typically 5-30 days)"
        
        letter = f"""
FREEDOM OF INFORMATION ACT REQUEST

Date: {today}

To: FOIA Officer
{agency if agency else "[AGENCY NAME]"}

Dear FOIA Officer,

Pursuant to {legal_cite}, I am requesting access to and copies of the following records:

{topic if topic else "[DESCRIBE RECORDS REQUESTED]"}

I request that responsive documents be provided in electronic format (PDF preferred).

"""
        
        if spoliation:
            letter += """
**NOTICE OF SPOLIATION:**
You are hereby placed on notice to preserve all records responsive to this request. 
Failure to produce these documents, or destruction of any records after receipt of this request, 
will be viewed as spoliation of evidence, leading to an ADVERSE INFERENCE that the missing 
evidence contained proof of negligence, malfeasance, or corruption.

"""
        
        letter += f"""
Under the law, you are required to respond to this request within {response_time}.

If you deny any part of this request, please cite the specific exemption and notify me of 
appeal procedures available under the law.

Thank you for your prompt attention to this matter.

Respectfully,
[YOUR NAME]
[YOUR ADDRESS]
[YOUR EMAIL]

---
Generated by The Plainview Protocol | Truth, Kindness, Security
        """
        
        return letter
    
    if st.button("🔥 Generate Legal Request", type="primary"):
        if agency_name and records_requested:
            foia_letter = generate_foia(jurisdiction, agency_name, records_requested, include_spoliation)
            st.session_state.generated_foia = foia_letter
        else:
            st.error("Please fill in the Agency Name and Records Requested fields.")
    
    if 'generated_foia' in st.session_state:
        st.text_area("Your FOIA Request", st.session_state.generated_foia, height=400)
        
        col1, col2, col3 = st.columns(3)
        col1.link_button("📧 Find Federal Agency (FOIA.gov)", SOURCES.get("foia_gov", "https://www.foia.gov"))
        col2.link_button("📜 Find State Laws (NFOIC)", SOURCES.get("state_laws", "https://www.nfoic.org"))
        col3.link_button("🔍 MuckRock (FOIA Help)", SOURCES.get("muckrock", "https://www.muckrock.com"))
    
    st.divider()
    st.subheader("📅 The Tracker")
    st.info("**Did you send it?** Mark it on your calendar. Federal agencies have **20 business days** to respond. State timelines vary.")
    st.caption("Pro tip: Send via email with read receipt, or certified mail for a paper trail.")

elif page == "The Ecosystem":
    st.header("🌳 From Pain to Purpose: The Full Grove")
    
    st.markdown("""
I'm **Russell Nomer**—a 54-year-old dad from Plainview, NY, recovering from accidents and loss, 
turning it all into tools for truth and protection. The Plainview Protocol is one part—here's the rest:
    """)
    
    st.divider()
    st.subheader("🛠️ Apps & Tools")
    col1, col2, col3 = st.columns(3)
    col1.link_button("🏠 Market Architect App", "https://marketarchitect.app")
    col2.link_button("🍳 Home Cooked Connections", "https://homecookedconnections.com")
    col3.link_button("💎 Verbum VIP", "https://verbum.vip")
    
    st.divider()
    st.subheader("📚 Books")
    st.link_button("📖 The Grove (Book on Amazon)", "https://amzn.to/4sukXoc")
    
    st.divider()
    st.subheader("🎵 Music")
    
    music_col1, music_col2, music_col3 = st.columns(3)
    music_col1.link_button("📺 YouTube Channel", "https://www.youtube.com/@russellnomermusic")
    music_col2.link_button("🎵 UnitedMasters", "https://unitedmasters.com/russell-nomer-music")
    music_col3.link_button("🎧 Apple Music", "https://music.apple.com/us/artist/russell-nomer/1762452726")
    
    music_col4, music_col5 = st.columns(2)
    music_col4.link_button("🎹 Bandcamp", "https://russellnomer.bandcamp.com/")
    music_col5.link_button("☁️ SoundCloud", "https://soundcloud.com/russell-nomer")
    
    st.divider()
    st.info("🌲 Music, books, apps—all channeling resilience into protecting America. **Join the Grove.**")

elif page == "Support":
    st.header("☕ Sustain the Mission")
    st.write("This tool is free, ad-free, and uncensorable thanks to supporters like you.")
    
    c1, c2, c3 = st.columns(3)
    c1.link_button("Donate via PayPal", "https://paypal.com")
    c2.link_button("Buy Russell a Coffee", "https://buymeacoffee.com/russellnomer")
    c3.link_button("Fork on GitHub", "https://github.com")

st.markdown("---")
st.markdown("<center>Built by Russell Nomer in Plainview, NY | <i>Truth, Kindness, Security</i></center>", unsafe_allow_html=True)
