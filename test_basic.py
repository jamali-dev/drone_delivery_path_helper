# test_basic.py
from src.energy import leg_energy_kJ, check_battery
from src.astar import astar

# make a small 10×10 grid (1 = free)
grid = [[1]*10 for _ in range(10)]

# block a few cells to simulate obstacles
for i in range(3,7):
    grid[i][5] = 0

# find a path around obstacle
path = astar(grid, (0,0), (9,9))
print("Path length:", len(path), "first few:", path[:5])

# test the energy model
E = leg_energy_kJ(dist_m=1000, payload_kg=2, battery_kg=1.5)
print(f"Energy used: {E:.2f} kJ")
print("Battery OK?", check_battery(E, battery_capacity_kJ=900))
