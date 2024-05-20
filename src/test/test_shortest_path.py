import random
from utils import timed_test

@timed_test
def test_large_network_shortest_path(large_network):
    print("Testing shortest paths for 10 random pairs of members...")
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
