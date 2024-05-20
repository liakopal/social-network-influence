import random
from utils import timed_test

@timed_test
def test_large_network_influence(large_network):
    print("Testing influence for 100 random pairs of members...")
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
