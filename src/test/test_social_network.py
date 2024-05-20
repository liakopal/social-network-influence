import pytest
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra
from data_structures.graph import Graph
from data_structures.network import Network

@pytest.fixture
def graph():
    g = Graph()
    edges = [
        (0, 1, 1), (0, 2, 1), (1, 3, 1), (1, 4, 1),
        (2, 5, 1), (2, 6, 1), (3, 7, 1), (4, 7, 1),
        (5, 7, 1), (6, 7, 1)
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g

@pytest.fixture
def network():
    net = Network()
    members = [("Alice", 1), ("Bob", 2), ("Charlie", 3), ("David", 4), ("Eve", 5), ("Frank", 6)]
    for name, member_id in members:
        net.add_member(member_id, name)
    net.follow(1, 2)
    net.follow(2, 3)
    net.follow(3, 4)
    net.follow(4, 5)
    net.follow(5, 6)
    return net

def test_bfs(graph):
    result = BFS.traverse(graph, 0)
    print("BFS traversal result:", result)
    assert result == [0, 1, 2, 3, 4, 5, 6, 7]

def test_dfs(graph):
    result = DFS.traverse(graph, 0)
    print("DFS traversal result:", result)
    valid_dfs_orders = [
        [0, 1, 3, 7, 4, 2, 5, 6],  # one possible valid order
        [0, 1, 3, 4, 7, 2, 5, 6],  # another possible valid order
        [0, 2, 5, 7, 6, 1, 3, 4],  # another possible valid order
        [0, 2, 6, 7, 5, 1, 3, 4],  # another possible valid order
        [0, 2, 6, 7, 5, 4, 1, 3],  # the current DFS implementation order
    ]
    assert result in valid_dfs_orders

def test_dijkstra(graph):
    expected_distances = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 3}
    result = Dijkstra.traverse_graph(graph, 0)
    print("Dijkstra traversal result:", result)
    assert result == expected_distances

def test_social_dijkstra(network):
    member1 = network.get_member(1)
    member6 = network.get_member(6)
    path = Dijkstra.traverse_members(network.members, member1.member_id, member6.member_id)
    print(f"Shortest path from {member1.name} (ID: {member1.member_id}) to {member6.name} (ID: {member6.member_id}): {' -> '.join(map(str, path))}")
    assert path == [1, 2, 3, 4, 5, 6]
