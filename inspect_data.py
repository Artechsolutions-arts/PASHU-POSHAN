import pandas as pd

def inspect_file(file, header_row=0):
    print(f"--- Inspecting {file} with header={header_row} ---")
    try:
        df = pd.read_excel(file, header=header_row)
        print("Columns:", df.columns.tolist())
        print("Shape:", df.shape)
        print("First 2 rows:")
        print(df.head(2).to_string())
        print("\n")
    except Exception as e:
        print(f"Error reading {file}: {e}\n")

# Try different headers for the first file based on previous observation
inspect_file("District wise Land Utilization Data for past 10 Years 13 Dists.xlsx", header_row=2)

# Inspect others with default header first
inspect_file("LSC_Mandal wise (1).xlsx")
inspect_file("Livestock_feed_format (1).xlsx")
