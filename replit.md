# The Plainview Protocol: Truth, Kindness, & Security

## Overview
Version 4.6 - The Citizen Orator. A production-ready Streamlit web application with bipartisan corruption tracking across all 50 states. Features Corruption Heatmap with Shadow Penalty scoring, Course Correction Manual (recall/impeachment/grand jury guides), bipartisan Grift Hunter FOIA templates, Electoral College-weighted Referendum Prototype, and citizen lever-pulling guides. Pro-American, rule of law, domestic security focus.

## Features
- **The National Lens**: Live national debt from Treasury API, state debt share, immigration burden with border state multipliers (1.6x)
- **The 2027 Fork**: Plotly chart anchored to live debt data, reform vs. status quo projections
- **Trade & Industry**: Tariff dividend calculator, sourcing finder
- **DOGE Scrutiny Hub**: DOGE metrics ($214B+ savings), Minnesota Feeding Our Future fraud case study
- **Corruption Heatmap**: 50-state Shadow Penalty scoring (FOIA speed, no-bid %, contractor donations), bipartisan tracking
- **The Activism Hub**: Tabbed interface (Veterans/Border/Education/Business), kindness rewriter, X share button
- **Accountability Tribunal**: Live Congress data, Shadow List, Scrutiny Tactics, Referendum Prototype (Vote to Audit)
- **FOIA Cannon**: Custom requests + Bipartisan Grift Hunter (Sanctuary Grift, Corporate Subsidy Grift, Universal)
- **Lever Map**: Citizen's guide to pulling levers of power (Paper Trail, Whistleblower Hotlines, Financial Chokehold)
- **Course Correction**: State-by-state recall laws, impeachment procedures, grand jury petition guides
- **The Ecosystem**: Russell's apps, books, and music
- **Support the Mission**: Buy Me a Coffee, PayPal, GitHub fork links

## Tech Stack
- Python 3.11
- Streamlit (web framework)
- Pandas (data handling)
- Plotly (interactive charts)
- Requests (API calls)
- lxml (XML/HTML parsing)

## Project Structure
- `app.py` - Main Streamlit application with all five pages
- `sources.json` - Data source URLs (Treasury API, Senate feed, Wikipedia)
- `source_checker.py` - URL health checker script
- `system_status.json` - System health status
- `.streamlit/config.toml` - Streamlit server configuration

## Running the App
```
streamlit run app.py --server.port 5000
```

## Data Sources
- **Treasury Debt**: https://api.fiscaldata.treasury.gov (live, cached 1 hour)
- **Senate Votes**: senate.gov XML feed
- **Congress Legislators**: UnitedStates.io live JSON API (real Senators/Representatives by state)

## Sidebar Controls
- State selector (all 50 states, default: New York)
- Focus selector (All, Border, Veterans, Education)
- System status indicator
- Persistent "Support Russell" coffee button

## Key Data
- Border states: Texas, Arizona, California, New Mexico (1.6x multiplier)
- State populations for debt share calculations
- Base immigration cost: $150.7B (FAIR 2023-2024)
- Fallback debt value: $36.5T if API fails

## Design
- Patriotic color scheme (navy blue, red, white)
- Live data with caching (TTL 3600 seconds)
- Graceful fallbacks for all data sources
- System health monitoring
