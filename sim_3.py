import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def astar(grid, start, end):
    open_list = []
    closed_list = set()
    start_node = Node(start)
    end_node = Node(end)
    
    heapq.heappush(open_list, start_node)
    path = []
    open_nodes = []
    closed_nodes = []

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)
        closed_nodes.append(current_node.position)
        
        if current_node.position == end_node.position:
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1], open_nodes, closed_nodes
        
        (x, y) = current_node.position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1),
                     (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
        
        for next_position in neighbors:
            if not (0 <= next_position[0] < grid.shape[0] and 0 <= next_position[1] < grid.shape[1]):
                continue
            if grid[next_position[0], next_position[1]] != 0:
                continue
            if next_position in closed_list:
                continue
                
            neighbor = Node(next_position, current_node)
            if neighbor in open_list:
                continue
                
            neighbor.g = current_node.g + np.linalg.norm(np.array(next_position) - np.array(current_node.position))
            neighbor.h = np.linalg.norm(np.array(neighbor.position) - np.array(end_node.position))
            neighbor.f = neighbor.g + neighbor.h
            
            heapq.heappush(open_list, neighbor)
            open_nodes.append(neighbor.position)
    
    return None, open_nodes, closed_nodes

def create_grid(size, obstacles):
    grid = np.zeros(size)
    for obstacle in obstacles:
        grid[obstacle] = 1
    return grid

def plot_path(grid, path, open_nodes, closed_nodes, obstacles):
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=plt.cm.binary, origin='lower')
    
    for obs in obstacles:
        ax.plot(obs[1], obs[0], 'ks')  # black squares for obstacles

    # Mark start and end points with different colors
    if path:
        ax.plot(path[0][1], path[0][0], 'go')  # start point in green
        ax.plot(path[-1][1], path[-1][0], 'ro')  # end point in red

    # Plot the path, open and closed nodes
    line, = ax.plot([], [], 'b-')  # blue line for path
    open_points, = ax.plot([], [], 'co')  # cyan circles for open nodes
    closed_points, = ax.plot([], [], 'mo')  # magenta circles for closed nodes
    

    def update(i):
        if i < len(closed_nodes):
            closed_points.set_data([pos[1] for pos in closed_nodes[:i]], [pos[0] for pos in closed_nodes[:i]])
        if i < len(open_nodes):
            open_points.set_data([pos[1] for pos in open_nodes[:i]], [pos[0] for pos in open_nodes[:i]])
        return open_points, closed_points

    def update_path(i):
        if path and i < len(path):
            line.set_data([pos[1] for pos in path[:i]], [pos[0] for pos in path[:i]])
        return line

    ani = FuncAnimation(fig, update, frames=max(len(open_nodes), len(closed_nodes)), interval=50)
    ani_path = FuncAnimation(fig, update_path, frames=len(path), interval=1000)

    plt.show()

import random
random.seed(0)
# Grid size
size = (10, 10)

# Number of obstacles
num_obstacles = 10

# Generate random obstacles
obstacles = [(random.randint(0, size[0]-1), random.randint(0, size[1]-1)) for _ in range(num_obstacles)]

# Start and end positions
start = (0, 0)
end = (9, 9)

grid = create_grid(size, obstacles)
path, open_nodes, closed_nodes = astar(grid, start, end)

if path:
    print("Path found:", path)
else:
    print("No path found")
plot_path(grid, path, open_nodes, closed_nodes, obstacles)
