import json
import requests

def check_sources():
    with open('sources.json', 'r') as f:
        sources = json.load(f)
    
    status = {}
    
    for name, url in sources.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                status[name] = "OK"
            else:
                status[name] = "ERROR"
                print(f"WARNING: {name} returned status {response.status_code}")
        except Exception as e:
            status[name] = "ERROR"
            print(f"WARNING: {name} failed - {str(e)}")
    
    with open('system_status.json', 'w') as f:
        json.dump(status, f, indent=2)
    
    print("System status updated:", status)
    return status

if __name__ == "__main__":
    check_sources()
