# The Plainview Protocol: Truth, Kindness, & Security

## Overview
Version 2.0 - National Edition. A Streamlit web application that educates citizens on federal policy costs, tracks leader accountability, and helps voice concerns professionally. Features state-specific data with population-based cost calculations, border state multipliers, monetization, and leader scorecard tracking. Pro-American, rule of law, domestic security focus with an objective tone.

## Features
- **The National Lens**: State-specific federal cost calculator with border state multipliers (TX, AZ, CA, NM get 1.5x), population-prorated immigration costs based on $150.7B national figure
- **The 2027 Fork in the Road**: Debt-to-GDP projections, $36.5T national debt display, immunity double standard analysis
- **The Bridge Builder**: Transform emotional concerns into professional, effective communications
- **Support the Mission**: Buy Me a Coffee link, X/Twitter follow button
- **Leader Scorecard**: Interactive table of representative voting records with accountability scores (color-coded)

## Tech Stack
- Python 3.11
- Streamlit (web framework)
- Pandas (data handling)

## Project Structure
- `app.py` - Main Streamlit application with all five pages
- `.streamlit/config.toml` - Streamlit server configuration
- `pyproject.toml` - Python dependencies

## Running the App
The app runs on port 5000 via the Streamlit App workflow:
```
streamlit run app.py --server.port 5000
```

## Sidebar Controls
- State selector (all 50 states, default: New York)
- Role selector (Taxpayer, Business Owner, Concerned Citizen)
- Page navigation
- Persistent "Support Russell" coffee button

## Key Data
- Border states: Texas, Arizona, California, New Mexico (1.5x waste multiplier)
- State population ratios for prorating national costs
- Debt interest: ~18% of federal taxes
- Waste/policy gaps: ~5% base (7.5% for border states)

## Design
- Patriotic color scheme (navy blue, red, white)
- Clean, professional layout
- Sidebar navigation between five main pages
- State-aware calculations and messaging
- GitHub fork button in footer
