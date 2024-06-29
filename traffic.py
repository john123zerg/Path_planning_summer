import osmnx as ox
import networkx as nx
import geopandas as gpd
import random
from matplotlib import cm
from matplotlib.colors import Normalize

# Define the starting and ending locations
start_location = (30.618778910945345, -96.33762402554211)  # Langford
end_location = (29.951468003220015, -95.33175141246198)    # IAH

# Get the graph for the area around the starting location
G = ox.graph_from_point(start_location, dist=25000, network_type='drive')

# Function to add random traffic delay, including complete blockage
def add_traffic_delay(length):
    # 5% chance to completely block the road
    if random.random() < 0.05:
        delay_factor = float('inf')  # Representing a complete blockage
    else:
        delay_factor = random.uniform(1.0, 1.5)
    return length * delay_factor, delay_factor

# Add traffic delays to the edges
for u, v, data in G.edges(data=True):
    travel_time, delay_factor = add_traffic_delay(data['length'])
    data['travel_time'] = travel_time
    data['delay_factor'] = delay_factor

# Get the nearest nodes to the starting and ending locations
start_node = ox.distance.nearest_nodes(G, X=start_location[1], Y=start_location[0])
end_node = ox.distance.nearest_nodes(G, X=end_location[1], Y=end_location[0])

# Use the A* algorithm to find the shortest path based on distance
shortest_distance_route = nx.shortest_path(G, start_node, end_node, weight='length')

# Use the A* algorithm to find the shortest path based on travel time
shortest_time_route = nx.shortest_path(G, start_node, end_node, weight='travel_time')

# Convert graph to GeoDataFrames
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# Extract the route nodes as GeoDataFrames
shortest_distance_route_nodes = gdf_nodes.loc[shortest_distance_route]
shortest_time_route_nodes = gdf_nodes.loc[shortest_time_route]

# Extract the route edges as GeoDataFrames
def extract_route_edges(route):
    route_edges = []
    for u, v in zip(route[:-1], route[1:]):
        edge_data = G.get_edge_data(u, v)[0]  # Take the first edge data
        geometry = edge_data['geometry'] if 'geometry' in edge_data else None
        delay_factor = edge_data['delay_factor'] if 'delay_factor' in edge_data else 1.0
        if geometry:
            route_edges.append({'geometry': geometry, 'u': u, 'v': v, 'delay_factor': delay_factor})
    return gpd.GeoDataFrame(route_edges, crs=gdf_edges.crs)

shortest_distance_route_edges = extract_route_edges(shortest_distance_route)
shortest_time_route_edges = extract_route_edges(shortest_time_route)

# Plot the route using GeoPandas explore function
m = gdf_edges.explore(color='gray', tiles='OpenStreetMap')

# Normalize delay factor for color mapping
norm = Normalize(vmin=1.0, vmax=1.5)
cmap = cm.get_cmap('Reds')

# Plot the shortest distance route edges
shortest_distance_route_edges.explore(m=m, color='blue', legend=False)

# Plot the shortest time route edges with delay visualization
shortest_time_route_edges.explore(m=m, color='red', legend=False)

# Plot the route nodes
shortest_time_route_nodes.explore(m=m, color='red', legend=False)
shortest_distance_route_nodes.explore(m=m, color='blue', legend=False)

# Add start and end markers
start_marker = gpd.GeoDataFrame(geometry=[gdf_nodes.loc[start_node].geometry], crs=gdf_nodes.crs)
end_marker = gpd.GeoDataFrame(geometry=[gdf_nodes.loc[end_node].geometry], crs=gdf_nodes.crs)
start_marker.explore(m=m, color='green', marker_kwds={'icon': 'cloud', 'prefix': 'fa'}, legend=False)
end_marker.explore(m=m, color='red', marker_kwds={'icon': 'flag', 'prefix': 'fa'}, legend=False)

# Save the map to an HTML file
m.save('route_map_with_super_traffic_comparison.html')
