import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def analyze_and_visualize_network(file_path):

    network_data = pd.read_csv(file_path, 
                              names=['from_node', 'trust_value', 'to_node', 'timestamp'])
    
    directed_graph = nx.from_pandas_edgelist(
        network_data,
        source='from_node',
        target='to_node',
        create_using=nx.DiGraph()
    )
    
    undirected_graph = directed_graph.to_undirected()
    
    undirected_degrees = dict(undirected_graph.degree())
    max_undirected_degree = max(undirected_degrees.values())
    
    in_degrees = dict(directed_graph.in_degree())
    out_degrees = dict(directed_graph.out_degree())
    max_in_degree = max(in_degrees.values())
    max_out_degree = max(out_degrees.values())
    
    avg_clustering = nx.average_clustering(undirected_graph)
    
    plt.figure(figsize=(12, 8))
    
    pos = nx.spring_layout(directed_graph, k=0.5, iterations=50)
    
    nx.draw(directed_graph, pos,
           node_color='blue',
           node_size=20,
           alpha=0.7,
           with_labels=False,
           edge_color='gray',
           arrows=True,
           width=0.2)
    
    plt.title("Bitcoin Trust Network Visualization")
    plt.savefig('network_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'max_undirected_degree': max_undirected_degree,
        'max_in_degree': max_in_degree,
        'max_out_degree': max_out_degree,
        'avg_clustering': avg_clustering
    }

def main():
    metrics = analyze_and_visualize_network('database.csv')
    
    print(f"a. Maximum undirected degree: {metrics['max_undirected_degree']}")
    print("\nb. Directed graph metrics:")
    print(f"   - Maximum in-degree: {metrics['max_in_degree']}")
    print(f"   - Maximum out-degree: {metrics['max_out_degree']}")
    print(f"\nc. Average clustering coefficient: {metrics['avg_clustering']:.4f}")
    print("\nVisualization has been saved as 'network_visualization.png'")

if __name__ == "__main__":
    main()