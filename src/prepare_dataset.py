import pandas as pd
import os

# Define base path (adjust if your folder name changes)
BASE_PATH = os.path.join("data", "raw", "mao", "Data", "60", "C60_R12_0.25")

# --- Load datasets ---
drones = pd.read_csv(os.path.join(BASE_PATH, "Drones.csv"))
vehicles = pd.read_csv(os.path.join(BASE_PATH, "Electric vehicles.csv"))
nfz = pd.read_csv(os.path.join(BASE_PATH, "No-fly zones.csv"))
nodes = pd.read_csv(os.path.join(BASE_PATH, "Nodes.csv"))

# --- Display basic info ---
print("✅ Loaded Files:")
for name, df in [("Drones", drones), ("Vehicles", vehicles), ("No-Fly Zones", nfz), ("Nodes", nodes)]:
    print(f"{name}: {df.shape[0]} rows, {df.shape[1]} columns")

# --- Clean and normalize columns ---
drones.columns = drones.columns.str.strip().str.lower().str.replace(" ", "_")
vehicles.columns = vehicles.columns.str.strip().str.lower().str.replace(" ", "_")
nfz.columns = nfz.columns.str.strip().str.lower().str.replace(" ", "_")
nodes.columns = nodes.columns.str.strip().str.lower().str.replace(" ", "_")

# --- Merge basic drone and node info (for path helper) ---
dataset = nodes.copy()
dataset["drone_speed"] = drones["Speed"].mean() if "Speed" in drones.columns else 15
dataset["vehicle_speed"] = vehicles["Speed"].mean() if "Speed" in vehicles.columns else 10
dataset["nfz_count"] = len(nfz)

# --- Save cleaned dataset ---
os.makedirs("data/processed", exist_ok=True)
dataset.to_csv("data/processed/cleaned_dataset.csv", index=False)

print("\n✅ Cleaned dataset saved to data/processed/cleaned_dataset.csv")
print("📊 Columns:", dataset.columns.tolist())
print(dataset.head())
