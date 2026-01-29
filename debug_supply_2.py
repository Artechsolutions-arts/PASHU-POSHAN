import pandas as pd

file_path = "Livestock_feed_format (1).xlsx"
df = pd.read_excel(file_path, header=None)

# Crop row is 3, Metric row is 4
crop_row = df.iloc[3].values
metric_row = df.iloc[4].values

# Find indices
paddy_area_idx = -1
paddy_prod_idx = -1
paddy_yield_idx = -1

current_crop = None
for i in range(len(crop_row)):
    if pd.notna(crop_row[i]):
        current_crop = crop_row[i]
    
    if current_crop == 'Paddy':
        if metric_row[i] == 'Area':
            paddy_area_idx = i
        elif metric_row[i] == 'Production':
            paddy_prod_idx = i
        elif metric_row[i] == 'Yield':
            paddy_yield_idx = i

print(f"Paddy Indices - Area: {paddy_area_idx}, Prod: {paddy_prod_idx}, Yield: {paddy_yield_idx}")

print("First 10 rows of Paddy Data (Area, Prod, Yield):")
print(df.iloc[5:15, [1, paddy_area_idx, paddy_prod_idx, paddy_yield_idx]].to_string())
