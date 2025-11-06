import pandas as pd
import matplotlib.pyplot as plt
import os

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_dataset.csv")

# Basic scatter plot of all nodes
plt.figure(figsize=(8, 6))
for i, row in df.iterrows():
    if row['type'] == 'd':
        plt.scatter(row['x'], row['y'], c='red', label='Depot' if i == 0 else "")
    else:
        plt.scatter(row['x'], row['y'], c='blue', label='Customer' if i == 1 else "")
    plt.text(row['x'] + 0.3, row['y'] + 0.3, str(row['id']), fontsize=8)

plt.title("Drone Delivery Network — Mao et al. Dataset")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save plot
os.makedirs("outputs", exist_ok=True)
plt.savefig("outputs/drone_network_plot.png", dpi=300)
plt.show()
print("✅ Route map saved to outputs/drone_network_plot.png")
