import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from api.index import app
    print("Successfully imported app")
    for route in app.routes:
        print(f"Route: {route.path} [{route.methods}]")
except Exception as e:
    print(f"Error importing app: {e}")
