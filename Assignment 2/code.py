import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = "facebook_combined.txt"  # Update if needed

# Create an undirected graph
G = nx.read_edgelist(file_path, nodetype=int)

# Compute betweenness centrality (approximation for large graphs)
betweenness = nx.betweenness_centrality(G, k=4000, seed=42)

# Get the top 5 nodes with highest betweenness centrality
top_5_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]

# Print the top 5 nodes
print("Top 5 Nodes by Betweenness Centrality:")
for node, centrality in top_5_nodes:
    print(f"Node {node}: {centrality:.4f}")

# Normalize betweenness centrality for visualization
node_sizes = np.array(list(betweenness.values()))
node_sizes = 5000 * (node_sizes / max(node_sizes))  # Scale node sizes

# Create a color mapping based on centrality values
node_colors = np.array(list(betweenness.values()))

# Set up figure size
plt.figure(figsize=(12, 8))

# Use a force-directed layout
pos = nx.spring_layout(G, seed=42)

# Draw edges
nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color="black", width=0.5)

# Draw nodes with sizes and colors
sc = nx.draw_networkx_nodes(
    G, pos, node_size=node_sizes, cmap=plt.cm.viridis, 
    node_color=node_colors, alpha=0.9
)

# Add colorbar for betweenness centrality
plt.colorbar(sc, label="Betweenness Centrality")

# Remove axis for cleaner visualization
plt.axis("off")

# Title
plt.title("Graph Visualization with Betweenness Centrality")

# Show the plot
plt.show()
