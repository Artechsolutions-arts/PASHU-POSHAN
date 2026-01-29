import pandas as pd
import os
import json

datasets = [
    "district_fodder_demand.csv",
    "district_fodder_supply.csv",
    "fodder_gap_analysis.csv",
    "mandal_fodder_demand.csv"
]

base_path = "d:/pashu poshana animal husbandary/pashu poshana h/"

analysis_report = {}

for ds in datasets:
    full_path = os.path.join(base_path, ds)
    if not os.path.exists(full_path):
        continue
    
    print(f"Analyzing {ds}...")
    try:
        if ds.endswith('.csv'):
            df = pd.read_csv(full_path)
        else:
            df = pd.read_excel(full_path)
        
        # 1. Data Understanding
        info = {
            "columns": list(df.columns),
            "shape": df.shape,
            "data_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numerical_summary": df.describe(include='all').to_dict() if not df.empty else {},
            "sample_data": df.head(3).to_dict(orient='records')
        }
        
        # Detect Categorical vs Numerical
        categorical = df.select_dtypes(include=['object', 'category']).columns.tolist()
        numerical = df.select_dtypes(include=['number']).columns.tolist()
        
        info["field_classification"] = {
            "categorical": categorical,
            "numerical": numerical
        }
        
        # Frequencies for categorical
        freqs = {}
        for col in categorical:
            if df[col].nunique() < 25: 
                freqs[col] = df[col].value_counts().to_dict()
        info["categorical_distributions"] = freqs
        
        analysis_report[ds] = info
        
    except Exception as e:
        analysis_report[ds] = {"error": str(e)}

# 2. Schema Alignment Intelligence
location_keywords = ['district', 'location', 'region', 'area', 'state', 'mandal', 'mandal_name', 'district_name']
mappings = {}

for ds, info in analysis_report.items():
    if "error" in info: continue
    found = []
    for col in info["columns"]:
        if any(kw in col.lower() for kw in location_keywords):
            found.append(col)
    mappings[ds] = found

analysis_report["_cross_dataset_potential"] = {
    "location_mappings": mappings
}

with open(os.path.join(base_path, "senior_analysis_output.json"), "w") as f:
    json.dump(analysis_report, f, indent=4)
