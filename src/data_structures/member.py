from collections import defaultdict

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
        # BFS attributes
        self.color = 'WHITE'
        self.distance = float('inf')
        self.predecessor = None

    def follow(self, other):
        self.following.add(other)
        other.followers.add(self)

    def like(self, other, count=1):
        self.likes[other.member_id] += count
        other.likes_to[self.member_id] += count

    def comment(self, other, count=1):
        self.comments[other.member_id] += count
        other.comments_to[self.member_id] += count

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
