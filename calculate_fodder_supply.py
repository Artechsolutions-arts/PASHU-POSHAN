import pandas as pd
import numpy as np

# Configuration: Standard Harvest Indices (Residue to Grain Ratio)
# These are estimates. Adjust based on specific regional data if available.
# Source: Standard Indian Agricultural Research (ICAR/NIANP)
CROP_RESIDUE_MULTIPLIERS = {
    'Paddy': 1.3,       # Straw
    'Wheat': 1.0,       # Straw
    'Jowar': 2.5,       # Stover
    'Bajra': 2.5,       # Stover
    'Maize': 2.0,       # Stover
    'Ragi': 1.5,        # Straw
    'Small Millets': 1.5, # Straw
    'Groundnut': 2.0,   # Haulms
    'Sugarcane': 0.2,   # Tops (approx 20% of cane weight)
    'Cotton': 0.0,      # Usually not used for fodder or limited
    'Pulses': 1.0,      # Husk/Straw (Gram, Tur, etc.)
    'Soyabean': 1.0,    # Straw
}

def calculate_supply():
    file_path = "Livestock_feed_format (1).xlsx"
    print(f"Loading {file_path}...")
    
    # Load with header at row 3 (0-indexed 3 -> row 4 in Excel) which contains Crop Names
    # and row 4 (0-indexed 4 -> row 5 in Excel) which contains Area/Production/Yield
    # Actually, looking at previous output:
    # Row 3 (index 3): S.No., Name of District, Paddy, NaN, NaN, Wheat...
    # Row 4 (index 4): NaN, NaN, Area, Production, Yield...
    
    df = pd.read_excel(file_path, header=None)
    
    # Extract crop names from Row 3
    crop_row = df.iloc[3].values
    # Extract metric names from Row 4
    metric_row = df.iloc[4].values
    
    # Forward fill crop names (handle merged cells)
    current_crop = None
    headers = []
    
    for i in range(len(crop_row)):
        crop = crop_row[i]
        metric = metric_row[i]
        
        # If we have a crop name, update current_crop
        if pd.notna(crop):
            current_crop = crop
            
        # Construct header: "Crop_Metric" or just "ColumnName"
        if i == 1:
            headers.append("District")
        elif pd.notna(metric) and current_crop:
            headers.append(f"{current_crop}_{metric}")
        else:
            headers.append(f"Col_{i}")

    # Set new headers and slice data
    df.columns = headers
    data_df = df.iloc[5:].copy() # Data starts from row 5 (index 5)
    
    # Filter for just the district rows (drop empty rows)
    data_df = data_df[data_df['District'].notna()]
    
    # --- DATA CLEANING START ---
    # 1. Remove rows where District is a Year (e.g., '2014-15') or Header ('Name of the District')
    # Valid districts don't start with numbers and aren't standard headers
    def is_valid_district(name):
        name = str(name).strip()
        if name.replace('-', '').replace(' ', '').isdigit(): # Year check
            return False
        if "District" in name or "Year" in name or "S.No" in name:
            return False
        return True
        
    data_df = data_df[data_df['District'].apply(is_valid_district)]
    
    # 2. Normalize District Names
    # Remove spaces and hyphens to merge 'West Godavari' and 'WestGodavari'
    data_df['District'] = data_df['District'].astype(str).str.strip().str.upper().str.replace(" ", "").str.replace("-", "").str.replace(".", "")
    
    # Manual consolidation of variations
    SUPPLY_MAPPING = {
        'ANATHAPURAMU': 'ANANTAPUR',
        'ANANTHAPURAMU': 'ANANTAPUR',
        'ANANTHAPUR': 'ANANTAPUR',
        'ANATHAPUR': 'ANANTAPUR',
        'YSR': 'KADAPA',
        'YSRKADAPA': 'KADAPA',
        'SPSNELLORE': 'NELLORE',
        'SPSRNELLORE': 'NELLORE'
    }
    data_df['District'] = data_df['District'].replace(SUPPLY_MAPPING)

    # 3. Handle Duplicates (Multiple years of data per district)
    # We will take the MEAN (Average) supply over the available years
    
    # First, convert all value columns to numeric, coercing errors to 0
    cols_to_numeric = [c for c in data_df.columns if c != 'District']
    for col in cols_to_numeric:
        data_df[col] = pd.to_numeric(data_df[col], errors='coerce').fillna(0)
        
    print(f"Found {len(data_df)} valid data rows. Aggregating by District...")
    
    # Group by District and take Mean
    grouped_df = data_df.groupby('District')[cols_to_numeric].mean().reset_index()
    
    print(f"Aggregated into {len(grouped_df)} unique districts.")

    # 4. Map the old 13 districts to the new 26 districts for modern analysis
    # This is an estimation by splitting the supply of the parent district among its successors.
    DISTRICT_SUCCESSORS = {
        'ANANTAPUR': ['ANANTAPUR', 'SRISATYASAI'],
        'CHITTOOR': ['CHITTOOR', 'TIRUPATI', 'ANNAMAYYA'],
        'EASTGODAVARI': ['EASTGODAVARI', 'KAKINADA', 'DRBRAMBEDKARKONASEEMA'],
        'GUNTUR': ['GUNTUR', 'PALNADU', 'BAPATLA'],
        'KRISHNA': ['KRISHNA', 'NTR'],
        'KURNOOL': ['KURNOOL', 'NANDYAL'],
        'PRAKASAM': ['PRAKASAM', 'BAPATLA'],
        'VISAKHAPATNAM': ['VISAKHAPATNAM', 'ANAKAPALLI', 'ALLURISITARAMARAJU'],
        'VIZIANAGARAM': ['VIZIANAGARAM', 'PARVATHIPURAMMANYAM'],
        'WESTGODAVARI': ['WESTGODAVARI', 'ELURU'],
        'SRIKAKULAM': ['SRIKAKULAM'],
        'KADAPA': ['KADAPA', 'ANNAMAYYA'],
        'NELLORE': ['NELLORE']
    }
    
    final_rows = []
    for _, row in grouped_df.iterrows():
        parent_dist = row['District']
        if parent_dist in DISTRICT_SUCCESSORS:
            successors = DISTRICT_SUCCESSORS[parent_dist]
            num_successors = len(successors)
            for child in successors:
                child_row = row.copy()
                child_row['District'] = child
                for col in cols_to_numeric:
                    child_row[col] = row[col] / num_successors
                final_rows.append(child_row)
        else:
            final_rows.append(row)
            
    # Combine back and group by District again (handles shared successors)
    grouped_df = pd.DataFrame(final_rows).groupby('District')[cols_to_numeric].sum().reset_index()

    
    # --- DATA CLEANING END ---
    
    # Calculate Fodder
    results = []
    
    for index, row in grouped_df.iterrows():
        district = row['District']
        total_fodder_production = 0
        details = {}
        
        for crop, multiplier in CROP_RESIDUE_MULTIPLIERS.items():
            # DATA CORRECTION:
            # The Excel file headers are [Area, Production, Yield]
            # But the data analysis shows [Area, Yield, Production]
            # Example: Area=45885, Col2=5.75, Col3=263838.
            # 45885 * 5.75 = 263838. So Col3 is Production.
            # But Col3 is labeled "Yield" in the header.
            # Therefore, we read the column labeled "{crop}_Yield" to get the actual Production.
            
            # Since we renamed columns locally in this script loop before, we need to adapt.
            # The columns in grouped_df are the same as data_df.columns
            
            prod_col = f"{crop}_Yield"
            
            # Handle variations in naming (e.g., 'Tur(Arhar)' vs 'Tur')
            # We need to find the matching column in the dataframe
            matching_cols = [c for c in grouped_df.columns if crop in c and 'Yield' in c]
            
            if matching_cols:
                col_name = matching_cols[0]
                try:
                    production_val = float(row[col_name])
                    fodder_val = production_val * multiplier
                    total_fodder_production += fodder_val
                    details[crop] = fodder_val
                except ValueError:
                    continue
        
        results.append({
            'District': district,
            'Total_Fodder_Tons': total_fodder_production,
            **details
        })
        
    results_df = pd.DataFrame(results)
    
    # Sort by total production
    results_df = results_df.sort_values(by='Total_Fodder_Tons', ascending=False)
    
    print("\n--- Estimated Fodder Supply (Top 5 Districts) ---")
    print(results_df[['District', 'Total_Fodder_Tons']].head(5).to_string(index=False))
    
    output_csv = "district_fodder_supply.csv"
    results_df.to_csv(output_csv, index=False)
    print(f"\nDetailed results saved to {output_csv}")

if __name__ == "__main__":
    calculate_supply()
