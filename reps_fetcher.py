import requests
import pandas as pd
import json
import os
from datetime import datetime

LEGISLATORS_URL = "https://theunitedstates.io/congress-legislators/legislators-current.json"
SENTINEL_LOGS_FILE = "sentinel_logs.json"

US_STATE_TO_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

def log_to_sentinel(error_type: str, message: str, details: dict = None):  # type: ignore
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "error_type": error_type,
        "message": message,
        "details": details or {},
        "source": "reps_fetcher.py"
    }
    
    try:
        if os.path.exists(SENTINEL_LOGS_FILE):
            with open(SENTINEL_LOGS_FILE, 'r') as f:
                logs = json.load(f)
        else:
            logs = {"errors": []}
        
        logs["errors"].append(log_entry)
        
        if len(logs["errors"]) > 1000:
            logs["errors"] = logs["errors"][-500:]
        
        with open(SENTINEL_LOGS_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        pass

def fetch_reps_by_state(state_full_name: str) -> tuple[pd.DataFrame, bool]:
    state_code = US_STATE_TO_ABBREV.get(state_full_name)
    
    if not state_code:
        return pd.DataFrame([{"Name": "Invalid State", "District": "-", "Party": "-"}]), False
    
    try:
        response = requests.get(
            LEGISLATORS_URL,
            timeout=10,
            headers={"User-Agent": "PlainviewProtocol/8.4"}
        )
        response.raise_for_status()
        data = response.json()
        
        reps = []
        for legislator in data:
            terms = legislator.get('terms', [])
            if not terms:
                continue
            
            current_term = terms[-1]
            
            if current_term.get('state') != state_code:
                continue
            
            term_type = current_term.get('type', '')
            if term_type == 'sen':
                district = "Senator"
            else:
                district_num = current_term.get('district', 'At-Large')
                district = f"District {district_num}" if district_num != 'At-Large' else "At-Large"
            
            name_data = legislator.get('name', {})
            first_name = name_data.get('first', '')
            last_name = name_data.get('last', '')
            full_name = f"{first_name} {last_name}".strip() or "Unknown"
            
            party_code = current_term.get('party', 'Unknown')
            party_map = {"Democrat": "D", "Republican": "R", "Independent": "I"}
            party = party_map.get(party_code, party_code)
            
            reps.append({
                "Name": full_name,
                "District": district,
                "Party": party
            })
        
        if reps:
            df = pd.DataFrame(reps)
            senators = df[df['District'] == 'Senator']
            house = df[df['District'] != 'Senator'].sort_values(by='District')
            df = pd.concat([senators, house], ignore_index=True)
            return df, True
        else:
            return pd.DataFrame([{"Name": f"No reps found for {state_full_name}", "District": "-", "Party": "-"}]), True
    
    except requests.exceptions.Timeout as e:
        log_to_sentinel(
            "TIMEOUT",
            f"API timeout fetching legislators for {state_full_name}",
            {"state": state_full_name, "url": LEGISLATORS_URL}
        )
        return pd.DataFrame([{"Name": "API Timeout", "District": "-", "Party": "-"}]), False
    
    except requests.exceptions.RequestException as e:
        log_to_sentinel(
            "REQUEST_ERROR",
            f"Request failed fetching legislators for {state_full_name}",
            {"state": state_full_name, "error": str(e)}
        )
        return pd.DataFrame([{"Name": "API Unavailable", "District": "-", "Party": "-"}]), False
    
    except json.JSONDecodeError as e:
        log_to_sentinel(
            "JSON_ERROR",
            f"Invalid JSON response for {state_full_name}",
            {"state": state_full_name, "error": str(e)}
        )
        return pd.DataFrame([{"Name": "Data Parse Error", "District": "-", "Party": "-"}]), False
    
    except Exception as e:
        log_to_sentinel(
            "UNKNOWN_ERROR",
            f"Unknown error fetching legislators for {state_full_name}",
            {"state": state_full_name, "error": str(e), "type": type(e).__name__}
        )
        return pd.DataFrame([{"Name": "Data Error", "District": "-", "Party": "-"}]), False

def fetch_ny_reps() -> tuple[pd.DataFrame, bool]:
    return fetch_reps_by_state("New York")

if __name__ == "__main__":
    df, success = fetch_ny_reps()
    print(f"Success: {success}")
    print(df.to_string(index=False))
