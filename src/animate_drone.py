import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# ---- Load dataset ----
df = pd.read_csv("data/processed/cleaned_dataset.csv")

# Get depot (type == 'd') and first customer (type == 'c')
depot = df[df['type'] == 'd'].iloc[0]
customer = df[df['type'] == 'c'].iloc[0]

# No-Fly Zones (from Mao dataset)
nfz = pd.DataFrame({
    "x": [19.0, -15.5],
    "y": [10.4, -12.7],
    "r": [5, 5]
})

# ---- Compute smooth path ----
# Linearly spaced points from depot to customer
num_points = 150
x_path = np.linspace(depot['x'], customer['x'], num_points)
y_path = np.linspace(depot['y'], customer['y'], num_points)

# Add a smooth arc detour if path goes near any NFZ
def adjust_path_for_nfz(x_path, y_path, nfz):
    new_x, new_y = [], []
    for x, y in zip(x_path, y_path):
        adjust_x, adjust_y = x, y
        for _, zone in nfz.iterrows():
            dx, dy = x - zone['x'], y - zone['y']
            dist = np.sqrt(dx**2 + dy**2)
            if dist < zone['r'] + 3:
                # create a small smooth arc detour
                theta = np.arctan2(dy, dx)
                adjust_x = zone['x'] + (zone['r'] + 3) * np.cos(theta + 0.6)
                adjust_y = zone['y'] + (zone['r'] + 3) * np.sin(theta + 0.6)
        new_x.append(adjust_x)
        new_y.append(adjust_y)
    return np.array(new_x), np.array(new_y)

x_path, y_path = adjust_path_for_nfz(x_path, y_path, nfz)

# ---- Plot setup ----
fig, ax = plt.subplots(figsize=(7, 6))
ax.set_xlim(-35, 35)
ax.set_ylim(-35, 35)
ax.set_title("Drone Delivery Animation — Smart NFZ Avoidance")
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")

# Plot depot & customer
ax.scatter(depot['x'], depot['y'], color='red', s=100, label="Depot")
ax.scatter(customer['x'], customer['y'], color='blue', s=100, label="Customer")

# Plot No-Fly Zones
for _, zone in nfz.iterrows():
    circle = Circle((zone['x'], zone['y']), zone['r'], color='gray', alpha=0.4)
    ax.add_patch(circle)

# Initialize drone and path line
(drone_path,) = ax.plot([], [], "g--", linewidth=2, label="Flight Path")
drone_dot, = ax.plot([], [], "ro", markersize=10)

ax.legend(loc="upper right")

# ---- Animation logic ----
def init():
    drone_path.set_data([], [])
    drone_dot.set_data([], [])
    return drone_path, drone_dot

def animate(i):
    # Clamp frame index
    if i >= len(x_path):
        i = len(x_path) - 1  
    # making sure the data is always passed as lists
    drone_path.set_data(x_path[:i+1], y_path[:i+1])
    drone_dot.set_data([x_path[i]], [y_path[i]])  # wrap in lists (sequence)

    return drone_path, drone_dot


ani = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=len(x_path),
    interval=60,
    blit=True,
)

# ---- Save animation ----
ani.save("data/processed/drone_animation.gif", writer="pillow", fps=30)
print("✅ Smart animation saved to data/processed/drone_animation.gif")

plt.show()
