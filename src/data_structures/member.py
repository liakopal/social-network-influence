# data_structures/member.py
from collections import defaultdict, deque
import heapq
import random

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.followers = set()
        self.following = set()
        self.likes = defaultdict(int)
        self.comments = defaultdict(int)
        self.likes_to = defaultdict(int)
        self.comments_to = defaultdict(int)

    def follow(self, other):
        self.following.add(other)
        other.followers.add(self)

    def like(self, other, count=1):
        self.likes[other.member_id] += count
        self.likes_to[other.member_id] += count

    def comment(self, other, count=1):
        self.comments[other.member_id] += count
        self.comments_to[other.member_id] += count

    def engagement_rate(self):
        followers_count = len(self.followers)
        if followers_count == 0:
            return 0.0
        total_likes = sum(self.likes.values())
        total_comments = sum(self.comments.values())
        return (total_likes + total_comments) / followers_count * 100

    def total_engagement(self):
        return sum(self.likes.values()) + sum(self.comments.values())

    def influence_on(self, other):
        total_engagement = self.total_engagement()
        if total_engagement == 0:
            return 0.0
        return (self.likes_to[other.member_id] + self.comments_to[other.member_id]) / total_engagement * 100

    def shortest_path_to(self, other, members):
        if self == other:
            return [self.member_id]

        visited = set()
        queue = deque([(self, [self.member_id])])

        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for neighbor in current.following:
                if neighbor == other:
                    return path + [neighbor.member_id]
                queue.append((neighbor, path + [neighbor.member_id]))
        return []

    def highest_engagement_path_to(self, other, members, max_depth=5):
        if self == other:
            return [self.member_id], 0
        visited = set()
        max_heap = [(-self.total_engagement(), self.member_id, [self.member_id])]
        best_path, best_engagement = [], 0

        while max_heap:
            negative_engagement, current_id, path = heapq.heappop(max_heap)
            current = members[current_id]
            engagement = -negative_engagement

            if current == other:
                if engagement > best_engagement:
                    best_path, best_engagement = path, engagement
                continue

            if len(path) > max_depth:
                continue

            visited.add(current)

            for neighbor in current.following:
                if neighbor not in visited:
                    new_path = path + [neighbor.member_id]
                    new_engagement = engagement + neighbor.total_engagement()
                    heapq.heappush(max_heap, (-new_engagement, neighbor.member_id, new_path))

        return best_path, best_engagement

    @classmethod
    def generate_large_network(cls, num_members=1000, num_followings=10000, num_interactions=5000):
        members = {i: cls(i, chr(65 + (i - 1) % 26)) for i in range(1, num_members + 1)}

        for _ in range(num_followings):
            follower_id = random.randint(1, num_members)
            followee_id = random.randint(1, num_members)
            if follower_id != followee_id:
                members[follower_id].follow(members[followee_id])

        for _ in range(num_interactions):
            liker_id = random.randint(1, num_members)
            likee_id = random.randint(1, num_members)
            if liker_id != likee_id:
                members[liker_id].like(members[likee_id], random.randint(0, 9))
            commenter_id = random.randint(1, num_members)
            commentee_id = random.randint(1, num_members)
            if commenter_id != commentee_id:
                members[commenter_id].comment(members[commentee_id], random.randint(0, 9))

        return members
