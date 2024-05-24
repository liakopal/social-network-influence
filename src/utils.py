import random
from data_structures.network import Network
from termcolor import colored
import logging

def generate_progressive_networks(sizes):
    networks = []
    for size in sizes:
        net = Network()
        members = {}
        for i in range(1, size + 1):
            net.add_member(i, f"Member_{i}")
            members[i] = f"Member_{i}"

        print(f"Generated members for network of size {size}: {members}")

        follow_relationships = []
        for _ in range(size * 10):
            follower = random.randint(1, size)
            followee = random.randint(1, size)
            if follower != followee:
                net.follow(follower, followee)
                follow_relationships.append((follower, followee))

        print(f"Generated follow relationships for network of size {size}: {follow_relationships}")

        like_comment_interactions = []
        for _ in range(size * 5):
            liker = random.randint(1, size)
            likee = random.randint(1, size)
            if liker != likee:
                net.like(liker, likee, random.randint(0, 9))
                like_comment_interactions.append((liker, likee, 'like'))
            commenter = random.randint(1, size)
            commente = random.randint(1, size)
            if commenter != commente:
                net.comment(commenter, commente, random.randint(0, 9))
                like_comment_interactions.append((commenter, commente, 'comment'))

        print(f"Generated like and comment interactions for network of size {size}: {like_comment_interactions}")

        for member_id, member in net.members.items():
            total_likes_given = sum(member.likes.values())
            total_likes_received = sum(m.likes.get(member_id, 0) for m in net.members.values())
            total_comments_given = sum(member.comments.values())
            total_comments_received = sum(m.comments.get(member_id, 0) for m in net.members.values())
            engagement_rate = (total_likes_given + total_comments_given) / len(member.followers) * 100 if member.followers else 0
            member.engagement_rate_value = engagement_rate
        networks.append(net)
    return networks

def calculate_influence(network):
    for member in network.members.values():
        influences = {}
        for followee in member.following:
            likes_to_followee = member.likes.get(followee.member_id, 0)
            comments_to_followee = member.comments.get(followee.member_id, 0)
            influence = (likes_to_followee + comments_to_followee) / member.engagement_rate_value if member.engagement_rate_value else 0
            influences[followee.member_id] = influence
        member.influences = influences

# Colors for termcolor
TERMCOLOR_COLORS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']

def random_color():
    return random.choice(TERMCOLOR_COLORS)

def log_and_print(message, color=None, file=None):
    if color:
        colored_message = colored(message, color)
        print(colored_message)
        logging.info(message)
        if file:
            file.write(message + "\n")
    else:
        print(message)
        logging.info(message)
        if file:
            file.write(message + "\n")
