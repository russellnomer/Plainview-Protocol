"""
Sunlight Flare Animation Logic for The Plainview Protocol V6.15

This module provides the CSS animations and JavaScript logic for
the Sunlight Flare victory notifications on the Corruption Heatmap.
"""

FLARE_CSS = """
<style>
@keyframes sunlight-pulse {
    0% { 
        box-shadow: 0 0 5px #FFD700, 0 0 10px #FFD700, 0 0 15px #FFD700;
        transform: scale(1);
    }
    50% { 
        box-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700, 0 0 60px #FFD700;
        transform: scale(1.1);
    }
    100% { 
        box-shadow: 0 0 5px #FFD700, 0 0 10px #FFD700, 0 0 15px #FFD700;
        transform: scale(1);
    }
}

.sunlight-flare {
    animation: sunlight-pulse 2s infinite;
    background: linear-gradient(135deg, #FFD700, #FFA500);
    border-radius: 50%;
    padding: 20px;
    text-align: center;
    color: #000;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.sunlight-flare:hover {
    transform: scale(1.2);
    box-shadow: 0 0 40px #FFD700, 0 0 80px #FFD700;
}

.flare-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 215, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    animation: flare-fade 3s forwards;
}

@keyframes flare-fade {
    0% { opacity: 1; }
    70% { opacity: 1; }
    100% { opacity: 0; }
}

.victory-modal {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 3px solid #FFD700;
    border-radius: 15px;
    padding: 30px;
    max-width: 500px;
    color: white;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
}

.victory-modal h2 {
    color: #FFD700;
    text-align: center;
    margin-bottom: 20px;
}

.victory-stat {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255, 215, 0, 0.3);
}

.vampire-tax-ticker {
    font-family: 'Courier New', monospace;
    font-size: 24px;
    color: #ff4444;
    background: #1a1a1a;
    padding: 10px 20px;
    border-radius: 5px;
    display: inline-block;
    animation: ticker-pulse 1s infinite;
}

@keyframes ticker-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
</style>
"""

def generate_flare_html(county, state, sentinel_name, target_entity, document_link, impact_score):
    """Generate the HTML for a Sunlight Flare victory notification."""
    return f"""
    <div class="sunlight-flare" onclick="showVictoryModal()">
        ☀️ SUNLIGHT! Document Released in {county} County, {state}!
    </div>
    
    <div id="victoryModal" class="victory-modal" style="display: none;">
        <h2>☀️ SUNLIGHT VICTORY ☀️</h2>
        <div class="victory-stat">
            <span>Sentinel:</span>
            <span>{sentinel_name}</span>
        </div>
        <div class="victory-stat">
            <span>Target Entity:</span>
            <span>{target_entity}</span>
        </div>
        <div class="victory-stat">
            <span>Location:</span>
            <span>{county} County, {state}</span>
        </div>
        <div class="victory-stat">
            <span>Impact Score:</span>
            <span>{impact_score}/100</span>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <a href="{document_link}" target="_blank" 
               style="background: #FFD700; color: #000; padding: 10px 20px; 
                      border-radius: 5px; text-decoration: none; font-weight: bold;">
                📄 View Released Document
            </a>
        </div>
    </div>
    """

def generate_vampire_tax_ticker(base_amount, days_accrued, daily_rate=0.01):
    """Generate a real-time vampire tax ticker that increments."""
    current_total = base_amount + (days_accrued * 86400 * daily_rate)
    return f"""
    <div class="vampire-tax-ticker" id="vampireTax">
        💀 VAMPIRE TAX OWED: ${current_total:,.2f}
    </div>
    <script>
        let taxAmount = {current_total};
        setInterval(() => {{
            taxAmount += 0.01;
            document.getElementById('vampireTax').innerHTML = 
                '💀 VAMPIRE TAX OWED: $' + taxAmount.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
        }}, 1000);
    </script>
    """

def calculate_vampire_tax(num_principals, days_in_shadow, shadow_income):
    """
    Calculate the total Vampire Tax liability.
    
    Formula: ($250,000 * num_principals) + ($1,000 * days) + shadow_income
    
    Legal basis:
    - 22 U.S.C. § 618(a): Criminal penalties for FARA violations
    - 18 U.S.C. § 3571: Fine schedule for federal offenses
    """
    base_penalty = 250000 * num_principals
    daily_penalty = 1000 * days_in_shadow
    total = base_penalty + daily_penalty + shadow_income
    
    return {
        "base_penalty": base_penalty,
        "daily_penalty": daily_penalty,
        "shadow_income": shadow_income,
        "total_liability": total
    }

def generate_treasury_invoice(agent_name, total_liability, principals, days_unregistered):
    """Generate a mock Treasury invoice for the Vampire Tax."""
    from datetime import date
    
    return f"""
════════════════════════════════════════════════════════════════════════════════
                    UNITED STATES DEPARTMENT OF THE TREASURY
                         INTERNAL REVENUE SERVICE
                    OFFICE OF FOREIGN AGENTS COMPLIANCE
════════════════════════════════════════════════════════════════════════════════

                            NOTICE OF TAX LIABILITY

DATE: {date.today().strftime("%B %d, %Y")}

TAXPAYER: {agent_name}
STATUS: UNREGISTERED FOREIGN AGENT

════════════════════════════════════════════════════════════════════════════════

                            VAMPIRE TAX ASSESSMENT

PURSUANT TO 22 U.S.C. § 618(a) AND 18 U.S.C. § 3571

CALCULATION:
    Base Penalty ({principals} principals × $250,000):     ${250000 * principals:>15,}
    Daily Continuing Offense ({days_unregistered} days × $1,000):   ${1000 * days_unregistered:>15,}
    Shadow Income Recovery:                                ${total_liability - (250000 * principals) - (1000 * days_unregistered):>15,}
                                                           ─────────────────
    TOTAL VAMPIRE TAX OWED:                                ${total_liability:>15,}

════════════════════════════════════════════════════════════════════════════════

PAYMENT INSTRUCTIONS:
    Make check payable to: U.S. Department of the Treasury
    Mail to: FARA Unit, National Security Division
             175 N Street NE
             Washington, DC 20002

FAILURE TO PAY within 30 days will result in additional penalties and
potential criminal prosecution under federal law.

════════════════════════════════════════════════════════════════════════════════
                    Generated by The Plainview Protocol V6.15
                    "FARA isn't just a paperwork error; it's a debt."
════════════════════════════════════════════════════════════════════════════════
"""
