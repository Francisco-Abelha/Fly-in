from drone import Drone
from zone import Zone
from graph import Graph


class Simulation:

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph = graph
        self.drones = drones
        self.turn: int = 0

    def count_in_zone(self, zone: Zone) -> int:
        return sum(1 for d in self.drones if d.reserved_zone is zone)

    def run_simulation(self) -> None:

        while not all(d.has_arrived for d in self.drones):
            self.turn += 1
            moved = False
            print_list: list[str] = []
            for d in self.drones:
                if d.in_transit:
                    d.advance()
                    moved = True
                    print_list.append(str(d))
                else:
                    nxt = d.next_zone()
                    if nxt is None:
                        continue
                    if (
                        self.count_in_zone(nxt) < nxt.max_drones
                        or nxt is self.graph.end
                    ):
                        d.advance()
                        moved = True
                        print_list.append(str(d))
            if not moved:
                raise ValueError(
                    f"deadlock: no drone could move on turn {self.turn}"
                )
            self._check_capacities()
            if print_list:
                print(" ".join(print_list))

    def _check_capacities(self) -> None:
        """Fail loudly if the current turn's state breaks a capacity rule.

        Called once per turn (after all moves). Verifies no zone holds more
        drones than its ``max_drones`` — start and end are exempt — and that
        no drone sits in a blocked zone. Raises ``ValueError`` on any
        violation so an illegal run can't masquerade as a fast one.

        TODO (link capacity): also enforce each connection's
        ``max_link_capacity``. Snapshot drone positions at the start of the
        turn, tally how many drones cross each connection, and reject any
        over its link cap. Not triggered by single-path routing, but needed
        once multi-path can overload a link tighter than its feeding zones.
        """
        for zone in self.graph.zones.values():
            if zone is self.graph.start or zone is self.graph.end:
                continue
            if self.count_in_zone(zone) > zone.max_drones:
                raise ValueError(
                    f"turn {self.turn}: {zone.name} over capacity"
                )
        for drone in self.drones:
            if drone.position.is_blocked():
                raise ValueError(
                    f"turn {self.turn}: drone D{drone.drone_id}"
                    "in blocked zone"
                )
