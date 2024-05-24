import heapq
from utils import log_and_print

class Dijkstra:
    @staticmethod
    def traverse_members(members, start_id, end_id, file=None):
        log_and_print(f"Starting Dijkstra's algorithm to find shortest path from {start_id} to {end_id}", color='red', file=file)
        distances = {member_id: float('infinity') for member_id in members}
        previous_nodes = {member_id: None for member_id in members}
        distances[start_id] = 0
        pq = [(0, start_id)]

        while pq:
            current_distance, current_member_id = heapq.heappop(pq)
            log_and_print(f"Visiting member {current_member_id}, current distance: {current_distance}", color='red', file=file)

            if current_distance > distances[current_member_id]:
                continue

            current_member = members[current_member_id]

            for neighbor in current_member.following:
                neighbor_id = neighbor.member_id
                distance = current_distance + 1

                log_and_print(f"Checking neighbor {neighbor_id} with current distance {distance}", color='red', file=file)

                if distance < distances[neighbor_id]:
                    log_and_print(f"Updating distance for member {neighbor_id}: old distance {distances[neighbor_id]}, new distance {distance}", color='red', file=file)
                    distances[neighbor_id] = distance
                    previous_nodes[neighbor_id] = current_member_id
                    heapq.heappush(pq, (distance, neighbor_id))

        # Reconstruct the path
        path = []
        current_id = end_id
        while current_id is not None:
            path.append(current_id)
            current_id = previous_nodes[current_id]

        path.reverse()
        log_and_print(f"Shortest path using Dijkstra's: {path}", color='red', file=file)
        return path if path and path[0] == start_id else []
