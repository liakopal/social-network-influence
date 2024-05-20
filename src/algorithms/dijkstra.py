# algorithms/dijkstra.py
import heapq

class Dijkstra:
    @staticmethod
    def traverse_graph(graph, start):
        distances = {node: float('infinity') for node in graph.adj_list}
        distances[start] = 0
        pq = [(0, start)]
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in graph.get_neighbors(current_node).items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances

    @staticmethod
    def traverse_members(members, start_id, end_id):
        distances = {member_id: float('infinity') for member_id in members}
        previous_nodes = {member_id: None for member_id in members}
        distances[start_id] = 0
        pq = [(0, start_id)]
        
        while pq:
            current_distance, current_member_id = heapq.heappop(pq)
            
            if current_distance > distances[current_member_id]:
                continue
            
            current_member = members[current_member_id]
            
            for neighbor in current_member.following:
                neighbor_id = neighbor.member_id
                distance = current_distance + 1
                
                if distance < distances[neighbor_id]:
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
        return path if path and path[0] == start_id else []
