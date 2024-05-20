# data_structures/network.py
from .member import Member

class Network:
    def __init__(self):
        self.members = {}

    def add_member(self, member_id, name):
        self.members[member_id] = Member(member_id, name)

    def follow(self, follower_id, followee_id):
        self.members[follower_id].follow(self.members[followee_id])

    def like(self, liker_id, likee_id, count=1):
        self.members[liker_id].like(self.members[likee_id], count)

    def comment(self, commenter_id, commentee_id, count=1):
        self.members[commenter_id].comment(self.members[commentee_id], count)

    def get_member(self, member_id):
        return self.members.get(member_id)

    def generate_large_network(self, num_members=1000, num_followings=10000, num_interactions=5000):
        self.members = Member.generate_large_network(num_members, num_followings, num_interactions)
        return self
