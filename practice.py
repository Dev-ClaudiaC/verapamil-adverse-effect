import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# =========================
# 1. DEFINE 20-YEAR WINDOW
# =========================
end_date = datetime.today()
start_date = end_date - timedelta(days=365 * 20)

start_str = start_date.strftime("%Y%m%d")
end_str = end_date.strftime("%Y%m%d")

# =========================
# 2. FDA API REQUEST
# =========================
url = "https://api.fda.gov/drug/event.json"

params = {
    "search": (
        f"patient.drug.medicinalproduct:verapamil "
        f"AND receivedate:[{start_str} TO {end_str}]"
    ),
    "count": "patient.reaction.reactionmeddrapt.exact",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()

# Safety check
if "results" not in data:
    print("No data returned from FDA API")
    print(data)
    exit()

# =========================
# 3. CREATE DATAFRAME
# =========================
df = pd.DataFrame(data["results"])

# FDA returns 'term' + 'count'
df = df.rename(columns={
    "term": "reaction",
    "count": "count"
})

df["count"] = pd.to_numeric(df["count"])
df = df.sort_values("count", ascending=True)

# =========================
# 4. PRINT REPORT
# =========================
print("\n" + "="*60)
print("VERAPAMIL ADVERSE REACTIONS (LAST 20 YEARS)")
print("="*60)

print(f"\nTime window: {start_str} → {end_str}")
print(f"Total reaction types shown: {len(df)}")
print(f"Total reports (top 10 reactions only): {df['count'].sum()}")

print("\nTop Reported Reactions:")
print("-"*60)

for _, row in df.sort_values("count", ascending=False).iterrows():
    print(f"{row['reaction']:<35} | {row['count']}")

# =========================
# 5. VISUALIZATION
# =========================
colors = plt.cm.viridis(np.linspace(0, 1, len(df)))

plt.figure(figsize=(12, 6))
plt.barh(df["reaction"], df["count"], color=colors)

plt.title("Verapamil Adverse Reactions (Last 20 Years)")
plt.xlabel("Number of Reports")
plt.ylabel("Reaction")

plt.tight_layout()
plt.show()