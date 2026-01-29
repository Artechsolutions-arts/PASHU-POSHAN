import pandas as pd

# Standardize District Names Mapping
DISTRICT_MAPPING = {
    'SPSRNELLORE': 'NELLORE',
    'SPSNELLORE': 'NELLORE',
    'NELLORE': 'NELLORE',
    
    'ANANTHAPURAMU': 'ANANTAPUR',
    'ANANTHAPUR': 'ANANTAPUR',
    'ANATHAPURAMU': 'ANANTAPUR',
    'ANANTAPUR': 'ANANTAPUR',
    
    'YSRKADAPA': 'KADAPA',
    'KADAPA': 'KADAPA',
    'YSR': 'KADAPA',

    'ALLURISITARAMARAJU': 'ALLURI SITARAMA RAJU',
    'SRISATYASAI': 'SRI SATYASAI',
    'DRBRAMBEDKARKONASEEMA': 'DR B.R. AMBEDKAR KONASEEMA',
    'PARVATHIPURAMMANYAM': 'PARVATHIPURAM MANYAM',
    'ANAKAPALLI': 'ANAKAPALLI',
    'ANNAMAYYA': 'ANNAMAYYA',
    'BAPATLA': 'BAPATLA',
    'ELURU': 'ELURU',
    'KAKINADA': 'KAKINADA',
    'NANDYAL': 'NANDYAL',
    'NTR': 'NTR',
    'PALNADU': 'PALNADU',
    'TIRUPATI': 'TIRUPATI',
    
    'SRIKAKULAM': 'SRIKAKULAM',
    'VIZIANAGARAM': 'VIZIANAGARAM',
    'VISAKHAPATNAM': 'VISAKHAPATNAM',
    'EASTGODAVARI': 'EAST GODAVARI',
    'WESTGODAVARI': 'WEST GODAVARI',
    'GUNTUR': 'GUNTUR',
    'PRAKASAM': 'PRAKASAM',
    'KRISHNA': 'KRISHNA',
    'KURNOOL': 'KURNOOL',
    'CHITTOOR': 'CHITTOOR'
}

def normalize_name(name):
    if pd.isna(name):
        return ""
    # Base normalization: Upper, No Space, No Hyphen
    clean_name = str(name).strip().upper().replace(" ", "").replace("-", "").replace(".", "")
    
    # Map to standard name if exists (partial matching could be dangerous, exact key match first)
    return DISTRICT_MAPPING.get(clean_name, clean_name)

def calculate_gap():
    print("Loading Supply and Demand data...")
    supply_df = pd.read_csv("district_fodder_supply.csv")
    demand_df = pd.read_csv("district_fodder_demand.csv")
    
    # Normalize District names for merging
    supply_df['District_Key'] = supply_df['District'].apply(normalize_name)
    demand_df['District_Key'] = demand_df['District'].apply(normalize_name)
    
    # Merge
    merged_df = pd.merge(supply_df, demand_df, on='District_Key', suffixes=('_Supply', '_Demand'), how='outer')
    
    # Use the standardized District Name (Key) instead of potentially messy source names
    merged_df['District'] = merged_df['District_Key']
    
    # Fill NaNs with 0
    merged_df['Total_Fodder_Tons'] = merged_df['Total_Fodder_Tons'].fillna(0)
    merged_df['Total_Demand_Tons'] = merged_df['Total_Demand_Tons'].fillna(0)
    
    # Calculate Gap
    merged_df['Balance_Tons'] = merged_df['Total_Fodder_Tons'] - merged_df['Total_Demand_Tons']
    merged_df['Status'] = merged_df['Balance_Tons'].apply(lambda x: 'SURPLUS' if x > 0 else 'DEFICIT')
    merged_df['Deficit_Percentage'] = (merged_df['Balance_Tons'] / merged_df['Total_Demand_Tons']) * 100
    
    # Handle division by zero
    merged_df['Deficit_Percentage'] = merged_df['Deficit_Percentage'].fillna(0)
    
    # Select and Sort columns
    final_cols = ['District', 'Total_Fodder_Tons', 'Total_Demand_Tons', 'Balance_Tons', 'Status', 'Deficit_Percentage']
    final_df = merged_df[final_cols].sort_values(by='Balance_Tons')
    
    print("\n--- Fodder Gap Analysis (Critical Deficits) ---")
    print(final_df.head(10).to_string(index=False))
    
    print("\n--- Fodder Gap Analysis (Top Surpluses) ---")
    print(final_df.tail(5).to_string(index=False))
    
    output_csv = "fodder_gap_analysis.csv"
    final_df.to_csv(output_csv, index=False)
    print(f"\nGap Analysis saved to {output_csv}")

if __name__ == "__main__":
    calculate_gap()
