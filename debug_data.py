import pandas as pd
df = pd.read_csv("fodder_gap_analysis.csv")
print(f"Supply Sum: {df['Total_Fodder_Tons'].sum()}")
print(f"Demand Sum: {df['Total_Demand_Tons'].sum()}")
print(f"Rows: {len(df)}")
print(f"Types:\n{df.dtypes}")
