from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
import io
import pandas as pd
import sys
import os

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
        # Check if there's custom data "cached" in a temp file or session
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
            # Save for AI context (Local file approach for persistence in this stateless-ish setup)
            df.to_csv("temp_upload.csv", index=False)
            
            # Generate a quick analysis summary for the UI
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
    # We will serve the High-Authority UI directly here for Vercel simplicity
    # Use absolute path for index.html as well
    index_path = get_data_path("index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# For Vercel, the app instance must be named 'app'
app_instance = app 
