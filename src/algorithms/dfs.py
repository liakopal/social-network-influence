import heapq
from utils import log_and_print

class DFS:
    @staticmethod
    def highest_engagement_path(members, start_id, end_id, file=None, max_depth=5):
        log_and_print(f"Starting DFS to find the highest engagement path from {start_id} to {end_id}", color='magenta', file=file)
        best_path, best_engagement = [], 0
        max_heap = [(-members[start_id].total_engagement(), start_id, [start_id])]

        while max_heap:
            negative_engagement, current_id, path = heapq.heappop(max_heap)
            current_member = members[current_id]
            current_engagement = -negative_engagement

            log_and_print(f"Visiting member {current_id}, current path: {path}, current engagement: {current_engagement}", color='magenta', file=file)

            if current_id == end_id:
                if current_engagement > best_engagement:
                    best_path, best_engagement = path, current_engagement
                continue

            if len(path) > max_depth:
                continue

            for neighbor in current_member.following:
                if neighbor.member_id not in path:
                    new_path = path + [neighbor.member_id]
                    new_engagement = current_engagement + neighbor.total_engagement()
                    heapq.heappush(max_heap, (-new_engagement, neighbor.member_id, new_path))

        log_and_print(f"Best path: {best_path}, Max engagement: {best_engagement}", color='magenta', file=file)
        return best_path, best_engagement
