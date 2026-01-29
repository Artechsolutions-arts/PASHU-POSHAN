import pandas as pd

# Configuration: Annual Dry Matter Requirement (Tons per head per year)
# Assumptions based on standard Indian livestock feeding standards:
# Adult Cattle: ~6kg/day -> 2.19 tons/year
# Buffalo: ~7kg/day -> 2.55 tons/year
# Sheep/Goat: ~0.8kg/day -> 0.3 tons/year
# These are rough averages averaging across age groups if detailed age data isn't used.
# Since the file has 'Cattle', 'Buffaloes', 'Sheep', 'Goat', 'Livestock Units', we can use the pre-calculated 'Livestock Units' if available and reliable, or calculate our own.

# Let's check the file columns again from the inspection:
# Columns: District, Mandal Name, Cattle, Buffaloes, Sheep, Goat, Pig, Poultry, Livestock Units...
# We will use the specific counts for better granularity if possible, or fallback to Livestock Units.

DM_REQ_TONS_PER_YEAR = {
    'Cattle': 2.2,
    'Buffaloes': 2.6,
    'Sheep': 0.3,
    'Goat': 0.3,
    'Pig': 0.4, # Minor contribution usually
    'Poultry': 0.0 # Poultry usually relies on concentrate/grains, not fodder/straw
}

# Normalization Mapping (Consistent with other scripts)
DISTRICT_MAPPING = {
    'SPSRNELLORE': 'NELLORE', 'SPSNELLORE': 'NELLORE', 'NELLORE': 'NELLORE',
    'YSRKADAPA': 'KADAPA', 'KADAPA': 'KADAPA', 'YSR': 'KADAPA',
    'ANANTHAPURAMU': 'ANANTAPUR', 'ANANTHAPUR': 'ANANTAPUR',
    'ALLURISITARAMARAJU': 'ALLURI SITARAMA RAJU', 'SRISATYASAI': 'SRI SATYASAI',
    'DRBRAMBEDKARKONASEEMA': 'DR B.R. AMBEDKAR KONASEEMA', 'PARVATHIPURAMMANYAM': 'PARVATHIPURAM MANYAM'
}

def normalize_name(name):
    if pd.isna(name): return ""
    clean = str(name).strip().upper().replace(" ", "").replace("-", "").replace(".", "")
    return DISTRICT_MAPPING.get(clean, clean)

def calculate_demand():
    file_path = "LSC_Mandal wise (1).xlsx"
    print(f"Loading {file_path}...")
    
    # Read file, header at row 1 (index 1) based on inspection
    # Row 0: Title
    # Row 1: Headers (S.No, District, Mandal Name...)
    df = pd.read_excel(file_path, header=1)
    
    # Clean column names
    df.columns = [c.strip() for c in df.columns]
    
    # Identify District column (it might be 'District (26)' or similar)
    dist_col = [c for c in df.columns if 'District' in c][0]
    # Process Mandal-wise data
    # Identifiers: District and Mandal
    mandal_results = []
    
    for _, row in df.iterrows():
        # Skip rows where Mandal Name or District is missing
        dist_name = row[dist_col]
        mandal_name = row.get('Mandal Name', 'Unknown')
        
        if pd.isna(dist_name) or pd.isna(mandal_name):
            continue
            
        total_demand = 0
        details = {}
        for animal, req_per_head in DM_REQ_TONS_PER_YEAR.items():
            if animal in row:
                count = pd.to_numeric(row[animal], errors='coerce')
                if pd.notna(count):
                    demand = count * req_per_head
                    total_demand += demand
                    details[f"{animal}_Demand"] = demand
        
        mandal_results.append({
            'District': normalize_name(dist_name),
            'Mandal': mandal_name,
            'Total_Demand_Tons': total_demand,
            **details
        })
        
    mandal_df = pd.DataFrame(mandal_results)
    mandal_df.to_csv("mandal_fodder_demand.csv", index=False)
    print(f"Mandal-level data saved to mandal_fodder_demand.csv")

    # Now group for District results (as before)
    grouped = mandal_df.groupby('District').sum(numeric_only=True).reset_index()
    
    results = []
    for index, row in grouped.iterrows():
        district = row['District']
        results.append({
            'District': district,
            'Total_Demand_Tons': row['Total_Demand_Tons'],
            **{c: row[c] for c in row.index if '_Demand' in c}
        })
        
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by='Total_Demand_Tons', ascending=False)
    
    print("\n--- Estimated Fodder Demand (Top 5 Districts) ---")
    print(results_df[['District', 'Total_Demand_Tons']].head(5).to_string(index=False))
    
    output_csv = "district_fodder_demand.csv"
    results_df.to_csv(output_csv, index=False)
    print(f"\nDetailed district results saved to {output_csv}")

if __name__ == "__main__":
    calculate_demand()
