import requests

def test_url(url, method="GET", payload=None):
    print(f"Testing {method} {url}")
    try:
        if method == "POST":
            r = requests.post(url, json=payload, timeout=5)
        else:
            r = requests.get(url, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Preview: {r.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

test_url("http://localhost:8000/")
test_url("http://localhost:8000/api/data")
test_url("http://localhost:8000/api/chat", "POST", {"message": "hi"})
