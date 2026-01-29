import pandas as pd
import sys

output_file = "dataset_overview.txt"

with open(output_file, "w", encoding="utf-8") as f:
    def log(msg):
        print(msg)
        f.write(msg + "\n")

    files = [
        "District wise Land Utilization Data for past 10 Years 13 Dists.xlsx",
        "LSC_Mandal wise (1).xlsx",
        "Livestock_feed_format (1).xlsx"
    ]

    for file in files:
        log(f"--- Inspecting {file} ---")
        try:
            # Read first few rows without header to find the structure
            df_raw = pd.read_excel(file, header=None, nrows=10)
            log("First 5 rows (raw):")
            log(df_raw.head(5).to_string())
            
            # Attempt to guess header (simple heuristic: row with most non-nulls or specific keywords)
            # For now, just logging raw is enough for me to see.
            
            log("\n")
        except Exception as e:
            log(f"Error reading {file}: {e}\n")
