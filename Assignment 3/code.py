import networkx as nx
import numpy as np
import time
from typing import Dict
import warnings
warnings.filterwarnings('ignore')

class NetworkModels:
    def __init__(self, num_vertices: int):
        self.n = num_vertices
        # Increase sample size for better accuracy
        self.sample_size = min(1000, num_vertices)
    
    def _estimate_diameter(self, G: nx.Graph, num_samples: int = 100) -> int:
        """Estimate diameter with increased sampling."""
        if not G:
            return 0
            
        nodes = list(G.nodes())
        max_distance = 0
        
        # Increase number of samples for better accuracy
        for _ in range(num_samples):
            source, target = np.random.choice(nodes, 2, replace=False)
            try:
                distance = nx.shortest_path_length(G, source, target)
                max_distance = max(max_distance, distance)
            except nx.NetworkXNoPath:
                continue
                
        return max_distance
    
    def _compute_metrics(self, G: nx.Graph) -> Dict:
        """Compute metrics with increased sampling."""
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        
        # Use more nodes for clustering coefficient calculation
        sample_nodes = np.random.choice(
            list(G.nodes()), 
            min(self.sample_size, G.number_of_nodes()), 
            replace=False
        )
        
        return {
            'diameter': self._estimate_diameter(subgraph),
            'clustering': nx.average_clustering(G, nodes=sample_nodes),
            'time': 0
        }
    
    def generate_er_model(self) -> Dict:
        """Generate ER graph with better timing measurement."""
        start_time = time.time()
        G = nx.erdos_renyi_graph(self.n, p=0.5)
        metrics = self._compute_metrics(G)
        metrics['time'] = time.time() - start_time
        return metrics
    
    def generate_small_world(self) -> Dict:
        """Generate Small World graph with optimized parameters."""
        k = max(2, int(np.log2(self.n)))
        p = 0.1
        
        start_time = time.time()
        G = nx.watts_strogatz_graph(self.n, k, p)
        metrics = self._compute_metrics(G)
        metrics['time'] = time.time() - start_time
        return metrics
    
    def generate_kronecker(self) -> Dict:
        """Generate Kronecker graph with improved probability calculation."""
        def create_kronecker_graph(initiator: np.ndarray, k: int) -> nx.Graph:
            n = 2**k
            edges = []
            
            for i in range(n):
                for j in range(i+1, n):
                    bits_i = format(i, f'0{k}b')
                    bits_j = format(j, f'0{k}b')
                    
                    prob = 1.0
                    for bit_i, bit_j in zip(bits_i, bits_j):
                        prob *= initiator[int(bit_i)][int(bit_j)]
                    
                    if np.random.random() < prob:
                        edges.append((i, j))
            
            G = nx.Graph()
            G.add_edges_from(edges)
            return G
        
        initiator = np.array([
            [0.9, 0.5],
            [0.5, 0.3]
        ])
        
        k = int(np.log2(self.n))
        start_time = time.time()
        G = create_kronecker_graph(initiator, k)
        metrics = self._compute_metrics(G)
        metrics['time'] = time.time() - start_time
        return metrics

def print_results(num_vertices: int):
    """Print results in the specified format."""
    models = NetworkModels(num_vertices)
    
    print("+" + "-"*20 + "+" + "-"*18 + "+" + "-"*20 + "+" + "-"*20 + "+")
    print("|{:<20}|{:<18}|{:<20}|{:<20}|".format(
        "Random graph", "Diameter", "Avg. Clustering", "Time taken to"))
    print("|{:<20}|{:<18}|{:<20}|{:<20}|".format(
        "model", "", "coefficient", "construct the graph"))
    print("+" + "-"*20 + "+" + "-"*18 + "+" + "-"*20 + "+" + "-"*20 + "+")
    
    for model_name, generator in [
        ("ER Model", models.generate_er_model),
        ("Small world Model", models.generate_small_world),
        ("Kronecker Model", models.generate_kronecker)
    ]:
        metrics = generator()
        print("|{:<20}|{:<18}|{:<20.4f}|{:<20.4f}|".format(
            model_name,
            metrics['diameter'],
            metrics['clustering'],
            metrics['time']
        ))
    
    print("+" + "-"*20 + "+" + "-"*18 + "+" + "-"*20 + "+" + "-"*20 + "+")

if __name__ == "__main__":
    print_results(1000)