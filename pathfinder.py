from graph import Graph
from zone import Zone
from collections import deque


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
