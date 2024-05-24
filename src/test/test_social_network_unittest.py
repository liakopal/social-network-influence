import unittest
import random
import sys
import os
import logging
from collections import defaultdict

# Configure logging to overwrite the log file each time
logging.basicConfig(
    filename='test_results.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

# Ensure the parent directory is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.network import Network
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra
from utils import generate_progressive_networks

class TestSocialNetwork(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.network = Network()
        # Add members
        for i in range(1, 11):
            cls.network.add_member(i, f'Member{i}')
        
        # Ensure a specific path exists: 1 -> 2 -> 3 -> 4 -> 5
        path_must_include = [1, 2, 3, 4, 5]
        cls.network.ensure_required_path(path_must_include)
        
        # Log the mandatory path
        logging.info(f'Mandatory path created: {path_must_include}')
        
        # Generate additional random followings while avoiding creating shorter paths
        while len(cls.network.members) > 15:
            follower = random.choice(list(cls.network.members.keys()))
            followee = random.choice(list(cls.network.members.keys()))
            if follower != followee and (follower, followee) not in zip(path_must_include, path_must_include[1:]):
                cls.network.follow(follower, followee)
        
        # Log all connections for debugging
        for member_id, member in cls.network.members.items():
            logging.info(f'Member {member_id} follows: {list(member.following)}')
        
        # Generate random likes and comments
        for _ in range(20):
            liker = random.choice(list(cls.network.members.keys()))
            likee = random.choice(list(cls.network.members.keys()))
            if liker != likee:
                cls.network.like(liker, likee, random.randint(1, 10))
        
        for _ in range(20):
            commenter = random.choice(list(cls.network.members.keys()))
            commente = random.choice(list(cls.network.members.keys()))
            if commenter != commente:
                cls.network.comment(commenter, commente, random.randint(1, 10))

        # Generate a large network for other tests
        cls.large_networks = generate_progressive_networks([10])

    def test_engagement_rate(self):
        for member_id, member in self.network.members.items():
            engagement_rate = member.engagement_rate()
            total_likes = sum(member.likes.values())
            total_comments = sum(member.comments.values())
            total_followers = len(member.followers)
            expected_engagement_rate = (total_likes + total_comments) / total_followers * 100 if total_followers > 0 else 0
            logging.info(f'Member ID: {member_id}, Engagement Rate: {engagement_rate}, Expected: {expected_engagement_rate}')
            self.assertAlmostEqual(engagement_rate, expected_engagement_rate)

    def test_influence(self):
        for liker_id, liker in self.network.members.items():
            for likee_id, likee in self.network.members.items():
                if liker_id != likee_id:
                    influence = liker.influence_on(likee)
                    likes_to_likee = liker.likes_to[likee_id]
                    comments_to_likee = liker.comments_to[likee_id]
                    total_engagement = liker.total_engagement()
                    expected_influence = (likes_to_likee + comments_to_likee) / total_engagement * 100 if total_engagement > 0 else 0
                    logging.info(f'Liker ID: {liker_id}, Likee ID: {likee_id}, Influence: {influence}, Expected: {expected_influence}')
                    self.assertAlmostEqual(influence, expected_influence)

    def test_shortest_path(self):
        path = BFS.shortest_path(self.network.members, 1, 5)
        logging.info(f'Shortest Path from 1 to 5: {path}')
        self.assertIsNotNone(path, "No path found from member 1 to member 5")
        # Ensure the path includes all required nodes
        expected_path = [1, 2, 3, 4, 5]
        self.assertEqual(path, expected_path, f"Path does not include all required nodes in order. Expected: {expected_path}, Actual: {path}")

    def test_highest_engagement_path(self):
        path, engagement = DFS.highest_engagement_path(self.network.members, 1, 5)
        logging.info(f'Highest Engagement Path from 1 to 5: {path}, Engagement: {engagement}')
        self.assertIsNotNone(path, "No engagement path found from member 1 to member 5")
        self.assertGreater(engagement, 0)

    def test_large_network_engagement_rate(self):
        for network in self.large_networks:
            for member_id, member in network.members.items():
                engagement_rate = member.engagement_rate()
                logging.info(f'Large Network Member ID: {member_id}, Engagement Rate: {engagement_rate}')
                self.assertGreaterEqual(engagement_rate, 0.0)

    def test_large_network_shortest_path(self):
        for network in self.large_networks:
            member_ids = list(network.members.keys())
            for _ in range(3):  # Reduce the number of iterations
                member1_id = random.choice(member_ids)
                member2_id = random.choice(member_ids)
                if member1_id != member2_id:
                    path = BFS.shortest_path(network.members, member1_id, member2_id)
                    logging.info(f'Large Network Shortest Path from {member1_id} to {member2_id}: {path}')
                    self.assertIsNotNone(path, f"No path found from member {member1_id} to member {member2_id}")
                    self.assertEqual(path[0], member1_id)
                    self.assertEqual(path[-1], member2_id)

    def test_large_network_highest_engagement_path(self):
        for network in self.large_networks:
            member_ids = list(network.members.keys())
            for _ in range(3):  # Reduce the number of iterations
                member1_id = random.choice(member_ids)
                member2_id = random.choice(member_ids)
                if member1_id != member2_id:
                    path, engagement = DFS.highest_engagement_path(network.members, member1_id, member2_id)
                    logging.info(f'Large Network Highest Engagement Path from {member1_id} to {member2_id}: {path}, Engagement: {engagement}')
                    self.assertIsNotNone(path, f"No engagement path found from member {member1_id} to member {member2_id}")
                    self.assertGreater(engagement, 0)
                    self.assertEqual(path[0], member1_id)
                    self.assertEqual(path[-1], member2_id)

    def test_large_network_dijkstra(self):
        for network in self.large_networks:
            member_ids = list(network.members.keys())
            for _ in range(3):  # Reduce the number of iterations
                member1_id = random.choice(member_ids)
                member2_id = random.choice(member_ids)
                if member1_id != member2_id:
                    path = Dijkstra.traverse_members(network.members, member1_id, member2_id)
                    logging.info(f'Large Network Dijkstra Path from {member1_id} to {member2_id}: {path}')
                    self.assertIsNotNone(path, f"No path found from member {member1_id} to member {member2_id}")
                    self.assertEqual(path[0], member1_id)
                    self.assertEqual(path[-1], member2_id)

    @classmethod
    def tearDownClass(cls):
        # Generate the summary report for small network
        def summarize_network(network, label):
            total_members = len(network.members)
            total_followings = sum(len(member.following) for member in network.members.values())
            total_likes = sum(sum(member.likes.values()) for member in network.members.values())
            total_comments = sum(sum(member.comments.values()) for member in network.members.values())
            total_engagements = total_likes + total_comments

            summary = (
                f"========== {label} Network Analysis Summary ==========\n"
                f"Total members: {total_members}\n"
                f"Total followings: {total_followings}\n"
                f"Total likes: {total_likes}\n"
                f"Total comments: {total_comments}\n"
                f"Total engagements: {total_engagements}\n"
            )

            # Append the detailed member information
            for member_id, member in network.members.items():
                likes_given = dict(member.likes)
                comments_given = dict(member.comments)
                comments_received_from = defaultdict(int)
                for m in network.members.values():
                    if member_id in m.comments_to:
                        comments_received_from[m.member_id] += m.comments_to[member_id]
                
                # Compute shortest path and highest engagement path for each member
                shortest_paths = []
                highest_engagement_paths = []
                for other_id in network.members.keys():
                    if member_id != other_id:
                        shortest_path = BFS.shortest_path(network.members, member_id, other_id)
                        if shortest_path:
                            steps = len(shortest_path) - 1
                            shortest_paths.append(f"Shortest path to member {other_id} using BFS: {steps} steps\nPath: {shortest_path}")
                        else:
                            shortest_paths.append(f"Shortest path to member {other_id} using BFS: No path found")

                        highest_engagement_path, engagement = DFS.highest_engagement_path(network.members, member_id, other_id)
                        if highest_engagement_path:
                            highest_engagement_paths.append(f"Highest engagement path to member {other_id} using DFS: {highest_engagement_path}\nEngagement score: {engagement}")
                        else:
                            highest_engagement_paths.append(f"Highest engagement path to member {other_id} using DFS: No path found")

                summary += (
                    f"\nMember {member_id}: Follows {len(member.following)} others, Followed by {len(member.followers)}\n"
                    f"Likes given: {likes_given} (Total given: {sum(likes_given.values())})\n"
                    f"Likes received: {sum(m.likes_to[member_id] for m in network.members.values() if member_id in m.likes_to)}\n"
                    f"Comments given: {comments_given} (Total given: {sum(comments_given.values())})\n"
                    f"Comments received: {sum(m.comments_to[member_id] for m in network.members.values() if member_id in m.comments_to)}\n"
                    f"Comments received from: {dict(comments_received_from)}\n"
                    f"Engagement rate: {member.engagement_rate():.2f}\n"
                )

                # Append paths
                summary += "\n" + "\n".join(shortest_paths)
                summary += "\n" + "\n".join(highest_engagement_paths)

            return summary

        summary = summarize_network(cls.network, "Small")

        for i, large_network in enumerate(cls.large_networks):
            summary += "\n\n" + summarize_network(large_network, f"Large {i + 1}")

        with open('test_network_summary.txt', 'w') as f:
            f.write(summary)
            f.flush()
            os.fsync(f.fileno())

        # Log summary creation
        logging.info('test_network_summary.txt has been created.')


if __name__ == '__main__':
    unittest.main()

    # Explicitly call tearDownClass to generate the summary file
    TestSocialNetwork.tearDownClass()




# import unittest
# import random
# import sys
# import os
# import logging
# from collections import defaultdict

# # Configure logging to overwrite the log file each time
# logging.basicConfig(
#     filename='test_results.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filemode='w'
# )

# # Ensure the parent directory is in the sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from data_structures.network import Network
# from algorithms.bfs import BFS
# from algorithms.dfs import DFS
# from algorithms.dijkstra import Dijkstra
# from utils import generate_progressive_networks

# class TestSocialNetwork(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.network = Network()
#         # Add members
#         for i in range(1, 11):
#             cls.network.add_member(i, f'Member{i}')
        
#         # Ensure a specific path exists: 1 -> 2 -> 3 -> 4 -> 5
#         path_must_include = [1, 2, 3, 4, 5]
#         cls.network.ensure_required_path(path_must_include)
        
#         # Log the mandatory path
#         logging.info(f'Mandatory path created: {path_must_include}')
        
#         # Generate additional random followings while avoiding creating shorter paths
#         while len(cls.network.members) > 15:
#             follower = random.choice(list(cls.network.members.keys()))
#             followee = random.choice(list(cls.network.members.keys()))
#             if follower != followee and (follower, followee) not in zip(path_must_include, path_must_include[1:]):
#                 cls.network.follow(follower, followee)
        
#         # Log all connections for debugging
#         for member_id, member in cls.network.members.items():
#             logging.info(f'Member {member_id} follows: {list(member.following)}')
        
#         # Generate random likes and comments
#         for _ in range(20):
#             liker = random.choice(list(cls.network.members.keys()))
#             likee = random.choice(list(cls.network.members.keys()))
#             if liker != likee:
#                 cls.network.like(liker, likee, random.randint(1, 10))
        
#         for _ in range(20):
#             commenter = random.choice(list(cls.network.members.keys()))
#             commente = random.choice(list(cls.network.members.keys()))
#             if commenter != commente:
#                 cls.network.comment(commenter, commente, random.randint(1, 10))

#         # Generate a large network for other tests
#         cls.large_networks = generate_progressive_networks([10])

#     def test_engagement_rate(self):
#         for member_id, member in self.network.members.items():
#             engagement_rate = member.engagement_rate()
#             total_likes = sum(member.likes.values())
#             total_comments = sum(member.comments.values())
#             total_followers = len(member.followers)
#             expected_engagement_rate = (total_likes + total_comments) / total_followers * 100 if total_followers > 0 else 0
#             logging.info(f'Member ID: {member_id}, Engagement Rate: {engagement_rate}, Expected: {expected_engagement_rate}')
#             self.assertAlmostEqual(engagement_rate, expected_engagement_rate)

#     def test_influence(self):
#         for liker_id, liker in self.network.members.items():
#             for likee_id, likee in self.network.members.items():
#                 if liker_id != likee_id:
#                     influence = liker.influence_on(likee)
#                     likes_to_likee = liker.likes_to[likee_id]
#                     comments_to_likee = liker.comments_to[likee_id]
#                     total_engagement = liker.total_engagement()
#                     expected_influence = (likes_to_likee + comments_to_likee) / total_engagement * 100 if total_engagement > 0 else 0
#                     logging.info(f'Liker ID: {liker_id}, Likee ID: {likee_id}, Influence: {influence}, Expected: {expected_influence}')
#                     self.assertAlmostEqual(influence, expected_influence)

#     def test_shortest_path(self):
#         path = BFS.shortest_path(self.network.members, 1, 5)
#         logging.info(f'Shortest Path from 1 to 5: {path}')
#         self.assertIsNotNone(path, "No path found from member 1 to member 5")
#         # Ensure the path includes all required nodes
#         expected_path = [1, 2, 3, 4, 5]
#         self.assertEqual(path, expected_path, f"Path does not include all required nodes in order. Expected: {expected_path}, Actual: {path}")

#     def test_highest_engagement_path(self):
#         path, engagement = DFS.highest_engagement_path(self.network.members, 1, 5)
#         logging.info(f'Highest Engagement Path from 1 to 5: {path}, Engagement: {engagement}')
#         self.assertIsNotNone(path, "No engagement path found from member 1 to member 5")
#         self.assertGreater(engagement, 0)

#     def test_large_network_engagement_rate(self):
#         for network in self.large_networks:
#             for member_id, member in network.members.items():
#                 engagement_rate = member.engagement_rate()
#                 logging.info(f'Large Network Member ID: {member_id}, Engagement Rate: {engagement_rate}')
#                 self.assertGreaterEqual(engagement_rate, 0.0)

#     def test_large_network_shortest_path(self):
#         for network in self.large_networks:
#             member_ids = list(network.members.keys())
#             for _ in range(3):  # Reduce the number of iterations
#                 member1_id = random.choice(member_ids)
#                 member2_id = random.choice(member_ids)
#                 if member1_id != member2_id:
#                     path = BFS.shortest_path(network.members, member1_id, member2_id)
#                     logging.info(f'Large Network Shortest Path from {member1_id} to {member2_id}: {path}')
#                     self.assertIsNotNone(path, f"No path found from member {member1_id} to member {member2_id}")
#                     self.assertEqual(path[0], member1_id)
#                     self.assertEqual(path[-1], member2_id)

#     def test_large_network_highest_engagement_path(self):
#         for network in self.large_networks:
#             member_ids = list(network.members.keys())
#             for _ in range(3):  # Reduce the number of iterations
#                 member1_id = random.choice(member_ids)
#                 member2_id = random.choice(member_ids)
#                 if member1_id != member2_id:
#                     path, engagement = DFS.highest_engagement_path(network.members, member1_id, member2_id)
#                     logging.info(f'Large Network Highest Engagement Path from {member1_id} to {member2_id}: {path}, Engagement: {engagement}')
#                     self.assertIsNotNone(path, f"No engagement path found from member {member1_id} to member {member2_id}")
#                     self.assertGreater(engagement, 0)
#                     self.assertEqual(path[0], member1_id)
#                     self.assertEqual(path[-1], member2_id)

#     def test_large_network_dijkstra(self):
#         for network in self.large_networks:
#             member_ids = list(network.members.keys())
#             for _ in range(3):  # Reduce the number of iterations
#                 member1_id = random.choice(member_ids)
#                 member2_id = random.choice(member_ids)
#                 if member1_id != member2_id:
#                     path = Dijkstra.traverse_members(network.members, member1_id, member2_id)
#                     logging.info(f'Large Network Dijkstra Path from {member1_id} to {member2_id}: {path}')
#                     self.assertIsNotNone(path, f"No path found from member {member1_id} to member {member2_id}")
#                     self.assertEqual(path[0], member1_id)
#                     self.assertEqual(path[-1], member2_id)

#     @classmethod
#     def tearDownClass(cls):
#         # Generate the summary report for small network
#         def summarize_network(network, label):
#             total_members = len(network.members)
#             total_followings = sum(len(member.following) for member in network.members.values())
#             total_likes = sum(sum(member.likes.values()) for member in network.members.values())
#             total_comments = sum(sum(member.comments.values()) for member in network.members.values())
#             total_engagements = total_likes + total_comments

#             summary = (
#                 f"========== {label} Network Analysis Summary ==========\n"
#                 f"Total members: {total_members}\n"
#                 f"Total followings: {total_followings}\n"
#                 f"Total likes: {total_likes}\n"
#                 f"Total comments: {total_comments}\n"
#                 f"Total engagements: {total_engagements}\n"
#             )

#             # Append the detailed member information
#             for member_id, member in network.members.items():
#                 likes_given = dict(member.likes)
#                 comments_given = dict(member.comments)
#                 comments_received_from = defaultdict(int)
#                 for m in network.members.values():
#                     if member_id in m.comments_to:
#                         comments_received_from[m.member_id] += m.comments_to[member_id]
                
#                 summary += (
#                     f"\nMember {member_id}: Follows {len(member.following)} others, Followed by {len(member.followers)}\n"
#                     f"Likes given: {likes_given} (Total given: {sum(likes_given.values())})\n"
#                     f"Likes received: {sum(m.likes_to[member_id] for m in network.members.values() if member_id in m.likes_to)}\n"
#                     f"Comments given: {comments_given} (Total given: {sum(comments_given.values())})\n"
#                     f"Comments received: {sum(m.comments_to[member_id] for m in network.members.values() if member_id in m.comments_to)}\n"
#                     f"Comments received from: {dict(comments_received_from)}\n"
#                     f"Engagement rate: {member.engagement_rate():.2f}\n"
#                 )

#             # Append shortest path and highest engagement path details
#             shortest_path = BFS.shortest_path(network.members, 1, 5)
#             highest_engagement_path, highest_engagement = DFS.highest_engagement_path(network.members, 1, 5)
            
#             summary += (
#                 f"\nShortest path from Member 1 to Member 5 using BFS: {len(shortest_path) - 1} steps\n"
#                 f"Path: {shortest_path}\n"
#                 f"Highest engagement path from Member 1 to Member 5 using DFS: {len(highest_engagement_path) - 1} steps\n"
#                 f"Engagement score: {highest_engagement}\n"
#                 f"Path: {highest_engagement_path}\n"
#             )

#             return summary

#         summary = summarize_network(cls.network, "Small")

#         for i, large_network in enumerate(cls.large_networks):
#             summary += "\n\n" + summarize_network(large_network, f"Large {i + 1}")

#         with open('test_network_summary.txt', 'w') as f:
#             f.write(summary)
#             f.flush()
#             os.fsync(f.fileno())

#         # Log summary creation
#         logging.info('test_network_summary.txt has been created.')

# if __name__ == '__main__':
#     unittest.main()

#     # Explicitly call tearDownClass to generate the summary file
#     TestSocialNetwork.tearDownClass()
