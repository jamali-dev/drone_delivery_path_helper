# src/astar.py
import heapq, math

def heuristic(a, b):
    # Euclidean distance (straight-line)
    return math.hypot(a[0]-b[0], a[1]-b[1])

def astar(grid, start, goal):
    """
    Classic A* path-finding on a 2D grid.
    grid: 2D list (1 = free, 0 = obstacle)
    start, goal: (x, y) tuples
    returns list of nodes [(x,y), ...] if found
    """
    openh = [(0+heuristic(start,goal), 0, start, None)]
    came, g = {}, {start: 0}
    while openh:
        f, gc, node, parent = heapq.heappop(openh)
        if node in came:
            continue
        came[node] = parent
        if node == goal:
            break
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nxt = (node[0]+dx, node[1]+dy)
            if nxt[0]<0 or nxt[1]<0 or nxt[0]>=len(grid) or nxt[1]>=len(grid[0]):
                continue
            if grid[nxt[0]][nxt[1]] == 0:
                continue
            step = math.hypot(dx, dy)
            newg = gc + step
            if nxt not in g or newg < g[nxt]:
                g[nxt] = newg
                heapq.heappush(openh, (newg+heuristic(nxt,goal), newg, nxt, node))
    if goal not in came:
        return None
    # reconstruct path
    path, cur = [], goal
    while cur:
        path.append(cur)
        cur = came[cur]
    return path[::-1]
