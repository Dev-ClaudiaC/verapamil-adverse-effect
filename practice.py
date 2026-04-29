import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# 1. GET DATA FROM FDA API
# =========================
url = "https://api.fda.gov/drug/event.json"

params = {
    "search": "patient.drug.medicinalproduct:verapamil",
    "count": "patient.reaction.reactionmeddrapt.exact",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()

# =========================
# 2. CREATE DATAFRAME (THIS IS REQUIRED BEFORE PRINTING)
# =========================
df = pd.DataFrame(data["results"])
df.columns = ["reaction", "count"]
df["count"] = pd.to_numeric(df["count"])

df = df.sort_values("count", ascending=True)

# =========================
# 3. TERMINAL REPORT (NOW df EXISTS)
# =========================

print("\n" + "="*50)
print("VERAPAMIL ADVERSE DRUG REACTION ANALYSIS")
print("="*50)

print(f"\nNumber of reactions analyzed: {len(df)}")
print(f"Total reports: {df['count'].sum()}")

print("\nTop Reactions:")
print("-"*50)

for _, row in df.sort_values("count", ascending=False).iterrows():
    print(f"{row['reaction']:<30} | {row['count']}")

# =========================
# 4. PLOT
# =========================
colors = plt.cm.viridis(np.linspace(0, 1, len(df)))

plt.figure(figsize=(10,6))
plt.bar(df["reaction"], df["count"], color=colors)

plt.xticks(rotation=45, ha="right")
plt.title("Most Reported Adverse Effects of Verapamil")
plt.xlabel("Reaction")
plt.ylabel("Number of Reports")

plt.tight_layout()
plt.show()