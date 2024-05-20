import pytest
import time
import statistics
import random
from data_structures.network import Network
from data_structures.graph import Graph
from algorithms.dijkstra import Dijkstra
from algorithms.bfs import BFS
from algorithms.dfs import DFS

@pytest.fixture
def large_network():
    net = Network().generate_large_network()
    return net

@pytest.fixture
def large_graph():
    g = Graph().generate_large_graph()
    return g

def test_large_network_engagement_rate(large_network):
    print("Testing engagement rates for first 100 members...")
    start_time = time.time()
    engagement_rates = []
    followers_counts = []

    for member_id in range(1, 101):
        member = large_network.members[member_id]
        engagement_rate = member.engagement_rate()
        engagement_rates.append(engagement_rate)
        followers_counts.append(len(member.followers))

        print(f"Member {member_id} - Engagement rate: {engagement_rate:.2f} %")
        assert engagement_rate >= 0.0

    mean_engagement_rate = statistics.mean(engagement_rates)
    stddev_engagement_rate = statistics.stdev(engagement_rates)
    regression_coef, r_squared = calculate_regression(followers_counts, engagement_rates)

    end_time = time.time()
    print(f"Mean engagement rate: {mean_engagement_rate:.2f}")
    print(f"Standard deviation: {stddev_engagement_rate:.2f}")
    print(f"Regression coefficient: {regression_coef:.2f}")
    print(f"R-squared value: {r_squared:.2f}")
    print(f"Test completed in {end_time - start_time:.2f} seconds.")

def test_large_network_influence(large_network):
    print("Testing influence for 100 random pairs of members...")
    start_time = time.time()

    for _ in range(100):
        member1_id = random.randint(1, 1000)
        member2_id = random.randint(1, 1000)
        if member1_id != member2_id:
            member1 = large_network.members[member1_id]
            member2 = large_network.members[member2_id]
            like_count = random.randint(0, 9)
            member1.like(member2, like_count)
            influence = member1.influence_on(member2)
            print(f"Member {member1_id} influence on Member {member2_id}: {influence:.2f} %")
            assert influence >= 0.0

    end_time = time.time()
    print(f"Test completed in {end_time - start_time:.2f} seconds.")

def test_large_network_shortest_path(large_network):
    print("Testing shortest paths for 10 random pairs of members...")
    start_time = time.time()

    for _ in range(10):
        member1_id = random.randint(1, 1000)
        member2_id = random.randint(1, 1000)
        if member1_id != member2_id:
            member1 = large_network.members[member1_id]
            member2 = large_network.members[member2_id]
            path = member1.shortest_path_to(member2, large_network.members)
            print(f"Shortest path from Member {member1_id} to Member {member2_id}: {path}")
            if path:
                assert path[0] == member1_id
                assert path[-1] == member2_id

    end_time = time.time()
    print(f"Test completed in {end_time - start_time:.2f} seconds.")

def test_large_network_highest_engagement_path(large_network):
    print("Testing highest engagement paths for 10 random pairs of members...")
    start_time = time.time()

    for _ in range(10):
        member1_id = random.randint(1, 1000)
        member2_id = random.randint(1, 1000)
        if member1_id != member2_id:
            member1 = large_network.members[member1_id]
            member2 = large_network.members[member2_id]
            path, engagement = member1.highest_engagement_path_to(member2, large_network.members)
            print(f"Highest engagement path from Member {member1_id} to Member {member2_id}: {path} with engagement: {engagement}")
            if path:
                assert path[0] == member1_id
                assert path[-1] == member2_id

    end_time = time.time()
    print(f"Test completed in {end_time - start_time:.2f} seconds.")

def test_large_graph_bfs(large_graph):
    print("Testing BFS traversal on large graph...")
    start_node = random.randint(0, 999)
    start_time = time.time()
    traversal_order = BFS.traverse(large_graph, start_node)
    end_time = time.time()
    print(f"BFS traversal starting from node {start_node}: {traversal_order[:20]}")
    print(f"Test completed in {end_time - start_time:.2f} seconds.")
    assert len(traversal_order) > 0

def test_large_graph_dfs(large_graph):
    print("Testing DFS traversal on large graph...")
    start_node = random.randint(0, 999)
    start_time = time.time()
    traversal_order = DFS.traverse(large_graph, start_node)
    end_time = time.time()
    print(f"DFS traversal starting from node {start_node}: {traversal_order[:20]}")
    print(f"Test completed in {end_time - start_time:.2f} seconds.")
    assert len(traversal_order) > 0

def calculate_regression(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    variance_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    if variance_x == 0:
        return 0, 0
    regression_coef = covariance / variance_x
    mean_y_pred = [mean_y + regression_coef * (xi - mean_x) for xi in x]
    ss_tot = sum((yi - mean_y) ** 2 for yi in y)
    ss_res = sum((y[i] - mean_y_pred[i]) ** 2 for i in range(n))
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    return regression_coef, r_squared

if __name__ == "__main__":
    pytest.main()
