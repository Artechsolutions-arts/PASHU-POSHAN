import pandas as pd
import os

files = [
    "fodder_gap_analysis.csv",
    "district_fodder_supply.csv",
    "district_fodder_demand.csv",
    "mandal_fodder_demand.csv"
]

print("--- Data Integrity Check ---")
for f in files:
    if os.path.exists(f):
        try:
            df = pd.read_csv(f)
            print(f"[SUCCESS] {f}: Found ({len(df)} rows)")
        except Exception as e:
            print(f"[ERROR] {f}: Error reading - {e}")
    else:
        print(f"[ERROR] {f}: File NOT FOUND")

# Check normalized names logic (same as dashboard.py)
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

print("\n--- Normalization Logic Test ---")
test_names = ['SPS NELLORE', 'YSR Kadapa', 'Ananthapuramu', 'Nellore']
for tn in test_names:
    print(f"'{tn}' -> '{normalize_name(tn)}'")
