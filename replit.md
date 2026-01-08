# The Plainview Protocol: Truth, Kindness, & Security

## Overview
A Streamlit web application that educates citizens on federal policy costs and helps them voice concerns professionally. The app has a pro-American, rule of law, domestic security focus with an objective tone.

## Features
- **The Local Lens**: Calculate your personal share of federal costs (debt interest, waste/policy gaps) based on your annual taxes
- **The 2027 Fork in the Road**: Visualize debt-to-GDP projections comparing status quo vs accountability paths, plus immunity double standard analysis
- **The Bridge Builder**: Transform emotional concerns into professional, effective communications

## Tech Stack
- Python 3.11
- Streamlit (web framework)
- Pandas (data handling)
- Plotly (interactive charts)

## Project Structure
- `app.py` - Main Streamlit application with all three pages
- `.streamlit/config.toml` - Streamlit server configuration
- `pyproject.toml` - Python dependencies

## Running the App
The app runs on port 5000 via the Streamlit App workflow:
```
streamlit run app.py --server.port 5000
```

## Design
- Patriotic color scheme (blue #002868, red #BF0A30, white)
- Clean, professional layout
- Sidebar navigation between three main pages
