import pandas as pd

# Step 1: Load the dataset
df = pd.read_excel("pv_events.xlsx")

df_2025 = df[df["YEAR"] == 2025].copy()

# Assign category
def assign_category(events):
    if events <= 6:
        return "Very Low"
    elif events <= 28:
        return "Low"
    elif events <= 279:
        return "Moderate"
    elif events <= 1000:
        return "High"
    else:
        return "Extreme"

df_2025["CATEGORY"] = df_2025["EVENTS"].apply(assign_category)

# Save clean dataset
df_2025.to_csv("pv_2025_categorized.csv", index=False)

# Minimal clean output
print("Done.")
print("Countries:", len(df_2025))
print("\nCategory Distribution:")
print(df_2025["CATEGORY"].value_counts())