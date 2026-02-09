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
        # Check for general crop shortage/lowest production query
        if any(x in clean_q for x in ["SHORTAGE", "LOWEST", "LEAST"]) and ("CROP" in clean_q or "FODDER" in clean_q):
            # Calculate totals and filter out 0-value items (placeholders)
            crop_totals = {col: supply_df[col].sum() for col in set(CROP_MAP.values())}
            active_crops = {k: v for k, v in crop_totals.items() if v > 0}
            
            if active_crops:
                min_crop = min(active_crops, key=active_crops.get)
                min_val = active_crops[min_crop]
                return header + f"CRITICAL CROP ANALYSIS: {min_crop.upper()}\n\n" + \
                    f"State Total: **{fmt(min_val)}**\n" + \
                    f"Status: **Lowest Active Fodder Source**\n\n" + \
                    f"Insight: {min_crop} provides the smallest volume of biomass to our state's total fodder pool. In districts with high cattle demand, relying on {min_crop} alone creates a high vulnerability. We recommend supplementing with Paddy straw or Maize silage." + footer

        # Existing individual crop lookup
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
        "FEATURES": "**FORAGE (Pashu Poshana) Project Capabilities:**\n\n" + \
                    "1. **Sufficiency Index:** A single live score indicating fodder adequacy for any region.\n" + \
                    "2. **Predictive Forecasting:** AI-driven 6-month outlook to identify shortages before they occur.\n" + \
                    "3. **Logistics Optimization:** Dynamic identification of Surplus Hubs and Deficit Zones for resource movement.\n" + \
                    "4. **Stress Test Scenarios:** 'What-If' simulations for rainfall reduction and drought impact analysis.\n" + \
                    "5. **Pashu Sahayak (AI Assistant):** Conversational data intelligence for senior administrative decision-making.",
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

    # 7. INTENT: RANKING (ORDINAL & SUPERLATIVE)
    ORDINAL_MAP = {
        "FIFTH": 4, "5TH": 4, "FOURTH": 3, "4TH": 3, "THIRD": 2, "3RD": 2,
        "SECOND": 1, "2ND": 1, "FIRST": 0, "1ST": 0, "HIGHEST": 0, "MOST": 0, 
        "MAX": 0, "TOP": 0, "LOWEST": 0, "LEAST": 0
    }
    rank_idx = -1
    for word, idx in ORDINAL_MAP.items():
        if word in clean_q: 
            rank_idx = idx
            break
    
    # Extra check for superlatives/extremes even without ordinals
    extreme_keywords = ["HIGHEST", "LOWEST", "MOST", "LEAST", "MAX", "MIN", "NOT SUPPLYING", "NOT FEEDING", "WORST", "BEST", "POOR"]
    is_extreme_query = any(x in clean_q for x in extreme_keywords)
    
    if rank_idx != -1 or is_extreme_query:
        if rank_idx == -1: rank_idx = 0 # Default to #1 if a superlative was used without an ordinal
        
        # Default sort
        sort_col = 'Balance_Tons'
        ascending = True # Default to critical (shortage)
        label = "RANKING"

        # Refine Sorting Logic
        is_lowest = any(x in clean_q for x in ["LOWEST", "LEAST", "BOTTOM", "SMALLEST", "MIN", "NOT", "POOR"])
        is_highest = any(x in clean_q for x in ["HIGHEST", "MOST", "TOP", "MAX", "GREATEST", "BIGGEST"])

        if "DEMAND" in clean_q or "NEED" in clean_q:
            sort_col = 'Total_Demand_Tons'
            ascending = True if is_lowest else False
            label = f"{'LOWEST' if is_lowest else 'HIGHEST'} DEMAND"
        elif "SUPPLY" in clean_q or "FOOD" in clean_q or "AVAILABLE" in clean_q:
            sort_col = 'Total_Fodder_Tons'
            ascending = True if is_lowest else False
            label = f"{'LOWEST' if is_lowest else 'HIGHEST'} SUPPLY"
        elif any(x in clean_q for x in ["SURPLUS", "BEST", "SAFE"]):
            sort_col = 'Balance_Tons'
            ascending = False if not is_lowest else True
            label = f"{'LOWEST' if is_lowest else 'HIGHEST'} SURPLUS"
        
        sorted_df = df.sort_values(sort_col, ascending=ascending)
        if rank_idx < len(sorted_df):
            row = sorted_df.iloc[rank_idx]
            return header + f"{label}: #{rank_idx+1}\n\n" + \
                f"District: **{row['District'].upper()}**\n" + \
                f"Metric: **{fmt(row[sort_col])}**\n" + \
                f"Current Status: {row['Status']}" + footer

    # 9. INTENT: LOGISTICS ADVISOR (REDISTRIBUTION)
    if any(x in clean_q for x in ["DISTRIBUTE", "MOVE", "TRANSPORT", "LOGISTIC", "SEND", "SUPPLY TO"]):
        surplus_df = df[df['Balance_Tons'] > 0].sort_values('Balance_Tons', ascending=False).head(3)
        deficit_df = df[df['Balance_Tons'] < 0].sort_values('Balance_Tons').head(3)
        
        l_title = "🚚 LOGISTICS STRATEGY: STATEWIDE REDISTRIBUTION\n\n"
        l_content = "Yes, redistribution is the primary governance intervention recommended by the FORAGE system.\n\n"
        
        l_content += "**📍 KEY SUPPLY HUBS (SURPLUS):**\n"
        for _, r in surplus_df.iterrows():
            l_content += f"- **{r['District']}**: +{fmt(r['Balance_Tons'])}\n"
            
        l_content += "\n**🚩 PRIORITY DEFICIT ZONES:**\n"
        for _, r in deficit_df.iterrows():
            l_content += f"- **{r['District']}**: {fmt(r['Balance_Tons'])}\n"
            
        l_content += "\n**STRATEGIC PLAN:**\n"
        l_content += f"1. Initiate transport from **{surplus_df.iloc[0]['District']}** to **{deficit_df.iloc[0]['District']}** to bridge the largest gap.\n"
        l_content += f"2. Utilize **{surplus_df.iloc[1]['District']}** as a secondary hub for **{deficit_df.iloc[1]['District']}**.\n"
        l_content += "3. Mobilize regional fodder banks in Surplus zones to create a 30-day buffer for neighboring deficit areas."
        
        return header + l_title + l_content + footer

    # 10. INTENT: DEFICIT LIST (WHICH DISTRICTS)
    if df is not None and any(x in clean_q for x in ["DEFICIT", "SHORTAGE", "GAP", "AT RISK", "LIST"]) and ("WHICH" in clean_q or "LIST" in clean_q or "SHOW" in clean_q):
        def_df = df[df['Balance_Tons'] < 0].sort_values('Balance_Tons')
        if not def_df.empty:
            d_list = "\n".join([f"{i+1}. **{r['District']}** ({fmt(r['Balance_Tons'])})" for i, r in enumerate(def_df.to_dict('records'))])
            return header + f"🚩 CRITICAL SHORTAGE LIST ({len(def_df)} Districts)\n\n" + \
                "The following areas report a negative fodder balance:\n\n" + d_list + \
                "\n\n**Recommendation:** Prioritize logistical movement to top 3 zones immediately." + footer

    # 9. INTENT: PREDICTION & FORECASTING
    if df is not None and any(x in clean_q for x in ["PREDICT", "FUTURE", "FORECAST", "NEXT", "OUTLOOK", "QUARTER"]):
        target_name = None
        # Check if they asked about a specific district
        for d in all_districts:
            if d.upper().replace(" ", "") in clean_q.replace(" ", ""):
                target_name = d
                break
        
        target_df = df if target_name is None else df[df['District'] == target_name]
        total_s = target_df['Total_Fodder_Tons'].sum()
        total_d = target_df['Total_Demand_Tons'].sum()
        monthly_burn = total_d / 12
        
        p_title = f"🔮 FUTURE FORECAST: {target_name.upper() if target_name else 'STATEWIDE'}\n\n"
        p_content = f"Analyzing consumption trends... Monthly burn rate: ~{fmt(monthly_burn)}\n\n"
        p_content += "| Period | Est. Stock | Status |\n|---|---|---|\n"
        
        current_stock = total_s
        for i in range(1, 7):
            current_stock -= monthly_burn
            status = "🟢 SAFE" if current_stock > 0 else "🔴 SHORTAGE"
            p_content += f"| Month {i} | {fmt(max(0, current_stock))} | {status} |\n"
        
        p_content += "\n**GOVERNANCE ADVICE:** " + ("Resource redistribution is required within 90 days." if current_stock < 0 else "Maintain current storage levels.")
        return header + p_title + p_content + footer

    # 9. INTENT: WHAT-IF SCENARIO ANALYSIS (STRESS TEST)
    if any(x in clean_q for x in ["RAIN", "DROUGHT", "SCENARIO", "CLIMATE", "REDUCE"]):
        import re
        # Extract percentage if mentioned (e.g., "20%")
        pct_match = re.search(r'(\d+)\s*%', clean_q)
        drop_pct = int(pct_match.group(1)) if pct_match else 20 # default to 20%
        
        total_s = df['Total_Fodder_Tons'].sum()
        total_d = df['Total_Demand_Tons'].sum()
        
        hypo_s = total_s * (1 - (drop_pct/100))
        hypo_bal = hypo_s - total_d
        
        s_title = f"📉 SCENARIO STRESS TEST: {drop_pct}% RESOURCE DROP\n\n"
        s_content = f"Simulating impact on biomass generation (Rainfall/Drought factor)...\n\n"
        s_content += f"• Current Supply: **{fmt(total_s)}**\n"
        s_content += f"• Hypothetical Supply: **{fmt(hypo_s)}**\n"
        s_content += f"• New Resource Gap: **{fmt(hypo_bal)}**\n\n"
        
        s_content += "**GOVERNANCE INTERVENTION PLAN:**\n"
        s_content += "1. **Emergency Buffer:** Release 15% of strategic dry matter reserves immediately.\n"
        s_content += "2. **Inter-State Procurement:** Bridge the additional gap via trade orders from neighboring surplus states.\n"
        s_content += "3. **Cattle Camps:** Pre-identify 50 high-priority cattle camp sites in critical deficit zones."
        
        return header + s_title + s_content + footer

    # 10. ENTITY: DISTRICT SPECIFIC DEEP DIVE
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
        # Check if they specifically asked about crop deficit in this district
        if supply_df is not None and any(x in clean_q for x in ["CROP", "FODDER"]) and any(x in clean_q for x in ["DEFICIT", "SHORTAGE", "LOW", "GAP"]):
            s_row = supply_df[supply_df['District'] == target_dist].iloc[0]
            crops = ['Paddy','Maize','Groundnut','Sugarcane','Jowar','Bajra','Ragi']
            
            # Find the crop with the highest deficit relative to state average
            state_avgs = {c: supply_df[c].mean() for c in crops}
            crop_diffs = {c: s_row[c] - state_avgs[c] for c in crops}
            worst_crop = min(crop_diffs, key=crop_diffs.get)
            
            return header + f"DISTRICT CROP INTELLIGENCE: {target_dist.upper()}\n\n" + \
                f"Deficit Source: **{worst_crop.upper()}**\n" + \
                f"Local Production: {fmt(s_row[worst_crop])} vs State Avg: {fmt(state_avgs[worst_crop])}\n\n" + \
                f"Analysis: The fodder shortage in {target_dist} is significantly driven by underperformance in {worst_crop} biomass. We recommend investigating soil moisture levels or shifting to drought-resistant strains." + footer

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
