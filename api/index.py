from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
import io
import pandas as pd
import sys
import os
import numpy as np

# Ensure local imports work in development and production
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from ai_engine import get_ai_response, get_ai_response_stream, get_data_path

app = FastAPI()

# --- DATA CARRIER ---
def get_dashboard_data():
    try:
        gap_df = pd.read_csv(get_data_path("fodder_gap_analysis.csv")).fillna(0)
        supply_df = pd.read_csv(get_data_path("district_fodder_supply.csv")).fillna(0)
        demand_df = pd.read_csv(get_data_path("district_fodder_demand.csv")).fillna(0)
        mandal_df = pd.read_csv(get_data_path("mandal_fodder_demand.csv")).fillna(0)
        
        # Normalize District names to handle inconsistencies (spaces, case)
        for df in [gap_df, supply_df, demand_df, mandal_df]:
            if 'District' in df.columns:
                df['District'] = df['District'].astype(str).str.upper().str.replace(' ', '', regex=False)
        
        # Standardize specific long names if needed (optional but good for consistency)
        # e.g., 'DRB.R.AMBEDKARKONASEEMA' vs 'DRBRAMBEDKARKONASEEMA'
        for df in [gap_df, supply_df, demand_df, mandal_df]:
            if 'District' in df.columns:
                df['District'] = df['District'].str.replace('.', '', regex=False)
        
        # Simple Forecast Logic
        total_s = gap_df['Total_Fodder_Tons'].sum()
        total_d = gap_df['Total_Demand_Tons'].sum()
        
        months = ["Current", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"]
        forecast_supply = [total_s]
        forecast_demand = [total_d]
        
        # Assume slight supply drop (seasonal) and demand increase
        for i in range(1, 6):
            forecast_supply.append(forecast_supply[-1] * (0.98 + np.random.uniform(-0.02, 0.01)))
            forecast_demand.append(forecast_demand[-1] * (1.01 + np.random.uniform(0, 0.005)))

        return {
            "gap": gap_df.to_dict(orient='records'),
            "supply": supply_df.to_dict(orient='records'),
            "demand": demand_df.to_dict(orient='records'),
            "mandal": mandal_df.to_dict(orient='records'),
            "forecast": {
                "labels": months,
                "supply": [round(x) for x in forecast_supply],
                "demand": [round(x) for x in forecast_demand]
            }
        }
    except Exception as e:
        print(f"Data Error: {e}")
        return {"gap": [], "supply": [], "demand": [], "mandal": [], "forecast": {}}

class ChatRequest(BaseModel):
    message: str

@app.get("/api/data")
async def get_data_endpoint():
    return get_dashboard_data()

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        custom_context = None
        if os.path.exists("temp_upload.csv"):
            try:
                df_temp = pd.read_csv("temp_upload.csv")
                custom_context = f"CUSTOM UPLOADED DATASET:\n{df_temp.head(20).to_string(index=False)}"
            except: pass

        return StreamingResponse(get_ai_response_stream(req.message, custom_context), media_type="text/plain")
    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"⚠️ System Error: {str(e)}"})

@app.post("/api/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = None
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        
        if df is not None:
            df.to_csv("temp_upload.csv", index=False)
            summary = {
                "rows": len(df),
                "cols": list(df.columns),
                "stats": df.describe().to_dict() if not df.select_dtypes(include='number').empty else "No numeric stats"
            }
            return JSONResponse(content={"message": "File uploaded successfully", "summary": summary})
        return JSONResponse(status_code=400, content={"message": "Invalid file format"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Upload error: {str(e)}"})

@app.get("/")
async def root():
    index_path = get_data_path("index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

app_instance = app 
