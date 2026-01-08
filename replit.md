# The Plainview Protocol: Truth, Kindness, & Security

## Overview
Version 3.1 - Self-Healing National Edition. A production-ready Streamlit web application with live data fetching from U.S. Treasury API, Senate feeds, and Wikipedia. Features state-specific calculations, leader scorecards, and activism tools. Pro-American, rule of law, domestic security focus.

## Features
- **The National Lens**: Live national debt from Treasury API, state debt share, immigration burden with border state multipliers (1.6x)
- **The Fork in the Road**: Plotly chart anchored to live debt data, immunity double standard table
- **The Activism Hub**: Tabbed interface (Veterans/Border/Education), kindness rewriter, X share button
- **Leader Scorecard**: Live Senate votes, Wikipedia-scraped representatives, sample accountability scores
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
- **Representatives**: Wikipedia scraping via pd.read_html

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
