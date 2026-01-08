# The Plainview Protocol: Truth, Kindness, & Security

## Overview
Version 2.0 - A national Streamlit web application that educates citizens on federal policy costs, tracks leader accountability, and helps voice concerns professionally. Features state-specific data, monetization options, and leader scorecard tracking. Pro-American, rule of law, domestic security focus with an objective tone.

## Features
- **The National Lens**: State-specific federal cost calculator with border state multipliers (TX, AZ, CA, NM get 1.5x)
- **The 2027 Fork in the Road**: Debt-to-GDP projections, $36.5T national debt display, immunity double standard analysis
- **The Bridge Builder**: Transform emotional concerns into professional, effective communications
- **Support the Protocol**: Donation links, sponsorship, and GitHub fork options for sustainability
- **Leader Scorecard**: Interactive table of representative voting records with accountability scores

## Tech Stack
- Python 3.11
- Streamlit (web framework)
- Pandas (data handling)
- Plotly (interactive charts)

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

## Design
- Patriotic color scheme (blue #002868, red #BF0A30, white)
- Clean, professional layout
- Sidebar navigation between five main pages
- State-aware calculations and messaging
