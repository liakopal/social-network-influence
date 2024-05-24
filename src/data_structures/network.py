from collections import defaultdict
from data_structures.member import Member

class Network:
    def __init__(self):
        self.members = {}

    def add_member(self, member_id, name):
        self.members[member_id] = Member(member_id, name)

    def follow(self, follower_id, followee_id):
        follower = self.members[follower_id]
        followee = self.members[followee_id]
        follower.follow(followee)

    def like(self, liker_id, likee_id, amount):
        liker = self.members[liker_id]
        likee = self.members[likee_id]
        liker.like(likee, amount)

    def comment(self, commenter_id, commente_id, amount):
        commenter = self.members[commenter_id]
        commente = self.members[commente_id]
        commenter.comment(commente, amount)

    def ensure_required_path(self, path):
        for i in range(len(path) - 1):
            self.follow(path[i], path[i + 1])

    def generate_large_network(self, num_members, num_followings, num_interactions):
        import random
        # Generate members
        for i in range(1, num_members + 1):
            self.add_member(i, f'Member{i}')

        # Ensure a specific path: 1 -> 2 -> 3 -> 4 -> 5
        specific_path = [1, 2, 3, 4, 5]
        self.ensure_required_path(specific_path)

        # Generate additional random followings while avoiding creating shorter paths
        while num_followings > 0:
            follower_id = random.randint(1, num_members)
            followee_id = random.randint(1, num_members)
            if follower_id != followee_id and (follower_id, followee_id) not in zip(specific_path, specific_path[1:]):
                self.follow(follower_id, followee_id)
                num_followings -= 1

        # Generate random interactions (likes and comments)
        for _ in range(num_interactions):
            liker_id = random.randint(1, num_members)
            likee_id = random.randint(1, num_members)
            if liker_id != likee_id:
                self.like(liker_id, likee_id, random.randint(1, 10))
                self.comment(liker_id, likee_id, random.randint(1, 10))
