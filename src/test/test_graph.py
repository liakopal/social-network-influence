# src/test/test_graph.py

import pytest
from data_structures.graph import Graph

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

def test_add_edge(graph):
    assert graph.adj_list == {
        0: {1: 1, 2: 1},
        1: {0: 1, 3: 1, 4: 1},
        2: {0: 1, 5: 1, 6: 1},
        3: {1: 1, 7: 1},
        4: {1: 1, 7: 1},
        5: {2: 1, 7: 1},
        6: {2: 1, 7: 1},
        7: {3: 1, 4: 1, 5: 1, 6: 1}
    }

def test_get_neighbors(graph):
    assert graph.get_neighbors(0) == {1: 1, 2: 1}
    assert graph.get_neighbors(1) == {0: 1, 3: 1, 4: 1}
    assert graph.get_neighbors(7) == {3: 1, 4: 1, 5: 1, 6: 1}
    assert graph.get_neighbors(8) == {}

def test_getitem(graph):
    assert graph[0] == {1: 1, 2: 1}
    assert graph[1] == {0: 1, 3: 1, 4: 1}
    assert graph[7] == {3: 1, 4: 1, 5: 1, 6: 1}
    assert graph[8] == {}
