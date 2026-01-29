import pandas as pd

file_path = "Livestock_feed_format (1).xlsx"
print(f"Loading {file_path}...")

df = pd.read_excel(file_path, header=None)

# Crop row is 3, Metric row is 4, Data starts 5
crop_row = df.iloc[3].values
metric_row = df.iloc[4].values

# Find column index for Paddy Production
paddy_prod_idx = -1
current_crop = None
for i in range(len(crop_row)):
    if pd.notna(crop_row[i]):
        current_crop = crop_row[i]
    
    if current_crop == 'Paddy' and metric_row[i] == 'Production':
        paddy_prod_idx = i
        break

print(f"Paddy Production is at column index: {paddy_prod_idx}")

if paddy_prod_idx != -1:
    # Print first 10 rows of data for this column
    print("First 10 rows of Paddy Production:")
    print(df.iloc[5:15, [1, paddy_prod_idx]].to_string()) # Col 1 is District Name
else:
    print("Could not find Paddy Production column")
