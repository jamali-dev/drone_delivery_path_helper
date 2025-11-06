import pandas as pd
import matplotlib.pyplot as plt
import os
import math

# --- Load cleaned dataset ---
df = pd.read_csv("data/processed/cleaned_dataset.csv")

# --- Load No-Fly Zones from the Mao dataset ---
NFZ_PATH = os.path.join("data", "raw", "mao", "Data", "60", "C60_R12_0.25", "No-fly zones.csv")
nfz = pd.read_csv(NFZ_PATH)

print("✅ Loaded:", len(nfz), "no-fly zones")
print(nfz.head())

# --- Plot drone delivery network ---
plt.figure(figsize=(8, 6))
plt.title("Drone Delivery Network with No-Fly Zones — Mao et al.")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid(True)

# plot depot & customers
for i, row in df.iterrows():
    if row['type'] == 'd':
        plt.scatter(row['x'], row['y'], c='red', s=80, label='Depot' if i == 0 else "")
    else:
        plt.scatter(row['x'], row['y'], c='blue', s=40, label='Customer' if i == 1 else "")
    plt.text(row['x'] + 0.3, row['y'] + 0.3, str(row['id']), fontsize=8)

# --- Plot No-Fly Zones as rectangles ---
if 'x1' in nfz.columns and 'y1' in nfz.columns and 'x2' in nfz.columns and 'y2' in nfz.columns:
    for _, zone in nfz.iterrows():
        x1, y1, x2, y2 = zone['x1'], zone['y1'], zone['x2'], zone['y2']
        plt.fill([x1, x2, x2, x1], [y1, y1, y2, y2], color='gray', alpha=0.3, label='No-Fly Zone')

plt.legend()
plt.tight_layout()

os.makedirs("outputs", exist_ok=True)
plt.savefig("outputs/drone_network_nfz.png", dpi=300)
plt.show()
print("✅ Saved plot with NFZs to outputs/drone_network_nfz.png")

# --- Compute average distance from depot to all nodes ---
depot = df[df['type'] == 'd'].iloc[0]
distances = []
for _, node in df[df['type'] == 'c'].iterrows():
    d = math.sqrt((depot['x'] - node['x'])**2 + (depot['y'] - node['y'])**2)
    distances.append(d)

avg_distance = sum(distances) / len(distances)
energy_per_km = 1.5  # kJ per km (example)
total_energy = avg_distance * len(distances) * energy_per_km

print(f"📏 Average distance to customers: {avg_distance:.2f} km")
print(f"⚡ Total estimated energy used: {total_energy:.2f} kJ")
