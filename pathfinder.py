from graph import Graph
from zone import Zone
from heapq import heappop, heappush
from itertools import count
from path import Path


class Pathfinder:
    """Calculates the optimal path from start to end considering
    all the restrictions imposed by the subject.
    """
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def dijkstra(self, reserved: set[Zone] | None = None) -> list[Zone]:
        """Algorithm that finds the shortest path from start the end zone
        Its cost-aware, skips blocked and eserved zones, preferes priority
        zones and returns [] if the end is unreachable.
        Reserve param is used by the greedy_pathfinder to calculate
        multiple possible paths.
        """
        start = self.graph.start
        goal = self.graph.end

        assert start is not None
        assert goal is not None

        if reserved is None:
            reserved = set()

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
                if neighbor in reserved:
                    continue
                new_cost = cost + neighbor.movement_cost
                new_np = nonprio + (0 if neighbor.is_priority() else 1)
                if (new_cost, new_np) < distances.get(neighbor, INF):
                    distances[neighbor] = (new_cost, new_np)
                    heappush(pq, (new_cost, new_np, next(counter), neighbor))
                    parents[neighbor] = current_node

        return []

    def greedy_pathfinder(self) -> list[Path]:
        """Find multiple vertex-disjoint paths: repeatedly run Dijkstra,
        reserving each path's intermediate zones so later paths avoid them,
        until no path remains. Return the list of paths.
        """
        reserved: set[Zone] = set()
        paths_list: list[Path] = []
        while True:
            alg_output: list[Zone] = self.dijkstra(reserved)
            if not alg_output:
                break
            paths_list.append(Path(alg_output))
            interior = alg_output[1:-1]
            if not interior:
                break
            reserved.update(interior)
        return paths_list
