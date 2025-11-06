import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import numpy as np

def load_data():
    """Load processed dataset and no-fly zones."""
    nodes = pd.read_csv("data/processed/cleaned_dataset.csv")
    nfz = pd.read_csv("data/raw/mao/Data/60/C60_R12_0.25/No-fly zones.csv")
    return nodes, nfz

def plot_network(nodes, nfz, out_path="outputs/final_drone_network_with_real_nfz.png"):
    """Plot depot, customers, and no-fly zones."""
    plt.figure(figsize=(8, 6))
    depot = nodes[nodes["type"] == "d"]
    customers = nodes[nodes["type"] == "c"]

    # Points
    plt.scatter(depot["x"], depot["y"], color="red", label="Depot", s=100)
    plt.scatter(customers["x"], customers["y"], color="blue", label="Customer", s=40)

    # Labels
    for _, row in nodes.iterrows():
        plt.text(row["x"] + 0.5, row["y"] + 0.5, str(row["id"]), fontsize=8)

    # No-fly zones
    for _, row in nfz.iterrows():
        circle = plt.Circle((float(row["x"]), float(row["y"])), float(row["r"]),
                            color="gray", alpha=0.3, label="No-Fly Zone")
        plt.gca().add_patch(circle)

    plt.title("Drone Delivery Network with Real No-Fly Zones — Mao et al. Dataset")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.tight_layout()

    os.makedirs("outputs", exist_ok=True)
    plt.savefig(out_path)
    plt.show()
    print(f"✅ Plot saved to {out_path}")

def save_run_summary(nodes, nfz, out_path="outputs/run_summary.txt"):
    """Generate a text summary of the run."""
    depot = nodes[nodes["type"] == "d"]
    customers = nodes[nodes["type"] == "c"]
    summary_text = [
        "Drone Delivery Path Helper — Run Summary",
        f"Nodes: {len(nodes)} (Depot: {len(depot)}, Customers: {len(customers)})",
        f"NFZ count: {len(nfz)}",
        f"Drone speed (avg): {nodes['drone_speed'].iloc[0] if 'drone_speed' in nodes.columns else 'NA'}",
        f"Vehicle speed (avg): {nodes['vehicle_speed'].iloc[0] if 'vehicle_speed' in nodes.columns else 'NA'}"
    ]

    os.makedirs("outputs", exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(summary_text))
    print(f"✅ Run summary saved to {out_path}")

def calculate_stats(nodes, out_path="outputs/stats.csv"):
    """Calculate basic network statistics (distance, counts, averages)."""
    depot = nodes[nodes["type"] == "d"].iloc[0]
    customers = nodes[nodes["type"] == "c"]

    # Compute distances from depot to each customer
    distances = []
    for _, c in customers.iterrows():
        dist = math.sqrt((c["x"] - depot["x"])**2 + (c["y"] - depot["y"])**2)
        distances.append(dist)

    avg_distance = sum(distances) / len(distances)
    max_distance = max(distances)
    min_distance = min(distances)

    stats = {
        "Total_Customers": len(customers),
        "Average_Distance": round(avg_distance, 2),
        "Max_Distance": round(max_distance, 2),
        "Min_Distance": round(min_distance, 2),
        "NFZ_Count": len(nodes["nfz_count"].unique()) if "nfz_count" in nodes.columns else "NA"
    }

    import pandas as pd
    df = pd.DataFrame([stats])
    os.makedirs("outputs", exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"✅ Stats saved to {out_path}")

def plot_path_with_avoidance(nodes, nfz, out_path="outputs/pathfinding_demo.png"):
    """Draw a sample path from depot to a customer, detouring if a no-fly zone blocks it."""
    plt.figure(figsize=(8,6))
    depot = nodes[nodes["type"]=="d"].iloc[0]
    customer = nodes[nodes["type"]=="c"].iloc[40]  # pick any customer

    # plot depot & customer
    plt.scatter(depot["x"], depot["y"], c="red", s=100, label="Depot")
    plt.scatter(customer["x"], customer["y"], c="blue", s=80, label="Customer")

    # start with a straight line
    x1, y1 = depot["x"], depot["y"]
    x2, y2 = customer["x"], customer["y"]

    # check each NFZ to see if line crosses it
    detour_points = []
    for _, row in nfz.iterrows():
        cx, cy, r = row["x"], row["y"], row["r"]

        # line-circle distance formula
        dx, dy = x2 - x1, y2 - y1
        fx, fy = x1 - cx, y1 - cy
        a = dx**2 + dy**2
        b = 2*(fx*dx + fy*dy)
        c = fx**2 + fy**2 - r**2
        discriminant = b**2 - 4*a*c

        if discriminant >= 0:
            # line touches/intersects circle → detour
            angle = np.arctan2(cy - y1, cx - x1)
            detour_x = cx + (r + 2) * np.cos(angle + np.pi/3)
            detour_y = cy + (r + 2) * np.sin(angle + np.pi/3)
            detour_points.append((detour_x, detour_y))

            plt.plot([x1, detour_x, x2], [y1, detour_y, y2], "g--", lw=2, label="Detour Path")
        else:
            # no intersection, straight path ok
            plt.plot([x1, x2], [y1, y2], "g--", lw=2, label="Direct Path")

    # draw NFZ circles
    for _, row in nfz.iterrows():
        circle = plt.Circle((row["x"], row["y"]), row["r"], color="gray", alpha=0.3)
        plt.gca().add_patch(circle)

    plt.title("Drone Pathfinding Demo — NFZ Avoidance")
    plt.xlabel("X Coordinate"); plt.ylabel("Y Coordinate")
    plt.legend(); plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    os.makedirs("outputs", exist_ok=True)
    plt.savefig(out_path)
    plt.show()
    print(f"✅ Pathfinding demo saved to {out_path}")

def main():
    nodes, nfz = load_data()
    plot_network(nodes, nfz)
    save_run_summary(nodes, nfz)
    calculate_stats(nodes)
    plot_path_with_avoidance(nodes, nfz)

if __name__ == "__main__":
    main()
