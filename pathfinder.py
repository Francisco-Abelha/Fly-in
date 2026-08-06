from graph import Graph
from zone import Zone
from collections import deque
from heapq import heappop, heappush
from itertools import count


class Pathfinder:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def bfs(self) -> list[Zone]:

        start = self.graph.start
        goal = self.graph.end

        assert start is not None
        assert goal is not None

        parents: dict[Zone, Zone | None] = {}
        parents[start] = None

        visited = set()

        queue = deque([start])

        visited.add(start)

        while queue:
            current = queue.popleft()
            if current is not None:
                if current == goal:
                    path = []
                    cursor: Zone | None = goal
                    while cursor is not None:
                        path.append(cursor)
                        cursor = parents[cursor]
                    path.reverse()
                    return path
                else:
                    for neighbor in current.neighbors:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                            parents[neighbor] = current
        return []

    def dijkstra(self) -> list[Zone]:

        start = self.graph.start
        goal = self.graph.end

        assert start is not None
        assert goal is not None

        parents: dict[Zone, Zone | None] = {}
        parents[start] = None

        counter = count()

        pq = [(0, 0, next(counter), start)]

        distances = {start: (0, 0)}

        visited = set()

        INF = (float("inf"), float("inf"))

        while pq:

            cost, nonprio, _, current_node = heappop(pq)

            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == goal:
                path = []
                cursor: Zone | None = goal
                while cursor is not None:
                    path.append(cursor)
                    cursor = parents[cursor]
                path.reverse()
                return path

            for neighbor in current_node.neighbors:
                if neighbor.is_blocked():
                    continue
                new_cost = cost + neighbor.movement_cost
                new_np = nonprio + (0 if neighbor.is_priority() else 1)
                if (new_cost, new_np) < distances.get(neighbor, INF):
                    distances[neighbor] = (new_cost, new_np)
                    heappush(pq, (new_cost, new_np, next(counter), neighbor))
                    parents[neighbor] = current_node

        return []
