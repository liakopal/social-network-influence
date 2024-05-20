import random
from utils import timed_test
from algorithms.bfs import BFS

@timed_test
def test_large_graph_bfs(large_graph):
    print("Testing BFS traversal on large graph...")
    start_node = random.randint(0, 999)
    traversal_order = BFS.traverse(large_graph, start_node)
    print(f"BFS traversal starting from node {start_node}: {traversal_order[:20]}")
    assert len(traversal_order) > 0
