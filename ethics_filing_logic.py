"""
Ethics Filing Logic for The Plainview Protocol V6.17

This module generates formal ethics complaints for:
- Office of Congressional Conduct (OCC) - House
- Senate Select Committee on Ethics - Senate

Legal basis: 18 U.S.C. § 207 (Restrictions on former officers and employees)
"""

from datetime import date
from typing import Dict, Any, Optional


def generate_occ_complaint(
    complainant_name: str,
    complainant_email: str,
    lobbyist_name: str,
    former_role: str,
    government_exit_date: str,
    current_employer: str,
    first_lobby_contact: str,
    target_agency: str,
    evidence_summary: str
) -> str:
    """
    Generate a formal complaint for the Office of Congressional Conduct (House).
    
    The OCC replaced the Office of Congressional Ethics in January 2026.
    """
    return f"""
FORMAL COMPLAINT TO THE OFFICE OF CONGRESSIONAL CONDUCT

════════════════════════════════════════════════════════════════════════════════
                    UNITED STATES HOUSE OF REPRESENTATIVES
                      OFFICE OF CONGRESSIONAL CONDUCT (OCC)
                         ETHICS COMPLAINT SUBMISSION
════════════════════════════════════════════════════════════════════════════════

DATE: {date.today().strftime("%B %d, %Y")}

COMPLAINANT INFORMATION:
    Name: {complainant_name}
    Email: {complainant_email}

════════════════════════════════════════════════════════════════════════════════

SUBJECT OF COMPLAINT: Potential 18 U.S.C. § 207 Violation

RESPONDENT:
    Name: {lobbyist_name}
    Former Government Role: {former_role}
    Government Exit Date: {government_exit_date}
    Current Employer: {current_employer}
    First Registered Lobbying Contact: {first_lobby_contact}
    Target Agency of Lobbying: {target_agency}

════════════════════════════════════════════════════════════════════════════════

NATURE OF ALLEGED VIOLATION:

Pursuant to 18 U.S.C. § 207, I submit this complaint alleging that the above-named
individual has engaged in lobbying activities within the 730-day restricted period
following their departure from federal service.

Specifically, {lobbyist_name} departed their position as {former_role} on 
{government_exit_date} and subsequently registered as a lobbyist or engaged in
lobbying activities with {current_employer} on or about {first_lobby_contact}.

This contact occurred within the two-year cooling-off period mandated by federal
ethics law, potentially constituting a violation of post-employment restrictions.

════════════════════════════════════════════════════════════════════════════════

EVIDENCE SUMMARY:

{evidence_summary}

════════════════════════════════════════════════════════════════════════════════

LEGAL BASIS:

18 U.S.C. § 207 - Restrictions on former officers, employees, and elected 
officials of the executive and legislative branches:

(a) RESTRICTIONS ON ALL OFFICERS AND EMPLOYEES OF THE EXECUTIVE BRANCH AND 
    CERTAIN OTHER AGENCIES -
    
    Any person who is an officer or employee of the executive branch... and who,
    after the termination of his or her service... knowingly makes, with the 
    intent to influence, any communication to or appearance before any officer
    or employee of any department, agency, court, or court-martial of the 
    United States...
    
(c) ONE-YEAR RESTRICTIONS ON AIDING OR ADVISING -
    
    Any person who is a former senior employee... shall not, within 1 year
    after the termination of his or her employment... knowingly represent,
    aid, or advise any other person (except the United States) concerning
    any ongoing trade or treaty negotiation...

(d) TWO-YEAR RESTRICTIONS ON AIDING OR ADVISING CERTAIN TRADE MATTERS -

    The two-year window applies to senior officials who participated personally
    and substantially in trade or treaty negotiations.

════════════════════════════════════════════════════════════════════════════════

DECLARATION UNDER 18 U.S.C. § 1001 (FALSE STATEMENTS ACT):

I, {complainant_name}, hereby declare under penalty of perjury pursuant to 
18 U.S.C. § 1001 that the foregoing statements are true and correct to the 
best of my knowledge, information, and belief.

Signature: ______________________________

Date: {date.today().strftime("%B %d, %Y")}

════════════════════════════════════════════════════════════════════════════════

REQUEST FOR ACTION:

I respectfully request that the Office of Congressional Conduct:

1. Initiate a Preliminary Inquiry into the above-described conduct;
2. Issue a Notice of Review to the respondent's current employer;
3. If warranted, refer the matter to the Department of Justice for criminal
   prosecution under 18 U.S.C. § 207.

════════════════════════════════════════════════════════════════════════════════

SUBMISSION INSTRUCTIONS:

Mail to:
    Office of Congressional Conduct
    425 3rd Street SW, Suite 1110
    Washington, DC 20024

Email: complaints@occ.house.gov (if available)

════════════════════════════════════════════════════════════════════════════════
                    Generated by The Plainview Protocol V6.17
                    "The cooling-off period is a wall, not a suggestion."
════════════════════════════════════════════════════════════════════════════════
"""


def generate_senate_ethics_complaint(
    complainant_name: str,
    complainant_email: str,
    lobbyist_name: str,
    former_role: str,
    government_exit_date: str,
    current_employer: str,
    first_lobby_contact: str,
    target_agency: str,
    evidence_summary: str
) -> str:
    """
    Generate a formal complaint for the Senate Select Committee on Ethics.
    """
    return f"""
FORMAL COMPLAINT TO THE SENATE SELECT COMMITTEE ON ETHICS

════════════════════════════════════════════════════════════════════════════════
                         UNITED STATES SENATE
               SELECT COMMITTEE ON ETHICS
                    ETHICS COMPLAINT SUBMISSION
════════════════════════════════════════════════════════════════════════════════

DATE: {date.today().strftime("%B %d, %Y")}

COMPLAINANT INFORMATION:
    Name: {complainant_name}
    Email: {complainant_email}

════════════════════════════════════════════════════════════════════════════════

SUBJECT OF COMPLAINT: Potential 18 U.S.C. § 207 Violation

RESPONDENT:
    Name: {lobbyist_name}
    Former Senate Role: {former_role}
    Senate Exit Date: {government_exit_date}
    Current Employer: {current_employer}
    First Registered Lobbying Contact: {first_lobby_contact}
    Target of Lobbying: {target_agency}

════════════════════════════════════════════════════════════════════════════════

ALLEGATION:

I respectfully submit this complaint alleging that {lobbyist_name}, a former
Senate employee who served as {former_role}, has potentially violated the
post-employment lobbying restrictions under 18 U.S.C. § 207.

The respondent departed Senate service on {government_exit_date} and
subsequently engaged in lobbying activities for {current_employer} on or
about {first_lobby_contact}, which falls within the restricted cooling-off
period.

════════════════════════════════════════════════════════════════════════════════

EVIDENCE SUMMARY:

{evidence_summary}

════════════════════════════════════════════════════════════════════════════════

DECLARATION UNDER 18 U.S.C. § 1001:

I, {complainant_name}, declare under penalty of perjury that the statements
contained in this complaint are true and correct to the best of my knowledge.

Signature: ______________________________

Date: {date.today().strftime("%B %d, %Y")}

════════════════════════════════════════════════════════════════════════════════

SUBMISSION:

Mail to:
    Senate Select Committee on Ethics
    220 Hart Senate Office Building
    Washington, DC 20510

════════════════════════════════════════════════════════════════════════════════
                    Generated by The Plainview Protocol V6.17
════════════════════════════════════════════════════════════════════════════════
"""


def calculate_cooling_off_days(exit_date: str, contact_date: str) -> Dict[str, Any]:
    """
    Calculate the number of days between government exit and first lobbying contact.
    
    Returns violation status based on 730-day (2-year) window.
    """
    from datetime import datetime
    
    try:
        exit = datetime.strptime(exit_date, "%Y-%m-%d")
        contact = datetime.strptime(contact_date, "%Y-%m-%d")
        days_elapsed = (contact - exit).days
        days_remaining = 730 - days_elapsed
        
        return {
            "days_elapsed": days_elapsed,
            "days_remaining": max(0, days_remaining),
            "cooling_off_expired": days_elapsed >= 730,
            "violation_flag": days_elapsed < 730,
            "severity": "CRITICAL" if days_elapsed < 365 else "WARNING" if days_elapsed < 730 else "CLEAR"
        }
    except ValueError:
        return {
            "error": "Invalid date format. Use YYYY-MM-DD.",
            "days_elapsed": None,
            "violation_flag": None
        }


def get_sunlight_cc_recipients(state: str, district: str) -> Dict[str, list]:
    """
    Get the list of Labyrinth Reporters and Student Press for Sunlight CC distribution.
    """
    return {
        "labyrinth_reporters": [
            {"name": "OpenSecrets.org", "email": "tips@opensecrets.org", "focus": "Money in politics"},
            {"name": "ProPublica", "email": "tips@propublica.org", "focus": "Government accountability"},
            {"name": "The Intercept", "email": "tips@theintercept.com", "focus": "Investigative journalism"}
        ],
        "student_press": [
            {"name": "Columbia Daily Spectator", "state": "NY", "email": "tips@columbiaspectator.com"},
            {"name": "NYU Washington Square News", "state": "NY", "email": "news@nyunews.com"},
            {"name": "The Daily Californian", "state": "CA", "email": "news@dailycal.org"}
        ],
        "state_filtered": state,
        "district_filtered": district
    }


COOLING_OFF_DATABASE = {
    "former_ftc_aide": {
        "name": "[FLAGGED] Former FTC Commissioner Aide",
        "exit_date": "2025-03-15",
        "contact_date": "2025-09-01",
        "employer": "American Technology Excellence Project",
        "target_agency": "Federal Trade Commission"
    },
    "former_ntia_lead": {
        "name": "[FLAGGED] Former NTIA Policy Lead", 
        "exit_date": "2024-11-01",
        "contact_date": "2025-06-15",
        "employer": "Build American AI",
        "target_agency": "NTIA / Commerce Department"
    }
}
