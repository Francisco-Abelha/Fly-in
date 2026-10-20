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

    def run_simulation(self) -> typing.Generator[list[Drone], None, None]:
        """Generator that yields the list of drones that moved each turn.
        runs until all drones have arrived.
        raises ValueError on deadlock, and validates capacity each turn
        """
        not_arrived: list[Drone] = list(self.drones)
        while not_arrived:
            self.turn += 1
            moved = False
            moved_drones: list[Drone] = []
            link_usage: dict[frozenset[Zone], int] = {}
            reserved_zones_counter: dict[Zone, int] = {}
            for d in not_arrived:
                reserved_zones_counter[d.reserved_zone] = (
                    reserved_zones_counter.get(d.reserved_zone, 0) + 1
                )
            for d in not_arrived:
                if d.in_transit:
                    d.advance()
                    moved = True
                    moved_drones.append(d)
                else:
                    nxt = d.next_zone()
                    if nxt is None:
                        continue
                    key = frozenset({d.position, nxt})
                    link = self.graph.connection_between(d.position, nxt)
                    zone_ok = (reserved_zones_counter.get(nxt, 0)
                               < nxt.max_drones or nxt is self.graph.end)
                    link_ok = link is not None and (
                        link_usage.get(key, 0) < link.max_link_capacity
                    )
                    if zone_ok and link_ok:
                        link_usage[key] = link_usage.get(key, 0) + 1
                        leaving_from = d.reserved_zone
                        d.advance()
                        new_zone = d.reserved_zone
                        reserved_zones_counter[leaving_from] = (
                            reserved_zones_counter.get(leaving_from, 0) - 1
                        )
                        reserved_zones_counter[new_zone] = (
                            reserved_zones_counter.get(new_zone, 0) + 1
                        )
                        moved = True
                        moved_drones.append(d)
            new_lst = []
            for d in not_arrived:
                if not d.has_arrived:
                    new_lst.append(d)
            not_arrived = new_lst
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
        """
        reserved_zones_counter: dict[Zone, int] = {}
        for d in self.drones:
            reserved_zones_counter[d.reserved_zone] = (
                reserved_zones_counter.get(d.reserved_zone, 0) + 1
            )
        for zone in self.graph.zones.values():
            if zone is self.graph.start or zone is self.graph.end:
                continue
            if reserved_zones_counter.get(zone, 0) > zone.max_drones:
                raise ValueError(
                    f"turn {self.turn}: {zone.name} over capacity"
                )
        for drone in self.drones:
            if drone.position.is_blocked():
                raise ValueError(
                    f"turn {self.turn}: drone D{drone.drone_id}"
                    "in blocked zone"
                )
