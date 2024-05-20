import random
import time
from functools import wraps
from data_structures.network import Network
from algorithms.dijkstra import Dijkstra

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

def timed_test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Total execution time for {func.__name__}: {end_time - start_time:.2f} seconds.")
        return result
    return wrapper

def generate_progressive_networks(sizes):
    networks = []
    for size in sizes:
        net = Network()
        for i in range(1, size + 1):
            net.add_member(i, f"Member_{i}")
        
        for _ in range(size * 10):
            follower = random.randint(1, size)
            followee = random.randint(1, size)
            if follower != followee:
                net.follow(follower, followee)
        
        for _ in range(size * 5):
            liker = random.randint(1, size)
            likee = random.randint(1, size)
            if liker != likee:
                net.like(liker, likee, random.randint(0, 9))
            commenter = random.randint(1, size)
            commente = random.randint(1, size)
            if commenter != commente:
                net.comment(commenter, commente, random.randint(0, 9))
        
        networks.append(net)
    return networks

def create_engagement_matrix(network):
    size = len(network.members)
    engagement_matrix = [[0] * size for _ in range(size)]
    
    for member_id, member in network.members.items():
        for followee in member.following:
            engagement_matrix[member_id - 1][followee.member_id - 1] = member.engagement_rate()
    
    return engagement_matrix

def create_shortest_path_matrix(network):
    members = network.members
    member_ids = list(members.keys())
    size = len(member_ids)
    shortest_path_matrix = [[float('inf')] * size for _ in range(size)]

    for i, start_id in enumerate(member_ids):
        for j, end_id in enumerate(member_ids):
            if start_id == end_id:
                shortest_path_matrix[i][j] = 0
            else:
                path = Dijkstra.traverse_members(members, start_id, end_id)
                if path:
                    shortest_path_matrix[i][j] = len(path) - 1

    return shortest_path_matrix


def create_binary_matrix(matrix):
    size = len(matrix)
    binary_matrix = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            binary_matrix[i][j] = 1 if matrix[i][j] != 0 and matrix[i][j] != float('inf') else 0
    
    return binary_matrix
