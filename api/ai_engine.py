import pandas as pd
import os
import sys
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# Configuration
USE_OLLAMA = True 

def get_data_path(filename):
    # Try local first
    if os.path.exists(filename):
        return filename
    # Try parent (if running from api/ folder)
    parent_path = os.path.join("..", filename)
    if os.path.exists(parent_path):
        return parent_path
    # Try absolute path discovery
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abs_path = os.path.join(base_dir, filename)
    if os.path.exists(abs_path):
        return abs_path
    return filename

def get_governance_intelligence(df):
    """
    Heuristic-based Diagnostic Engine.
    Computes vulnerability indices and resource allocation benchmarks based on descriptive gaps.
    """
    if df is None: return None
    
    # 1. Descriptive: Metric Sufficiency
    total_s = df['Total_Fodder_Tons'].sum()
    total_d = df['Total_Demand_Tons'].sum()
    sufficiency = (total_s / total_d) if total_d > 0 else 0
    
    # 2. Heuristic Benchmarking (Prescriptive Support)
    surplus_dist = df[df['Status'] == 'SURPLUS'].sort_values('Balance_Tons', ascending=False).head(3)
    deficit_dist = df[df['Status'] == 'DEFICIT'].sort_values('Balance_Tons', ascending=True).head(3)
    
    advisory_recommendations = []
    if not deficit_dist.empty and not surplus_dist.empty:
        for idx in range(min(len(surplus_dist), len(deficit_dist))):
            s = surplus_dist.iloc[idx]
            d = deficit_dist.iloc[idx]
            amt = min(s['Balance_Tons'], abs(d['Balance_Tons'])) * 0.5 
            advisory_recommendations.append(f"Simulate transfer of ~{amt:,.0f}T from {s['District']} to {d['District']} as a stabilization measure.")

    # 3. Certainty Matrix
    data_completeness = len(df[df['Total_Fodder_Tons'] > 0]) / len(df) if len(df) > 0 else 0
    
    return {
        "sufficiency": sufficiency,
        "recommendations": advisory_recommendations,
        "vulnerability": "HIGH" if sufficiency < 0.85 else "MODERATE" if sufficiency < 1.0 else "RESILIENT",
        "certainty_score": data_completeness,
        "methodology": "Linear aggregation of census-based demand and district-level land utilization records."
    }

def get_local_response(prompt, df):
    clean_q = prompt.upper().replace("?", "").replace("!", "")
    intel = get_governance_intelligence(df)
    
    GOVERNANCE_FOOTER = "\n\n*DISCLAIMER: This output is a Decision Support Signal intended for administrative scenario-planning. All recommendations are advisory and must be validated against ground-truth field signals by jurisdictional officers.*"

    # 1. State Status with Defensive Framing
    if any(word in clean_q for word in ["STATE", "OVERVIEW", "SUMMARY", "WHOLE", "ALL"]):
        rec_str = "\n".join([f"  - {a}" for a in intel['recommendations']]) if intel else "N/A"
        return f"### [DESCRIPTIVE OBSERVATION]\nState sufficiency benchmarked at {intel['sufficiency']*100:.1f}%. Current profile indicates **{intel['vulnerability']} VULNERABILITY**.\n\n### [DIAGNOSTIC REASONING]\nDerived from aggregate fodder supply ({df['Total_Fodder_Tons'].sum():,.0f}T) vs. demand ({df['Total_Demand_Tons'].sum():,.0f}T).\n\n### [ADVISORY RECOMMENDATIONS]\n{rec_str}\n\n*Lineage: fodder_gap_analysis.csv | Certainty: {intel['certainty_score']*100:.0f}%*" + GOVERNANCE_FOOTER

    # 2. Entity Intelligence
    for _, row in df.iterrows():
        d_name = str(row['District']).upper().replace(" ", "")
        if d_name in clean_q.replace(" ", ""):
            action_bench = "Continue current supply monitoring." if row['Status'] == 'SURPLUS' else "Immediate prioritization for inter-district resource reallocation or external procurement is recommended."
            return f"### [ENTITY INTELLIGENCE: {row['District']}]\n**OBSERVATION:** {row['Status']} profile detected ({abs(row['Balance_Tons']):,.0f}T observed gap).\n**REASONING:** Observed local demand ({row['Total_Demand_Tons']:,.0f}T) exceeds recorded supply capacity.\n**ADVISORY:** {action_bench}" + GOVERNANCE_FOOTER

    return "Forage AI initialized. Please specify a District or request a 'State Summary' for evidence-based decision intelligence."

def get_ai_response(prompt):
    try:
        df = pd.read_csv(get_data_path("fodder_gap_analysis.csv"))
    except:
        df = None

    if USE_OLLAMA:
        try:
            import requests
            requests.get("http://localhost:11434", timeout=1)
            llm = ChatOllama(model="gemma3:1b", temperature=0.1, base_url="http://localhost:11434")
            
            ai_prompt = f"""
            Role: Senior AI Governance Engineer & Applied Data Scientist.
            Contextual Evidence: {df.to_string(index=False) if df is not None else "No evidence found."}
            Query: {prompt}

            Output Structural Protocol:
            1. DESCRIPTIVE OBSERVATION (Quantified facts)
            2. DIAGNOSTIC REASONING (Logic & data lineage)
            3. ADVISORY RECOMMENDATIONS (Non-authoritative scenario suggestions)
            4. CERTAINTY & ASSUMPTIONS (Transparency regarding data quality/limitations)

            Strict Constraint: Do not use overconfident predictive language. Always frame outputs as 'Advisory Decision Support'. Flag that this is NOT an autonomous directive.
            """
            return llm.invoke(ai_prompt).content
        except Exception:
            return f"⚠️ [Governance Decision Integrity Active]\n\n" + get_local_response(prompt, df)
    
    return get_local_response(prompt, df)
