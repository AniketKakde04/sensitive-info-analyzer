import pandas as pd
import json
import os
from collections import defaultdict

# File paths
TRAIN_CSV_PATH = "train.csv"
OUTPUT_JSON_PATH = "data/examples.json"

# List of sensitive field types to detect
SENSITIVE_FIELDS = [
    "phone", "email", "aadhaar", "address", "passport", "license", "firstname",
    "lastname", "person", "upi", "voter", "account", "customer", "credit_card",
    "employee", "password", "location"
]

# Load data
print("📥 Loading train.csv...")
df = pd.read_csv(TRAIN_CSV_PATH, low_memory=False)

# Group columns by base sensitive type
field_groups = defaultdict(list)

for col in df.columns:
    col_lower = col.lower()
    for keyword in SENSITIVE_FIELDS:
        if keyword in col_lower:
            field_groups[keyword].append(col)
            break

print(f"🧠 Found {len(field_groups)} unique sensitive field groups:")
for key in field_groups:
    print(f"  - {key}: {len(field_groups[key])} columns")

# For each field group, collect only ONE sentence example
examples = []

for field, cols in field_groups.items():
    found = False
    for col in cols:
        values = df[col].dropna()
        for val in values:
            val = str(val).strip()
            if val and val.lower() != "nan":
                sentence = f"My {field} is {val}"
                examples.append(sentence)
                found = True
                break
        if found:
            break  # only one example per field group

# Save output
os.makedirs("data", exist_ok=True)
with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(sorted(examples), f, indent=2)

print(f"\n✅ Final examples count: {len(examples)}")
print(f"💾 Saved to {OUTPUT_JSON_PATH}")
