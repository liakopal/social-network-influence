import pytest
from collections import defaultdict
from faker import Faker
from data_structures.network import Network
from data_structures.member import Member
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra

fake = Faker()

@pytest.fixture
def small_social_network():
    network = Network()
    names = ["Larry", "Pamela", "Michael", "Kevin", "Mary"]
    for i, name in enumerate(names, start=1):
        network.add_member(i, name)

    network.follow(1, 2)
    network.follow(2, 3)
    network.follow(3, 4)
    network.follow(4, 5)
    network.follow(5, 1)

    network.like(1, 2, 5)
    network.like(2, 3, 3)
    network.like(3, 4, 1)
    network.like(4, 5, 4)
    network.like(5, 1, 2)

    network.comment(1, 3, 2)
    network.comment(2, 4, 3)
    network.comment(3, 5, 1)
    network.comment(4, 1, 4)
    network.comment(5, 2, 2)

    return network

def test_engagement_rate(small_social_network):
    print("Calculating engagement rates...")
    for member_id, member in small_social_network.members.items():
        engagement_rate = member.engagement_rate()
        total_likes = sum(member.likes.values())
        total_comments = sum(member.comments.values())
        total_followers = len(member.followers)
        print(f"{member.name} (ID: {member_id}) - Engagement Rate: {engagement_rate:.2f}%")
        print(f"  Total Likes: {total_likes}, Total Comments: {total_comments}, Total Followers: {total_followers}")
        print(f"  Actual calculation: ({total_likes} + {total_comments}) / {total_followers} * 100\n")

def test_influence(small_social_network):
    print("Calculating influence...")
    for liker_id, liker in small_social_network.members.items():
        for likee_id, likee in small_social_network.members.items():
            if liker_id != likee_id:
                influence = liker.influence_on(likee)
                likes_to_likee = liker.likes_to[likee_id]
                comments_to_likee = liker.comments_to[likee_id]
                total_engagement = liker.total_engagement()
                print(f"{liker.name} (ID: {liker_id}) likes {likee.name} (ID: {likee_id}) - Influence: {influence:.2f}%")
                print(f"  Likes to {likee.name}: {likes_to_likee}, Comments to {likee.name}: {comments_to_likee}, Total Engagement: {total_engagement}")
                print(f"  Actual calculation: ({likes_to_likee} + {comments_to_likee}) / {total_engagement} * 100\n")

def test_shortest_path(small_social_network):
    print("Testing shortest paths...")
    members = small_social_network.members
    for member_id, member in members.items():
        for other_id, other in members.items():
            if member_id != other_id:
                path = member.shortest_path_to(other, members)
                print(f"Shortest path from {member.name} (ID: {member_id}) to {other.name} (ID: {other_id}): {' -> '.join(str(m) for m in path)}")
                print(f"  Path: {path}")
                print(f"  Actual path calculation: Starting at {member_id}, traversing through {path[:-1]}, ending at {other_id}\n")

def test_highest_engagement_path(small_social_network):
    print("Testing highest engagement paths...")
    members = small_social_network.members
    for member_id, member in members.items():
        for other_id, other in members.items():
            if member_id != other_id:
                path, engagement = member.highest_engagement_path_to(other, members)
                print(f"Highest engagement path from {member.name} (ID: {member_id}) to {other.name} (ID: {other_id}): {' -> '.join(str(m) for m in path)} with engagement: {engagement}")
                print(f"  Path: {path}")
                print(f"  Actual path calculation: Starting at {member_id}, traversing through {path[:-1]}, ending at {other_id} with total engagement: {engagement}\n")
