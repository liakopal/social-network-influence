import logging
from collections import defaultdict
from utils import generate_progressive_networks
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra

# Setup logging
logging.basicConfig(filename='network_analysis.log', level=logging.INFO, format='%(message)s', filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

def main():
    sizes = [10]  # Network size for testing
    networks = generate_progressive_networks(sizes)

    with open("network_analysis_output.txt", "w") as f:
        for idx, network in enumerate(networks):
            size = sizes[idx]
            header = f"\n{'='*10} Testing Network of Size {size} {'='*10}\n"
            f.write(header)

            total_members = len(network.members)
            total_followings = sum(len(member.following) for member in network.members.values())
            total_likes = sum(sum(member.likes.values()) for member in network.members.values())
            total_comments = sum(sum(member.comments.values()) for member in network.members.values())
            total_engagements = total_likes + total_comments

            network_summary = (
                f"Total members: {total_members}\n"
                f"Total followings: {total_followings}\n"
                f"Total likes: {total_likes}\n"
                f"Total comments: {total_comments}\n"
                f"Total engagements: {total_engagements}\n"
            )
            f.write(network_summary)

            for member_id, member in network.members.items():
                total_likes_given = sum(member.likes.values())
                total_likes_received = sum(m.likes.get(member_id, 0) for m in network.members.values())
                total_comments_given = sum(member.comments.values())
                total_comments_received = sum(m.comments.get(member_id, 0) for m in network.members.values())
                followers_count = len(member.followers)

                # Engagement rate calculation
                if followers_count > 0:
                    engagement_rate = (total_likes_given + total_comments_given) / followers_count * 100
                else:
                    engagement_rate = 0.0

                member_info = (
                    f"\nMember {member_id}: Follows {len(member.following)} others, Followed by {len(member.followers)}\n"
                    f"Likes given: {dict(member.likes)} (Total given: {total_likes_given})\n"
                    f"Likes received: {total_likes_received}\n"
                    f"Comments given: {dict(member.comments)} (Total given: {total_comments_given})\n"
                    f"Comments received: {total_comments_received}\n"
                    f"Engagement rate: {engagement_rate:.2f}\n"
                )
                f.write(member_info)

                # Influence calculations for each member
                interacted_members = set(member.likes.keys()).union(set(member.comments.keys()))
                for followee_id in interacted_members:
                    likes_to = member.likes.get(followee_id, 0)
                    comments_to = member.comments.get(followee_id, 0)
                    if engagement_rate != 0:
                        influence_to_followee = (likes_to + comments_to) / engagement_rate
                    else:
                        influence_to_followee = 0.0

                    influence_info = f"Influence to Member {followee_id}: {influence_to_followee:.2f}\n"
                    influence_proof = f"Calculation: ({likes_to} likes + {comments_to} comments) / {engagement_rate:.2f} engagement rate\n"
                    f.write(influence_info)
                    f.write(influence_proof)

                # Example BFS, DFS, and Dijkstra usage
                for other_id in network.members:
                    if member_id != other_id:
                        path_bfs = BFS.shortest_path(network.members, member_id, other_id)
                        if path_bfs:
                            bfs_info = (
                                f"Shortest path to member {other_id} using BFS: {len(path_bfs) - 1} steps\n"
                                f"Path: {path_bfs}\n"
                            )
                            f.write(bfs_info)

                        path_dfs, max_engagement = DFS.highest_engagement_path(network.members, member_id, other_id)
                        if path_dfs:
                            dfs_info = (
                                f"Highest engagement path to member {other_id} using DFS: {len(path_dfs) - 1} steps\n"
                                f"Engagement score: {max_engagement}\n"
                                f"Path: {path_dfs}\n"
                            )
                            f.write(dfs_info)

                        path_dijkstra = Dijkstra.traverse_members(network.members, member_id, other_id)
                        if path_dijkstra:
                            dijkstra_info = (
                                f"Shortest path to member {other_id} using Dijkstra's: {len(path_dijkstra) - 1} steps\n"
                                f"Path: {path_dijkstra}\n"
                            )
                            f.write(dijkstra_info)

if __name__ == "__main__":
    main()
