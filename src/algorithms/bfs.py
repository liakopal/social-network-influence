from collections import deque
from utils import log_and_print

class BFS:
    @staticmethod
    def shortest_path(members, start_id, end_id, file=None):
        log_and_print(f"Starting BFS to find the shortest path from {start_id} to {end_id}", color='blue', file=file)
        
        # Initialization
        for member in members.values():
            member.color = 'WHITE'
            member.distance = float('inf')
            member.predecessor = None

        start_member = members[start_id]
        start_member.color = 'GRAY'
        start_member.distance = 0
        start_member.predecessor = None

        queue = deque([start_member])

        while queue:
            current_member = queue.popleft()
            log_and_print(f"Visiting member {current_member.member_id}, current path: {BFS.build_path(current_member)}", color='blue', file=file)

            for neighbor in current_member.following:
                if neighbor.color == 'WHITE':
                    neighbor.color = 'GRAY'
                    neighbor.distance = current_member.distance + 1
                    neighbor.predecessor = current_member
                    queue.append(neighbor)
                    log_and_print(f"Adding neighbor {neighbor.member_id} to the queue", color='blue', file=file)

            current_member.color = 'BLACK'

        path = BFS.build_path(members[end_id])
        if members[end_id].distance == float('inf'):
            log_and_print(f"No path found from {start_id} to {end_id}", color='blue', file=file)
            return None
        log_and_print(f"Found path: {path}", color='blue', file=file)
        return path

    @staticmethod
    def build_path(member):
        path = []
        while member is not None:
            path.append(member.member_id)
            member = member.predecessor
        return path[::-1]
