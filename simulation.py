from drone import Drone
from zone import Zone
from graph import Graph
import typing


class Simulation:
    """Turn-based engine that advances drones along their paths
    to the end zone, respecting capacity rules.
    """
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph = graph
        self.drones = drones
        self.turn: int = 0

    def count_in_zone(self, zone: Zone) -> int:
        """Count how many drones are in a zone"""
        return sum(1 for d in self.drones if d.reserved_zone is zone)

    def run_simulation(self) -> typing.Generator[list[Drone], None, None]:
        """Generator that yields the list of drones that moved each turn.
        runs until all drones have arrived.
        raises ValueError on deadlock, and validates capacity each turn
        """
        while not all(d.has_arrived for d in self.drones):
            self.turn += 1
            moved = False
            moved_drones: list[Drone] = []
            for d in self.drones:
                if d.in_transit:
                    d.advance()
                    moved = True
                    moved_drones.append(d)
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
                        moved_drones.append(d)
            if not moved:
                raise ValueError(
                    f"deadlock: no drone could move on turn {self.turn}"
                )
            self._check_capacities()
            yield moved_drones

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
