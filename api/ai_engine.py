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
    """
    STARK NLU (Simple Tabular Analysis & Response Kernel)
    A robust heuristic engine that simulates 'training' by mapping multi-dimensional 
    intents to the available CSV data structures.
    """
    if df is None and not custom_context:
        return "I'm currently disconnected from my knowledge base. Please check if the datasets are loaded."

    clean_q = prompt.upper()
    header = "📊 PASHU SAHAYAK - DATA INSIGHT\n\n"
    footer = f"\n---\n*Insight generated from 2024 Livestock Dynamics Database*"

    # 1. BRAIN: LOAD SUPPLEMENTARY DATA (LAZY LOAD)
    try:
        supply_df = pd.read_csv(get_data_path("district_fodder_supply.csv"))
        demand_df = pd.read_csv(get_data_path("district_fodder_demand.csv"))
    except:
        supply_df, demand_df = None, None

    # 2. ENTITY LIBRARIES
    CROP_MAP = {
        "PADDY": "Paddy", "RICE": "Paddy", "STRAW": "Paddy",
        "MAIZE": "Maize", "CORN": "Maize",
        "GROUNDNUT": "Groundnut", "PEANUT": "Groundnut",
        "SUGARCANE": "Sugarcane", "SUGAR": "Sugarcane",
        "JOWAR": "Jowar", "BAJRA": "Bajra", "RAGI": "Ragi", "COTTON": "Cotton"
    }
    ANIMAL_MAP = {
        "CATTLE": "Cattle_Demand", "COW": "Cattle_Demand", "BULL": "Cattle_Demand",
        "BUFFALO": "Buffaloes_Demand", "BUFFALOE": "Buffaloes_Demand",
        "SHEEP": "Sheep_Demand", "GOAT": "Goat_Demand",
        "PIG": "Pig_Demand", "POULTRY": "Poultry_Demand", "CHICKEN": "Poultry_Demand"
    }

    # 3. HELPER: DATA FORMATTER
    def fmt(n):
        try:
            val = float(n)
            if abs(val) >= 100000: return f"{val/100000:.2f} Lakh Tons"
            if abs(val) >= 1000: return f"{val/1000:.1f} K Tons"
            return f"{val:,.0f} Tons"
        except: return str(n)

    # 4. INTENT: CROP ANALYSIS
    if supply_df is not None:
        for keyword, col in CROP_MAP.items():
            if keyword in clean_q:
                # Find top producer of this crop
                top_row = supply_df.sort_values(col, ascending=False).iloc[0]
                total_crop = supply_df[col].sum()
                return header + f"CROP REPORT: {col.upper()}\n\n" + \
                    f"State Total: **{fmt(total_crop)}**\n" + \
                    f"Top Producer: **{top_row['District']}** ({fmt(top_row[col])})\n\n" + \
                    f"Analysis: {col} is a vital fodder source. {top_row['District']} contributes significantly to the state's biomass pool." + footer

    # 5. INTENT: ANIMAL DEMAND ANALYSIS
    if demand_df is not None:
        for keyword, col in ANIMAL_MAP.items():
            if keyword in clean_q:
                # Find highest demand for this animal
                top_row = demand_df.sort_values(col, ascending=False).iloc[0]
                total_demand = demand_df[col].sum()
                animal_name = col.replace('_Demand', '')
                return header + f"LIVESTOCK INSIGHT: {animal_name.upper()}\n\n" + \
                    f"Total Feed Needed (State): **{fmt(total_demand)}**\n" + \
                    f"Highest Requirement in: **{top_row['District']}** ({fmt(top_row[col])})\n\n" + \
                    f"Management Tip: Ensuring quality feed for {animal_name} in {top_row['District']} is critical for production targets." + footer

    # 6. INTENT: COMPARISON ("Compare X and Y")
    districts_in_query = []
    all_districts = df['District'].unique()
    for d in all_districts:
        if d.upper().replace(" ", "") in clean_q.replace(" ", ""):
            districts_in_query.append(d)
    
    if len(districts_in_query) >= 2:
        d1, d2 = districts_in_query[0], districts_in_query[1]
        r1 = df[df['District'] == d1].iloc[0]
        r2 = df[df['District'] == d2].iloc[0]
        diff = r1['Balance_Tons'] - r2['Balance_Tons']
        winner = d1 if diff > 0 else d2
        return header + f"COMPARISON: {d1.upper()} vs {d2.upper()}\n\n" + \
            f"• {d1}: {fmt(r1['Balance_Tons'])} ({r1['Status']})\n" + \
            f"• {d2}: {fmt(r2['Balance_Tons'])} ({r2['Status']})\n\n" + \
            f"Gap Analysis: **{winner}** is in a better relative position by {fmt(abs(diff))}." + footer

    # 7. DASHBOARD & UI NAVIGATION GUIDE
    DASHBOARD_GUIDE = {
        "DASHBOARD": "The Pashu Poshana Dashboard is a 360° analytics tool. It has 5 views: **Overview** (Global metrics), **Supply** (Crop details), **Demand** (Animal details), **Risk** (Heatmaps), and **Predict** (AI Forecasts).",
        "FILTER": "You can use the **Select District** dropdown at the top-right to filter all charts and KPIs for a specific area.",
        "EXPORT": "To save data, use the **Export Report** button. It will download a CSV file of the current filtered data for your offline use.",
        "NAVIGATE": "Use the sidebar on the left to switch between different analytical views like Demand Dynamics or Future Predictions.",
        "PREDICTION": "The 'Future Predictions' view uses a 6-month projection model based on current consumption rates and seasonal biomass availability.",
        "COLOR": "Green (🟢) signifies a Surplus or Safe status. Red (🔴) signifies a Deficit or High Risk. Yellow/Orange signifies stress levels.",
        "PILL": "The 'Status Pills' summarize a district's condition into two simple states: SURPLUS (Safe) or DEFICIT (Action required).",
        "KPI": "The KPI cards at the top show total Supply, Demand, and the resulting Gap for your selected region.",
        "DOWNLOAD": "Look for the cloud icon or 'Export' button to download your analysis as a CSV file."
    }

    for key, help_text in DASHBOARD_GUIDE.items():
        if key in clean_q:
            return header + f"DASHBOARD GUIDE: {key}\n\n" + help_text + footer

    # 8. INTENT: RANKING (ORDINAL)
    ORDINAL_MAP = {"FIRST": 0, "1ST": 0, "SECOND": 1, "2ND": 1, "THIRD": 2, "3RD": 2, "4TH": 3, "FIFTH": 4}
    rank_idx = -1
    for word, idx in ORDINAL_MAP.items():
        if word in clean_q: rank_idx = idx; break
    
    if rank_idx != -1:
        sort_col = 'Balance_Tons'
        ascending = True # default to shortage
        label = "SHORTAGE RANKING"
        if any(x in clean_q for x in ["SURPLUS", "BEST", "TOP", "SUPPLY"]):
            ascending = False
            label = "RESOURCE RANKING"
            sort_col = 'Total_Fodder_Tons' if "SUPPLY" in clean_q else 'Balance_Tons'
        
        sorted_df = df.sort_values(sort_col, ascending=ascending)
        if rank_idx < len(sorted_df):
            row = sorted_df.iloc[rank_idx]
            return header + f"{label}: #{rank_idx+1}\n\n" + \
                f"District: **{row['District'].upper()}**\n" + \
                f"Current Status: {fmt(row[sort_col])} ({row['Status']})\n" + \
                f"Overall Need: {fmt(row['Total_Demand_Tons'])}" + footer

    # 8. ENTITY: DISTRICT SPECIFIC DEEP DIVE
    # Use a custom fuzzy match for fragmented district names
    def smart_match(q, dists):
        q_norm = q.replace(" ", "").upper()
        # Direct match check
        for d in dists:
            d_norm = d.upper().replace(" ", "")
            if d_norm in q_norm or q_norm in d_norm: return d
        # Common alias check
        aliases = {"KONASEEMA": "DR B.R. AMBEDKAR KONASEEMA", "ASR": "ALLURI SITARAMA RAJU", "YSR": "KADAPA", "VIZAG": "VISAKHAPATNAM"}
        for k, v in aliases.items():
            if k in q_norm: return v
        return None

    target_dist = smart_match(clean_q, all_districts)
    if target_dist:
        row = df[df['District'] == target_dist].iloc[0]
        # Get extra context if detail files exist
        context_str = ""
        if supply_df is not None:
            s_row = supply_df[supply_df['District'] == target_dist].iloc[0]
            top_crop = s_row[['Paddy','Maize','Groundnut','Sugarcane','Jowar','Bajra','Ragi']].idxmax()
            context_str += f"• Primary Crop: {top_crop} ({fmt(s_row[top_crop])})\n"
        if demand_df is not None:
            d_row = demand_df[demand_df['District'] == target_dist].iloc[0]
            top_animal = d_row[['Cattle_Demand','Buffaloes_Demand','Sheep_Demand','Goat_Demand']].idxmax().replace('_Demand','')
            context_str += f"• Highest Demand: {top_animal} ({fmt(d_row[d_row[['Cattle_Demand','Buffaloes_Demand','Sheep_Demand','Goat_Demand']].idxmax()])})\n"

        return header + f"EXPERT REPORT: {target_dist.upper()}\n\n" + \
            f"Status: **{row['Status']}**\n" + \
            f"Supply vs Demand: {fmt(row['Total_Fodder_Tons'])} vs {fmt(row['Total_Demand_Tons'])}\n" + \
            f"Gap Intensity: {fmt(row['Balance_Tons'])}\n\n" + \
            "**KEY DYNAMICS:**\n" + context_str + \
            f"\nRecomendation: " + ("Maintain current surplus levels through storage." if row['Status'] == 'SURPLUS' else "Immediate inter-district transport required to bridge the gap.") + footer

    # 9. DEFAULT: COMPREHENSIVE STATE SUMMARY
    total_s = df['Total_Fodder_Tons'].sum()
    total_d = df['Total_Demand_Tons'].sum()
    net = total_s - total_d
    surplus_count = len(df[df['Status']=='SURPLUS'])
    return header + "STATEWIDE SITUATIONAL AWARENESS\n\n" + \
        f"The state of Andhra Pradesh currently has **{fmt(total_s)}** of fodder against a requirement of **{fmt(total_d)}**.\n\n" + \
        f"- Current Balance: {fmt(net)} {'Surplus' if net > 0 else 'Deficit'}\n" + \
        f"- Secure Districts: {surplus_count} / {len(df)}\n\n" + \
        "**AI PROMPT TIPS:**\n" + \
        "Try asking: 'Which district grows most Paddy?', 'Compare Prakasam and Eluru', or 'Who needs the second most buffalo feed?'" + footer

    # --- 5. KNOWLEDGE BASE ---
    KNOWLEDGE_BASE = {
        "DRY MATTER": "DEFINITION:\nDry Matter (DM) is the part of fodder that remains after water is removed. It is the true measure of nutritional value because animals eat to satisfy their DM requirement (approx. 2.5% of body weight).",
        "METHODOLOGY": f"HOW WE WORK:\n{ASSUMPTIONS['methodology']}\nWe compare the biomass generated from crops against the census-based requirement of the livestock.",
        "CROPS": "KEY CROPS:\nThe primary sources of fodder in Andhra Pradesh are Paddy (Straw), Maize (Stalks), and Groundnut (Haulms). Sugarcane tops are also used in some belts.",
        "SOLUTION": "SUGGESTIONS FOR SHORTAGE:\n1. **Fodder Banks:** Create storage sites in surplus districts.\n2. **Silage:** Convert green fodder into silage for long-term storage.\n3. **Hydroponics:** Rapidly grow maize fodder in 7 days for emergencies.",
        "SILAGE": "SILAGE:\nPreserved green fodder made by fermentation. It is excellent for dairy cattle as it retains moisture and nutrients during summer months.",
        "DEFICIT": "WHAT IS A DEFICIT?\nA deficit means the local production of crop residue is LESS than what the animals legally need to eat to stay healthy. This requires importing feed."
    }

    # Check Knowledge Base
    for key, answer in KNOWLEDGE_BASE.items():
        if key in clean_q:
            return header + f"DOMAIN EXPERT REPORT: {key}\n\n{answer}\n" + footer

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
    # Load data once at the start
    try:
        df_gap = pd.read_csv(get_data_path("fodder_gap_analysis.csv"))
    except:
        df_gap = None

    # Try Ollama only if specifically enabled and available
    if USE_OLLAMA:
        try:
            import requests # Local import for safety
            # Quick check if Ollama is actually reachable
            requests.get("http://localhost:11434", timeout=0.5)
            
            from langchain_ollama import ChatOllama
            llm = ChatOllama(model="gemma3:1b", temperature=0.1, base_url="http://localhost:11434")
            
            context_summary = ""
            if df_gap is not None:
                top_data = df_gap.sort_values('Balance_Tons', ascending=False).head(5).copy()
                for col in ['Total_Fodder_Tons', 'Balance_Tons']:
                    top_data[col] = top_data[col].apply(lambda x: f"{x:,.0f}")
                context_summary = f"\nSTATEWIDE SUMMARY:\n{top_data[['District', 'Total_Fodder_Tons', 'Balance_Tons', 'Status']].to_string(index=False)}\n"
            
            # Add specific domain expertise context
            if supply_df is not None and demand_df is not None:
                top_crop = supply_df.sort_values('Paddy', ascending=False).iloc[0]['District']
                top_buffalo = demand_df.sort_values('Buffaloes_Demand', ascending=False).iloc[0]['District']
                context_summary += f"\nEXPERT KNOWLEDGE:\n- Paddy Leader: {top_crop}\n- Highest Buffalo Demand: {top_buffalo}\n"

            if custom_context:
                context_summary += f"\nNEW USER DATA:\n{custom_context}\n"

            system_instruction = f"""
            ROLE: Senior Predictive Agriculture Advisor.
            OBJECTIVE: Provide deep analysis on fodder, crops, and livestock.
            CONTEXT: {context_summary}
            STYLE: Professional, data-driven, and predictive. Use bold headers.
            """
            full_prompt = f"{system_instruction}\n\nUSER QUESTION: {prompt}"
            
            for chunk in llm.stream(full_prompt):
                yield chunk.content.replace('#', '')
            return # Success, exit generator
        except:
            pass # Fallback to local logic below

    # STABLE LOCAL FALLBACK (Always works)
    try:
        yield get_local_response(prompt, df_gap, custom_context)
    except Exception as e:
        yield f"⚠️ System Error: {str(e)}"

def get_ai_response(prompt, custom_context=None):
    resp = ""
    for chunk in get_ai_response_stream(prompt, custom_context):
        resp += chunk
    return resp
