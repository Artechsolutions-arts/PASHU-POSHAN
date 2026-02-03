import urllib.request
import json

try:
    with urllib.request.urlopen("http://localhost:8000/api/data") as response:
        data = json.loads(response.read().decode())
        print(f"Keys in data: {list(data.keys())}")
        if "forecast" in data:
            print(f"Forecast labels: {data['forecast'].get('labels')}")
            print(f"Forecast supply len: {len(data['forecast'].get('supply', []))}")
        else:
            print("Forecast key missing!")
except Exception as e:
    print(f"Error: {e}")
