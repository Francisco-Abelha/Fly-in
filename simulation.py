from drone import Drone
from zone import Zone
from graph import Graph


class Simulation:

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph = graph
        self.drones = drones
        self.turn: int = 0

    def count_in_zone(self, zone: Zone) -> int:
        return sum(1 for d in self.drones if d.position is zone)

    def run_simulation(self) -> None:

        while not all(d.has_arrived for d in self.drones):
            self.turn += 1
            moved = False
            print_list: list[str] = []
            for d in self.drones:
                nxt = d.next_zone()
                if nxt is None:
                    continue
                if (
                    self.count_in_zone(nxt) < nxt.max_drones
                    or nxt is self.graph.end
                ):
                    d.advance()
                    moved = True
                    print_list.append(f"D{d.drone_id}-{d.position.name}")
            if not moved:
                raise ValueError(
                    f"deadlock: no drone could move on turn {self.turn}"
                )
            if print_list:
                print(" ".join(print_list))
