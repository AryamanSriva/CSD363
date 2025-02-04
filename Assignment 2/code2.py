# Required Libraries
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Load the graph from the edge list
def load_graph_from_edge_list(file_path, directed=False):
    edges = []
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            src, dst = map(int, line.strip().split())
            edges.append((src, dst))
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_edges_from(edges)
    return G

# Load the Facebook dataset
file_path = "twitter_combined.txt"  # Ensure this file is in the same directory or provide the correct path
G = load_graph_from_edge_list(file_path)

# Step 2: Compute Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)

# Print the top 5 nodes by betweenness centrality
print("Top 5 nodes by Betweenness Centrality:")
top_nodes = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
for node, score in top_nodes:
    print(f"Node {node}: {score:.3f}")

# Step 3: Visualize the Graph with Betweenness Centrality
plt.figure(figsize=(15, 10))

# Use spring layout for positioning nodes
pos = nx.spring_layout(G)

# Draw nodes with size proportional to their betweenness centrality
nodes = nx.draw_networkx_nodes(
    G,
    pos,
    node_size=[v * 3000 for v in betweenness_centrality.values()],  # Scale node size
    node_color=list(betweenness_centrality.values()),  # Color nodes based on centrality
    cmap=plt.cm.viridis  # Use a colormap
)

# Draw edges
nx.draw_networkx_edges(G, pos, alpha=0.2)

# Add a colorbar to indicate centrality values
plt.colorbar(nodes, label="Betweenness Centrality")
plt.title("Graph Visualization with Betweenness Centrality")

# Remove axis for better aesthetics
plt.axis('off')

# Save the figure as an image (optional)
plt.savefig("graph_betweenness_centrality.png", dpi=300, bbox_inches='tight')

# Show the plot
plt.show()