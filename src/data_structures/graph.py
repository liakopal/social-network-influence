import random

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v, weight=1):
        if u not in self.adj_list:
            self.adj_list[u] = {}
        if v not in self.adj_list:
            self.adj_list[v] = {}
        self.adj_list[u][v] = weight
        self.adj_list[v][u] = weight

    def get_neighbors(self, node):
        return self.adj_list.get(node, {})

    def __getitem__(self, node):
        return self.adj_list.get(node, {})

    def generate_large_graph(self, num_nodes=1000, num_edges=10000, max_weight=10):
        for _ in range(num_edges):
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            if u != v:
                weight = random.randint(1, max_weight)
                self.add_edge(u, v, weight)
        return self
