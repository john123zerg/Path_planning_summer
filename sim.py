import heapq
import numpy as np
import matplotlib.pyplot as plt

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

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)
        
        if current_node.position == end_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        (x, y) = current_node.position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        
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
                
            neighbor.g = current_node.g + 1
            neighbor.h = abs(neighbor.position[0] - end_node.position[0]) + abs(neighbor.position[1] - end_node.position[1])
            neighbor.f = neighbor.g + neighbor.h
            
            heapq.heappush(open_list, neighbor)
    
    return None

def create_grid(size, obstacles):
    grid = np.zeros(size)
    for obstacle in obstacles:
        grid[obstacle] = 1
    return grid

from matplotlib.animation import FuncAnimation

def plot_path(grid, path):
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=plt.cm.binary)
    point, = ax.plot([], [], 'bo')  # plot in y, x order
    
    # Mark start and end points with different colors
    ax.plot(path[0][1], path[0][0], 'go')  # start point in green
    ax.plot(path[-1][1], path[-1][0], 'ro')  # end point in red

    def update(i):
        point.set_data([path[i][1]], [path[i][0]])  # plot in y, x order
        return point,

    ani = FuncAnimation(fig, update, frames=len(path), interval=200)
    plt.show()

# Grid size
size = (10, 10)

# Define obstacles as a list of (x, y) positions
obstacles = [(3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (6, 5)]

# Start and end positions
start = (0, 0)
end = (9, 9)

grid = create_grid(size, obstacles)
path = astar(grid, start, end)

if path:
    print("Path found:", path)
    plot_path(grid, path)
else:
    print("No path found")
