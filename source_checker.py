import json
import requests
import os

STATUS_FILE = "system_status.json"
SOURCES_FILE = "sources.json"

def check_health():
    print("🐕 Watchdog started: Checking data sources...")
    
    try:
        with open(SOURCES_FILE, "r") as f:
            sources = json.load(f)
    except FileNotFoundError:
        print("❌ Error: sources.json not found.")
        return

    status_report = {}
    all_healthy = True

    for name, url in sources.items():
        try:
            print(f"   Pinging {name}...", end=" ")
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ OK")
                status_report[name] = "OK"
            else:
                print(f"❌ FAIL ({response.status_code})")
                status_report[name] = "ERROR"
                all_healthy = False
        except Exception as e:
            print(f"❌ FAIL (Exception: {e})")
            status_report[name] = "ERROR"
            all_healthy = False

    with open(STATUS_FILE, "w") as f:
        json.dump(status_report, f)
    
    if all_healthy:
        print("🟢 All systems nominal.")
    else:
        print("⚠️ Warning: Some systems are down. App will use fallbacks.")

if __name__ == "__main__":
    check_health()
