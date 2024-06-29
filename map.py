import osmnx as ox
import networkx as nx
import geopandas as gpd

# Define the starting and ending locations
start_location = (30.618778910945345, -96.33762402554211)  # Langford
end_location = (30.705851724745518, -96.46465632258864)    # Lake Bryan

# Get the graph for the area around the starting location
G = ox.graph_from_point(start_location, dist=25000, network_type='drive')

# Get the nearest nodes to the starting and ending locations
start_node = ox.distance.nearest_nodes(G, X=start_location[1], Y=start_location[0])
end_node = ox.distance.nearest_nodes(G, X=end_location[1], Y=end_location[0])

# Use the A* algorithm to find the shortest path
route = nx.shortest_path(G, start_node, end_node, weight='length')

# Convert graph to GeoDataFrames
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# Extract the route nodes as a GeoDataFrame
route_nodes = gdf_nodes.loc[route]

# Extract the route edges as a GeoDataFrame
route_edges = []
for u, v in zip(route[:-1], route[1:]):
    edge_data = G.get_edge_data(u, v)[0]  # Take the first edge data
    geometry = edge_data['geometry'] if 'geometry' in edge_data else None
    if geometry:
        route_edges.append({'geometry': geometry, 'u': u, 'v': v})

route_edges_gdf = gpd.GeoDataFrame(route_edges, crs=gdf_edges.crs)

# Plot the route using GeoPandas explore function
m = gdf_edges.explore(color='gray', tiles='OpenStreetMap')
route_edges_gdf.explore(m=m, color='blue', legend=False)
route_nodes.explore(m=m, color='red', legend=False)

# Add start and end markers
start_marker = gpd.GeoDataFrame(geometry=[gdf_nodes.loc[start_node].geometry], crs=gdf_nodes.crs)
end_marker = gpd.GeoDataFrame(geometry=[gdf_nodes.loc[end_node].geometry], crs=gdf_nodes.crs)
start_marker.explore(m=m, color='green', marker_kwds={'icon': 'cloud', 'prefix': 'fa'}, legend=False)
end_marker.explore(m=m, color='red', marker_kwds={'icon': 'flag', 'prefix': 'fa'}, legend=False)

# Save the map to an HTML file
m.save('route_map.html')

