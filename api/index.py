from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import sys
import os

# Ensure local imports work in development and production
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from ai_engine import get_ai_response, get_data_path

app = FastAPI()

# --- DATA CARRIER ---
def get_dashboard_data():
    try:
        gap_df = pd.read_csv(get_data_path("fodder_gap_analysis.csv")).fillna(0)
        supply_df = pd.read_csv(get_data_path("district_fodder_supply.csv")).fillna(0)
        demand_df = pd.read_csv(get_data_path("district_fodder_demand.csv")).fillna(0)
        mandal_df = pd.read_csv(get_data_path("mandal_fodder_demand.csv")).fillna(0)
        
        return {
            "gap": gap_df.to_dict(orient='records'),
            "supply": supply_df.to_dict(orient='records'),
            "demand": demand_df.to_dict(orient='records'),
            "mandal": mandal_df.to_dict(orient='records')
        }
    except Exception as e:
        print(f"Data Error: {e}")
        return {"gap": [], "supply": [], "demand": [], "mandal": []}

class ChatRequest(BaseModel):
    message: str

@app.get("/api/data")
async def get_data_endpoint():
    return get_dashboard_data()

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        response = get_ai_response(req.message)
        return {"response": response}
    except Exception as e:
        return {"response": f"⚠️ System Error: {str(e)}"}

@app.get("/")
async def root():
    # We will serve the High-Authority UI directly here for Vercel simplicity
    # Use absolute path for index.html as well
    index_path = get_data_path("index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# For Vercel, the app instance must be named 'app'
app_instance = app 
