# The Plainview Protocol: Truth, Kindness, & Security

## Overview
Version 8.2 - Traffic Audit & Adoption Ledger. Established January 8, 2026. A production-ready Streamlit web application with bipartisan corruption tracking across all 50 states and 3,143 counties. Features Corruption Heatmap with Shadow Penalty scoring, Foreign Influence Tracker with Affidavit Gate, Revolving Door Tracker for lobbyist cooling-off violations, Ethics Complaint Trigger for OCC/Senate submissions, Agency Collaboration Portal with 72-hour correction window, and comprehensive FOIA/FARA tools. Pro-American, rule of law, domestic security focus.

## Version 6.18 Features (Sovereign Affidavit Portal)
- **Affidavit of Integrity**: SHA-256 signature binding for Foreign Influence/FARA access
- **Revolving Door Tracker**: Lobbyist database with cooling-off violation detection
- **Ethics Complaint Trigger**: OCC/Senate Ethics formal complaint generator
- **Agency Collaboration Portal**: .gov/.mil email gate, 72-hour correction workflow
- **Legal Shield**: TERMS.md, PRIVACY.md, SAFE_HARBOR.md with footer modal
- **AI Regulation Drill-Down**: Leading the Future, Think Big PAC, Meta tracking
- **Soros Network Forensics**: $140M flow mapping from Open Society Policy Center

## Core Features
- **The National Lens**: Live national debt from Treasury API, state debt share, immigration burden with border state multipliers (1.6x)
- **The 2027 Fork**: Plotly chart anchored to live debt data, reform vs. status quo projections
- **Trade & Industry**: Tariff dividend calculator, sourcing finder
- **DOGE Scrutiny Hub**: DOGE metrics ($214B+ savings), Minnesota Feeding Our Future fraud case study
- **Corruption Heatmap**: 50-state Shadow Penalty scoring (FOIA speed, no-bid %, contractor donations), bipartisan tracking, Deep Dive triggers
- **State Deep Dive**: Detailed state-level analysis with no-bid contract tables, PAC black hole spending, Justice.gov/FBI Vault links (NY, FL, CA, TX, IL)
- **The Activism Hub**: Tabbed interface (Veterans/Border/Education/Business), kindness rewriter, X share button
- **Accountability Tribunal**: Live Congress data, Shadow List, Scrutiny Tactics, Referendum Prototype (Vote to Audit)
- **FOIA Cannon**: Custom requests + Bipartisan Grift Hunter (Sanctuary Grift, Corporate Subsidy Grift, Universal)
- **Foreign Influence Tracker**: International conduits, 501(c)(4) dark money, FARA watchlist (requires affidavit)
- **FARA Violation Reporter**: Citizen reports to DOJ National Security Division (requires affidavit)
- **Shadow Watch**: Vampire Tax calculator, Sunlight Victory tracking
- **Lever Map**: Citizen's guide to pulling levers of power (Paper Trail, Whistleblower Hotlines, Financial Chokehold)
- **Course Correction**: State-by-state recall laws, impeachment procedures, grand jury petition guides
- **Sentinel Training Ground**: 4-step FOIA guide, Practice Cannon sandbox, Code of Conduct
- **Citizen Reel**: Video uploader with privacy scrubbing
- **The Ecosystem**: Russell's apps, books, and music
- **Support the Mission**: Buy Me a Coffee, PayPal, GitHub fork links

## Tech Stack
- Python 3.11
- Streamlit (web framework)
- Pandas (data handling)
- Plotly (interactive charts)
- Requests (API calls)
- lxml (XML/HTML parsing)
- hashlib (SHA-256 signature binding)

## Project Structure
- `app.py` - Main Streamlit application with 25+ pages
- `affidavit_portal.py` - Sovereign Affidavit signing module
- `ethics_filing_logic.py` - OCC/Senate complaint generator
- `vampire_tax_calculator.py` - FARA penalty calculations
- `flare_animation_logic.py` - Sunlight Flare animations
- `sources.json` - Data source URLs (Treasury API, Senate feed, Wikipedia)
- `technical_audit.json` - Silicon & Soros Audit data
- `revolving_door_audit.json` - Lobbyist database with cooling-off tracking
- `leftist_target_list.json` - Updated PAC target list with AI regulation focus
- `foreign_influence_audit.json` - International conduits and 501(c)(4) tracking
- `grassroots_media.json` - Student press and indie creator contacts
- `county_portals.json` - 3,143 county portal data
- `test_findings_v8.json` - Zero-Day Forensic Audit results
- `CODE_OF_CONDUCT.md` - Sentinel's 5 Pillars of Evidentiary Integrity
- `TERMS.md` - Terms of Service (AS-IS warranty)
- `PRIVACY.md` - Privacy Policy (AI disclosure)
- `SAFE_HARBOR.md` - Agency Collaboration Safe Harbor
- `TUTORIAL.md` - Sentinel onboarding guide
- `.streamlit/config.toml` - Streamlit server configuration

## Running the App
```
streamlit run app.py --server.port 5000
```

## Data Sources
- **Treasury Debt**: https://api.fiscaldata.treasury.gov (live, cached 1 hour)
- **Senate Votes**: senate.gov XML feed
- **Congress Legislators**: UnitedStates.io live JSON API
- **FEC Data**: FEC.gov committee filings
- **FARA Database**: efile.fara.gov
- **Lobbying Data**: OpenSecrets.org, LDA filings

## Legal Framework
- **Code of Conduct**: 5 Pillars aligned with GAO 2024 Yellow Book (GAGAS)
- **Affidavit Gate**: 52 U.S.C. § 30121, 18 U.S.C. § 1001 basis
- **Ethics Complaints**: 18 U.S.C. § 207 cooling-off violations
- **FARA Reporting**: 22 U.S.C. § 611 et seq.
- **Safe Harbor**: 72-hour correction window for agencies

## Sidebar Controls
- State selector (all 50 states, default: New York)
- Focus selector (All, Border, Veterans, Education)
- System status indicator
- Affidavit status display
- Persistent "Support Russell" coffee button

## Key Data
- Border states: Texas, Arizona, California, New Mexico (1.6x multiplier)
- State populations for debt share calculations
- Base immigration cost: $150.7B (FAIR 2023-2024)
- Fallback debt value: $36.5T if API fails
- AI lobbying 2025: $50M total
- Revolving door rate: 53% of tech lobbyists are former government officials

## Design
- Patriotic color scheme (navy blue, red, white)
- Live data with caching (TTL 3600 seconds)
- Graceful fallbacks for all data sources
- System health monitoring
- Session-based SHA-256 signature binding
- Legal footer with Terms/Privacy/Safe Harbor links

## User Preferences
- Equal scrutiny for Red and Blue jurisdictions (bipartisan)
- Evidence-based claims only (Documentary Primacy)
- Free access (no paywalls)
- Open source (GitHub fork available)
