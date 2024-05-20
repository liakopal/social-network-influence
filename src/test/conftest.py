import pytest
import random
from data_structures.network import Network
from data_structures.graph import Graph

@pytest.fixture
def large_network():
    net = Network().generate_large_network()
    return net

@pytest.fixture
def large_graph():
    g = Graph().generate_large_graph()
    return g
