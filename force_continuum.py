"""
Force Continuum Module - V8.9
The Plainview Protocol

Physics-based analysis of vehicle impact force,
legal citation overlay for use of force policy,
and Cost of Open Borders ticker.

"Physics doesn't care about politics."
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import time
from fact_check_builder import get_fact_check_card, get_hashtags

CFR_287_8_TEXT = """
**8 CFR 287.8 — Use of Force Standards**

(a)(2) **Use of deadly force.** Deadly force may be used only when a 
designated immigration officer, as specified below, has a reasonable 
belief that the subject of such force poses an imminent danger of 
death or serious physical injury to the officer or other persons.

**Key Provision:**

> *"Firearms may be discharged at a moving vehicle only when a 
> designated immigration officer has a reasonable belief that:*
>
> *(i) The vehicle is operated in a manner that threatens to cause 
> death or serious physical injury to the officer or others; and*
>
> *(ii) There is no other reasonable alternative to prevent the 
> threat."*

**Source:** Code of Federal Regulations, Title 8, Section 287.8
"""

FAIR_2024_DATA = {
    "total_annual_cost": 150700000000,
    "taxpayers": 130000000,
    "cost_per_taxpayer": 1156,
    "cost_per_second": 4778,
    "source": "House Budget Committee / FAIR 2023-2024 Analysis",
    "components": {
        "education": 70000000000,
        "healthcare": 29000000000,
        "welfare": 9000000000,
        "justice": 25000000000,
        "other": 17700000000
    }
}

DEPORTATION_COST = 10854

def calculate_kinetic_energy(mass_kg: float, velocity_mps: float) -> float:
    """Calculate kinetic energy in Joules: KE = 0.5 * m * v^2"""
    return 0.5 * mass_kg * (velocity_mps ** 2)

def lbs_to_kg(lbs: float) -> float:
    """Convert pounds to kilograms."""
    return lbs * 0.453592

def mph_to_mps(mph: float) -> float:
    """Convert miles per hour to meters per second."""
    return mph * 0.44704

def get_bullet_energy() -> dict:
    """Get reference bullet kinetic energies in Joules."""
    return {
        "9mm Handgun": 519,
        ".45 ACP": 477,
        "5.56 NATO (AR-15)": 1767,
        "7.62x39 (AK-47)": 2010,
        ".308 Winchester": 3500
    }

def render_force_continuum():
    """Render the Force Continuum dashboard."""
    st.header("⚖️ Force Continuum — Physics & Law")
    st.caption("V8.9 — Understanding Deadly Force Standards")
    
    st.info("""
    *"Physics doesn't care about politics. When a 4,000-lb vehicle is 
    accelerated toward a human being, the laws of physics apply 
    regardless of the driver's intentions or affiliations."*
    """)
    
    st.divider()
    
    tabs = st.tabs(["⚡ Impact Calculator", "📜 Legal Framework", "💰 Cost Ticker", "📊 Analysis", "🛡️ Narrative Shield"])
    
    with tabs[0]:
        st.subheader("⚡ Vehicle Impact Energy Calculator")
        st.caption("Kinetic energy comparison: Vehicle vs. Firearm projectiles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            vehicle_weight = st.slider("Vehicle Weight (lbs)", 2000, 8000, 4000, 100)
            vehicle_speed = st.slider("Vehicle Speed (mph)", 5, 60, 25, 5)
        
        weight_kg = lbs_to_kg(vehicle_weight)
        speed_mps = mph_to_mps(vehicle_speed)
        vehicle_energy = calculate_kinetic_energy(weight_kg, speed_mps)
        
        bullet_data = get_bullet_energy()
        
        with col2:
            st.metric("Vehicle Kinetic Energy", f"{vehicle_energy:,.0f} Joules")
            st.metric("Equivalent to", f"{vehicle_energy / bullet_data['9mm Handgun']:.1f}x a 9mm bullet")
        
        st.divider()
        
        categories = list(bullet_data.keys()) + [f"Vehicle ({vehicle_weight} lbs @ {vehicle_speed} mph)"]
        energies = list(bullet_data.values()) + [vehicle_energy]
        colors = ['#636EFA'] * len(bullet_data) + ['#EF553B']
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=energies,
                marker_color=colors,
                text=[f"{e:,.0f} J" for e in energies],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Kinetic Energy Comparison (Joules)",
            xaxis_title="Projectile / Vehicle",
            yaxis_title="Energy (Joules)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.warning(f"""
        **Physics Analysis:**
        
        A {vehicle_weight:,} lb vehicle traveling at {vehicle_speed} mph delivers 
        **{vehicle_energy:,.0f} Joules** of kinetic energy upon impact.
        
        This is equivalent to being struck by **{vehicle_energy / bullet_data['9mm Handgun']:.1f} 
        simultaneous 9mm bullets** or **{vehicle_energy / bullet_data['5.56 NATO (AR-15)']:.1f} 
        AR-15 rounds**.
        
        Under federal use-of-force guidelines, a vehicle operated aggressively 
        toward personnel constitutes a deadly weapon requiring appropriate response.
        """)
    
    with tabs[1]:
        st.subheader("📜 Legal Framework — Use of Force")
        st.caption("Federal regulations governing immigration enforcement")
        
        st.markdown(CFR_287_8_TEXT)
        
        st.divider()
        
        st.markdown("**Key Legal Principles:**")
        
        st.success("""
        **1. Objective Reasonableness Standard**
        
        The Supreme Court in *Graham v. Connor* (1989) established that use of force 
        must be judged from the perspective of a reasonable officer on the scene, 
        not with 20/20 hindsight.
        """)
        
        st.info("""
        **2. Vehicle as Deadly Weapon**
        
        Under federal and state law, a motor vehicle operated in a manner that 
        threatens death or serious bodily injury is legally classified as a 
        deadly weapon, equivalent to a firearm.
        """)
        
        st.warning("""
        **3. Duty to Self-Preserve**
        
        Law enforcement officers have both a right and duty to protect themselves 
        and others from imminent deadly threats using proportionate force.
        """)
    
    with tabs[2]:
        st.subheader("💰 Cost of Open Borders — Live Ticker")
        st.caption(f"Source: {FAIR_2024_DATA['source']}")
        
        st.markdown("""
        <style>
        .cost-ticker-wrap {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .cost-ticker-wrap h3, .cost-ticker-wrap .big-number {
            white-space: nowrap;
            font-size: 1.5rem;
        }
        .cost-headline {
            white-space: nowrap;
            font-weight: bold;
            font-size: 1.4rem;
        }
        @media (max-width: 400px) {
            .cost-ticker-wrap h3, .cost-ticker-wrap .big-number {
                font-size: 1.1rem;
            }
            .cost-headline {
                font-size: 1rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        cost_placeholder = st.empty()
        
        base_time = datetime(2026, 1, 1, 0, 0, 0)
        now = datetime.now()
        seconds_elapsed = (now - base_time).total_seconds()
        accumulated_cost = seconds_elapsed * FAIR_2024_DATA["cost_per_second"]
        
        with cost_placeholder.container():
            st.markdown(f"""
            <div class="cost-ticker-wrap" style="background: #ffcccc; padding: 15px; border-radius: 8px; border-left: 4px solid #b22222;">
                <span class="cost-headline">💸 2026 Running Total: ${accumulated_cost:,.0f}</span><br>
                <span style="font-style: italic; white-space: nowrap;">Adding ${FAIR_2024_DATA['cost_per_second']:,} every second...</span>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Annual Cost", f"${FAIR_2024_DATA['total_annual_cost']/1e9:.1f}B")
        col2.metric("Cost per Taxpayer", f"${FAIR_2024_DATA['cost_per_taxpayer']:,}/year")
        col3.metric("Cost per Second", f"${FAIR_2024_DATA['cost_per_second']:,}")
        
        st.divider()
        
        st.markdown("**Cost Breakdown:**")
        
        breakdown_fig = go.Figure(data=[go.Pie(
            labels=list(FAIR_2024_DATA["components"].keys()),
            values=list(FAIR_2024_DATA["components"].values()),
            textinfo='label+percent',
            hole=0.4
        )])
        
        breakdown_fig.update_layout(
            title=dict(
                text="Annual Cost Distribution ($150.7B Total)",
                font=dict(size=14)
            ),
            height=350,
            margin=dict(t=40, b=20)
        )
        
        st.plotly_chart(breakdown_fig, use_container_width=True)
        
        st.divider()
        
        st.markdown("**Protest vs. Enforcement Cost Comparison:**")
        
        protest_col1, protest_col2 = st.columns(2)
        
        with protest_col1:
            st.error(f"""
            **Average Deportation Cost:**
            ${DEPORTATION_COST:,} per individual
            
            *Source: ICE FY2023 Budget Data*
            """)
        
        with protest_col2:
            st.warning("""
            **Average Protest Response Cost:**
            $50,000 - $200,000 per event
            
            *Includes: Police overtime, barriers, cleanup*
            """)
    
    with tabs[3]:
        st.subheader("📊 Data Analysis")
        st.caption("Verified sources and methodology")
        
        st.markdown("""
        **Data Sources:**
        
        1. **Vehicle Kinetic Energy:** Standard physics formula KE = ½mv²
        2. **Bullet Energy Data:** Manufacturer specifications, FBI ballistics
        3. **Immigration Cost:** House Budget Committee, FAIR 2023-2024 Analysis
        4. **Legal Citations:** Code of Federal Regulations, Title 8
        5. **Deportation Cost:** ICE Congressional Budget Justification FY2023
        
        **Methodology:**
        - All calculations use peer-reviewed physics formulas
        - Cost data sourced from official government reports
        - Legal text quoted directly from CFR
        """)
        
        with st.expander("📋 Full Data Sources"):
            st.markdown("""
            - 8 CFR 287.8: https://www.ecfr.gov/current/title-8/chapter-I/subchapter-B/part-287
            - Graham v. Connor, 490 U.S. 386 (1989)
            - FAIR Fiscal Burden Study: https://www.fairus.org/issue/publications-resources/fiscal-burden-illegal-immigration-united-states-taxpayers
            - ICE Budget: https://www.dhs.gov/immigration-statistics
            """)
    
    with tabs[4]:
        st.subheader("🛡️ Narrative Shield Generator")
        st.caption("V6.28 — The Ammo Box")
        
        st.success("""
        *"The lie travels halfway around the world while the truth is putting on its shoes. 
        We gave the truth a Ferrari. Download the card. Post it. Kill the narrative."*
        
        — Russell David Nomer, Founder
        """)
        
        st.divider()
        
        st.markdown("**Generate a shareable Fact Check graphic:**")
        
        if st.button("🛡️ Generate Truth Card", use_container_width=True, type="primary"):
            st.session_state.truth_card_generated = True
        
        if st.session_state.get("truth_card_generated", False):
            try:
                card_bytes = get_fact_check_card()
                
                st.image(card_bytes, caption="Narrative Shield — Fact Check Card", use_container_width=True)
                
                st.download_button(
                    "📥 Download High-Res PNG",
                    data=card_bytes,
                    file_name="plainview_fact_check.png",
                    mime="image/png",
                    use_container_width=True
                )
                
            except Exception as e:
                st.warning("Card generation loading. Please try again.")
        
        st.divider()
        
        st.markdown("**📋 Copy & Fire Social Pack:**")
        
        hashtags = get_hashtags()
        st.code(hashtags, language=None)
        
        st.markdown("""
        <script>
        function copyHashtags() {
            navigator.clipboard.writeText('%s');
        }
        </script>
        """ % hashtags, unsafe_allow_html=True)
        
        st.info("""
        **How to use:**
        1. Click "Generate Truth Card" above
        2. Download the high-res PNG
        3. Copy the hashtags above
        4. Post to X/Twitter or Facebook with the image and hashtags
        
        *Every share is a counter-strike against misinformation.*
        """)
        
        with st.expander("ℹ️ Card Contents"):
            st.markdown("""
            **Header:** FACT CHECK: "SHE WAS JUST DRIVING AWAY"
            
            **Panel A (Visual):**
            - Honda Pilot silhouette (~4,300 lbs)
            - Force multiplier arrow showing acceleration
            
            **Panel B (Data):**
            - THE CLAIM: Peaceful exit
            - THE REALITY: Vehicle = Deadly Weapon
            - THE LAW: 8 CFR 287.8 authorizes response
            
            **Verdict:** FALSE (Stamped)
            
            **Sources cited:** CFR, Graham v. Connor, Physics
            """)
    
    st.divider()
    
    st.markdown("""
    **🏛️ The Plainview Position:**
    
    This module provides factual, physics-based analysis of force dynamics 
    and publicly available cost data. All sources are cited and verifiable. 
    The Protocol takes no position on individual cases but provides the 
    tools for citizens to understand the legal and fiscal frameworks 
    governing immigration enforcement.
    
    *Facts over feelings. Data over narrative.*
    """)
