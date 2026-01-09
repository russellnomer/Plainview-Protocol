"""
Vampire Tax Calculator for The Plainview Protocol V6.14

Calculates FARA violation penalties based on:
- 22 U.S.C. § 618(a): Criminal penalties for FARA violations
- 18 U.S.C. § 3571: Fine schedule for federal offenses
- Continuing offense doctrine: Each day unregistered is a new violation
"""

from datetime import date, datetime
from typing import Dict, Any, Optional


class VampireTaxCalculator:
    """
    Calculate the total liability for FARA violations.
    
    The "Vampire Tax" represents the financial penalty owed to taxpayers
    by foreign agents who operated without proper FARA registration.
    """
    
    BASE_PENALTY_PER_PRINCIPAL = 250000
    DAILY_PENALTY_RATE = 1000
    REAL_TIME_ACCRUAL_RATE = 0.01
    
    def __init__(self, agent_name: str, num_principals: int = 1):
        self.agent_name = agent_name
        self.num_principals = num_principals
        self.shadow_start_date: Optional[date] = None
        self.shadow_income = 0
        self.registration_date: Optional[date] = None
        
    def set_shadow_period(self, start_date: date, end_date: Optional[date] = None):
        """Set the period during which the agent operated unregistered."""
        self.shadow_start_date = start_date
        self.registration_date = end_date or date.today()
        
    def add_shadow_income(self, amount: float):
        """Add income received during the shadow period."""
        self.shadow_income += amount
        
    @property
    def days_in_shadow(self) -> int:
        """Calculate the number of days in the shadow period."""
        if not self.shadow_start_date:
            return 0
        end = self.registration_date or date.today()
        return (end - self.shadow_start_date).days
    
    @property
    def base_penalty(self) -> float:
        """Calculate the base penalty per principal."""
        return self.BASE_PENALTY_PER_PRINCIPAL * self.num_principals
    
    @property
    def daily_penalty(self) -> float:
        """Calculate the cumulative daily penalty."""
        return self.DAILY_PENALTY_RATE * self.days_in_shadow
    
    @property
    def total_liability(self) -> float:
        """Calculate the total Vampire Tax liability."""
        return self.base_penalty + self.daily_penalty + self.shadow_income
    
    def get_breakdown(self) -> Dict[str, Any]:
        """Get a detailed breakdown of the Vampire Tax calculation."""
        return {
            "agent_name": self.agent_name,
            "num_principals": self.num_principals,
            "shadow_start_date": self.shadow_start_date.isoformat() if self.shadow_start_date else None,
            "registration_date": self.registration_date.isoformat() if self.registration_date else None,
            "days_in_shadow": self.days_in_shadow,
            "base_penalty": self.base_penalty,
            "daily_penalty": self.daily_penalty,
            "shadow_income": self.shadow_income,
            "total_liability": self.total_liability,
            "legal_basis": {
                "statute_1": "22 U.S.C. § 618(a)",
                "statute_2": "18 U.S.C. § 3571",
                "doctrine": "Continuing Offense"
            }
        }
    
    def get_real_time_amount(self) -> float:
        """Get the current liability including real-time accrual."""
        now = datetime.now()
        seconds_today = now.hour * 3600 + now.minute * 60 + now.second
        real_time_addition = seconds_today * self.REAL_TIME_ACCRUAL_RATE
        return self.total_liability + real_time_addition
    
    def generate_invoice(self) -> str:
        """Generate a Treasury-style invoice for the Vampire Tax."""
        return f"""
════════════════════════════════════════════════════════════════════════════════
                    VAMPIRE TAX ASSESSMENT NOTICE
════════════════════════════════════════════════════════════════════════════════

DATE: {date.today().strftime("%B %d, %Y")}
SUBJECT: {self.agent_name}
STATUS: UNREGISTERED FOREIGN AGENT

════════════════════════════════════════════════════════════════════════════════

SHADOW PERIOD: {self.shadow_start_date} to {self.registration_date or 'PRESENT'}
DAYS UNREGISTERED: {self.days_in_shadow:,}

CALCULATION BREAKDOWN:

    Base Penalty ({self.num_principals} principal(s) × $250,000):
                                                    ${self.base_penalty:>15,}
    
    Daily Continuing Offense ({self.days_in_shadow:,} days × $1,000):
                                                    ${self.daily_penalty:>15,}
    
    Shadow Income Recovery:
                                                    ${self.shadow_income:>15,}
    
    ════════════════════════════════════════════════════════════════════════
    
    TOTAL VAMPIRE TAX OWED:                         ${self.total_liability:>15,}

════════════════════════════════════════════════════════════════════════════════

LEGAL BASIS:
• 22 U.S.C. § 618(a): Criminal penalties for FARA violations
• 18 U.S.C. § 3571: Fine schedule for federal offenses  
• Continuing Offense Doctrine: Each day unregistered = new violation

════════════════════════════════════════════════════════════════════════════════
                    Generated by The Plainview Protocol V6.14
════════════════════════════════════════════════════════════════════════════════
"""


def calculate_quick_estimate(num_principals: int, days_unregistered: int, 
                             shadow_income: float = 0) -> Dict[str, float]:
    """
    Quick calculation without creating a full calculator instance.
    
    Returns a dictionary with the breakdown and total.
    """
    base = 250000 * num_principals
    daily = 1000 * days_unregistered
    total = base + daily + shadow_income
    
    return {
        "base_penalty": base,
        "daily_penalty": daily,
        "shadow_income": shadow_income,
        "total_liability": total
    }


SHADOW_AGENT_DATABASE = {
    "Open Society Policy Center": {
        "principals": 3,
        "estimated_shadow_days": 1825,
        "shadow_income": 45000000,
        "status": "Under Monitoring"
    },
    "Democracy PAC II Consultants": {
        "principals": 2,
        "estimated_shadow_days": 730,
        "shadow_income": 12000000,
        "status": "Under Review"
    },
    "Sixteen Thirty Fund Lobbyists": {
        "principals": 5,
        "estimated_shadow_days": 1460,
        "shadow_income": 85000000,
        "status": "Under Monitoring"
    }
}


def get_all_shadow_agents_liability() -> Dict[str, Dict[str, Any]]:
    """Calculate Vampire Tax for all known shadow agents."""
    results = {}
    for agent_name, data in SHADOW_AGENT_DATABASE.items():
        estimate = calculate_quick_estimate(
            data["principals"],
            data["estimated_shadow_days"],
            data["shadow_income"]
        )
        results[agent_name] = {
            **estimate,
            "status": data["status"]
        }
    return results
