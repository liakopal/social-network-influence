import random
from utils import timed_test
from algorithms.dfs import DFS

@timed_test
def test_large_graph_dfs(large_graph):
    print("Testing DFS traversal on large graph...")
    start_node = random.randint(0, 999)
    traversal_order = DFS.traverse(large_graph, start_node)
    print(f"DFS traversal starting from node {start_node}: {traversal_order[:20]}")
    assert len(traversal_order) > 0
