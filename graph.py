from zone import Zone
from connection import Connection


class Graph:

    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.zones: dict[str, Zone] = {}
        self.start: Zone | None = None
        self.end: Zone | None = None
        self.connections: list[Connection] = []
        self._edges: set[frozenset[Zone]] = set()

    def add_zone(self, zone: Zone) -> None:

        if zone.name in self.zones:
            raise ValueError("Rejecting duplicate Zones")
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:

        key = frozenset({connection.zone_a, connection.zone_b})
        if key in self._edges:
            raise ValueError("Error: Duplicate Connection")

        self._edges.add(key)
        self.connections.append(connection)
