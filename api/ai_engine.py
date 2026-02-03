import pandas as pd
import os
import sys
# from langchain_ollama import ChatOllama # Moved to local import
from dotenv import load_dotenv
import re

load_dotenv()

# --- CONFIGURATION ---
USE_OLLAMA = True 

# --- GOVERNANCE METADATA & ASSUMPTIONS ---
ASSUMPTIONS = {
    "consumption": "Adult Cattle: 2.2T/yr, Buffalo: 2.6T/yr, Small Ruminants: 0.3T/yr.",
    "methodology": "Production-based residue estimation using standard Indian Harvest Indices (1.3 for Paddy, 2.0 for Maize/Groundnut).",
    "lineage": "Derived from LSC Mandal Census and Livestock Feed Production Records.",
    "disclaimer": "This is a Decision Support Signal (DSS). It does not constitute an executive order. Administrative validation of ground-truth is mandatory."
}

def get_data_path(filename):
    if os.path.exists(filename): return filename
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abs_path = os.path.join(base_dir, filename)
    return abs_path if os.path.exists(abs_path) else filename

def compute_uncertainty(df):
    """Calculates a certainty score based on data density and variance."""
    if df is None or df.empty: return 0.0
    density = (df['Total_Fodder_Tons'] > 0).mean()
    return float(density)

def get_governance_intelligence(df):
    if df is None: return None
    
    total_s = df['Total_Fodder_Tons'].sum()
    total_d = df['Total_Demand_Tons'].sum()
    sufficiency = (total_s / total_d) if total_d > 0 else 0
    
    surplus_dist = df[df['Status'] == 'SURPLUS'].sort_values('Balance_Tons', ascending=False).head(3)
    deficit_dist = df[df['Status'] == 'DEFICIT'].sort_values('Balance_Tons', ascending=True).head(3)
    
    transfers = []
    if not deficit_dist.empty and not surplus_dist.empty:
        for i in range(min(len(surplus_dist), len(deficit_dist))):
            s, d = surplus_dist.iloc[i], deficit_dist.iloc[i]
            amt = min(s['Balance_Tons'], abs(d['Balance_Tons'])) * 0.4 
            transfers.append(f"Suggest moving ~{amt:,.0f} tons from {s['District']} to {d['District']}.")

    return {
        "sufficiency_index": sufficiency,
        "recommendations": transfers,
        "vulnerability": "CRITICAL" if sufficiency < 0.75 else "ELEVATED" if sufficiency < 0.9 else "STABLE",
        "certainty": compute_uncertainty(df),
        "methodology": "Applied Residue-to-Grain Ratio (RGR) modeling against Census Data."
    }

def get_local_response(prompt, df, custom_context=None):
    """Simple and friendly fallback engine."""
    if df is None and not custom_context:
        return "I can't reach the data right now. Please check your files!"

    clean_q = prompt.upper()
    header = "HELLO! HERE IS YOUR SIMPLE REPORT\n\n"
    
    def fmt(n):
        try:
            val = float(n)
            if abs(val) >= 100000: return f"{val/100000:.2f} Lakh Tons"
            if abs(val) >= 1000: return f"{val/1000:.1f} Thousand Tons"
            return f"{val:,.0f} Tons"
        except: return str(n)

    if custom_context and any(word in clean_q for word in ["CUSTOM", "UPLOAD", "NEW", "PREDICT"]):
        return header + "NEW DATA FOUND:\nI see you uploaded some new data! My brain is currently in 'Safe Mode' so I can't do deep math on it yet, but I've saved it and it's ready for looking at."

    footer = f"\n---\n*Source: {ASSUMPTIONS['lineage']}*"
    
    # Expanded keyword list for general queries
    general_keywords = ["STATE", "OVERVIEW", "SUMMARY", "TOTAL", "STATUS", "SITUATION", "ANALYSIS", "REPORT", "FODDER", "GAP", "SUPPLY", "DEMAND", "HELP", "HELLO", "HI", "WHAT"]
    
    # Check for specific District names first (Priority)
    for _, row in df.iterrows():
        d_name = str(row['District']).upper().replace(" ", "")
        if d_name in clean_q.replace(" ", ""):
            status = row['Status']
            content = f"DISTRICT REPORT: {row['District'].upper()}\n\n"
            content += f"How is it looking? {status}\n"
            content += f"- Food they have: {fmt(row['Total_Fodder_Tons'])}\n"
            content += f"- Food they need: {fmt(row['Total_Demand_Tons'])}\n"
            content += f"- The Gap: {fmt(row['Balance_Tons'])}\n\n"
            content += f"SUGGESTION:\n" + ("They are doing well with a surplus!" if status == 'SURPLUS' else "They need a bit of help to get more food for their animals soon.")
            return header + content + footer

    # If no district is found, or if a general keyword is present (or as a default fallback), show State Summary
    # This ensures the bot ALWAYS answers with data instead of being silent.
    total_s = df['Total_Fodder_Tons'].sum() if df is not None else 0
    total_d = df['Total_Demand_Tons'].sum() if df is not None else 0
    net = total_s - total_d
    
    content = f"STATEWIDE SUMMARY:\n(I didn't hear a specific district, so here is the big picture)\n\n"
    content += f"Across Andhra Pradesh, we have about **{fmt(total_s)}** of food available.\n\n"
    content += f"THE NUMBERS:\n- Food Available: {fmt(total_s)}\n- Food Needed: {fmt(total_d)}\n- Current Balance: {fmt(net)} {'Surplus' if net > 0 else 'Shortage'}\n\n"
    content += f"QUICK TIP:\nYou can ask me about a specific district like 'Anantapur' or 'Chittoor' to see how they are doing!"
    return header + content + footer

def get_ai_response_stream(prompt, custom_context=None):
    try:
        df_gap = pd.read_csv(get_data_path("fodder_gap_analysis.csv"))
    except:
        df_gap = None

    if USE_OLLAMA:
        try:
            import requests
            requests.get("http://localhost:11434", timeout=1)
            from langchain_ollama import ChatOllama
            llm = ChatOllama(model="gemma3:1b", temperature=0.1, base_url="http://localhost:11434")
            
            context_summary = ""
            if df_gap is not None:
                # Format numbers with commas to prevent AI from seeing scientific notation
                top_data = df_gap.sort_values('Balance_Tons', ascending=False).head(5).copy()
                for col in ['Total_Fodder_Tons', 'Balance_Tons']:
                    top_data[col] = top_data[col].apply(lambda x: f"{x:,.0f}")
                
                context_summary = f"\nLATEST DATA RECORDS:\n{top_data[['District', 'Total_Fodder_Tons', 'Balance_Tons', 'Status']].to_string(index=False)}\n"
            
            if custom_context:
                context_summary += f"\nNEW USER DATA:\n{custom_context}\n"

            system_instruction = f"""
            ROLE: Senior Predictive Agriculture Advisor.
            
            OBJECTIVE: Analyze current records and PROVIDE PREDICTIONS for the next 6-12 months. 
            Tell the user what is likely to happen (e.g., 'If this trend continues, District X will face a fodder shortage by summer').
            
            STRICT RULES:
            - PREDICTIONS: You must include a section called 'FUTURE PREDICTIONS:'.
            - NO SCIENTIFIC NOTATION: Never use '1.1e+06'. Use '11 Lakh' or '1,120,000'.
            - NO HASHTAGS: Do not use '#' symbols. 
            - HEADERS: Use bold plain text like **SUMMARY:** or **PREDICTIONS:**.
            - SIMPLE ENGLISH: Explain like you are talking to a farmer.
            
            CONTEXT: {context_summary}
            """
            
            full_prompt = f"{system_instruction}\n\nUSER QUESTION: {prompt}"
            
            for chunk in llm.stream(full_prompt):
                # Strip hashtags just in case the model forgets
                text = chunk.content.replace('#', '')
                yield text
        except Exception as e:
            # yield f"(Using backup engine) " # Hiding internal details from user
            yield get_local_response(prompt, df_gap, custom_context)
    else:
        yield get_local_response(prompt, df_gap, custom_context)

def get_ai_response(prompt, custom_context=None):
    resp = ""
    for chunk in get_ai_response_stream(prompt, custom_context):
        resp += chunk
    return resp
