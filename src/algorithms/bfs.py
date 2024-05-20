from collections import deque

class BFS:
    @staticmethod
    def traverse(graph, start_node):
        visited = set()
        queue = deque([start_node])
        traversal_order = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                traversal_order.append(node)
                queue.extend(neighbor for neighbor in graph[node] if neighbor not in visited)

        return traversal_order
