from zone import Zone
from connection import Connection


class Graph:
    """Structure for the zones and connections map"""

    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.zones: dict[str, Zone] = {}
        self.start: Zone | None = None
        self.end: Zone | None = None
        self.connections: list[Connection] = []
        self._edges: dict[frozenset[Zone], Connection] = {}

    def validate(self) -> None:
        """Checks start, end, and nb_drones exist
        and raises an error otherwise
        """
        if self.start is None:
            raise ValueError("Graph has no start hub.")
        if self.end is None:
            raise ValueError("Graph has no end hub.")
        if self.nb_drones is None:
            raise ValueError("Graph has no number of drones.")

    def connection_between(
            self, zone_a: Zone, zone_b: Zone
    ) -> Connection | None:
        """Returns the connection between two zones,
        or None if it doesn't exist
        """
        return self._edges.get(frozenset({zone_a, zone_b}), None)

    def add_zone(self, zone: Zone) -> None:
        """Add a new zone to the graph"""
        if zone.name in self.zones:
            raise ValueError("Rejecting duplicate Zones")
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Add a connection to the graph,
        wires both neighbors and rejects duplicates
        """
        key = frozenset({connection.zone_a, connection.zone_b})
        if key in self._edges:
            raise ValueError("Error: Duplicate Connection")

        self._edges[key] = connection
        self.connections.append(connection)
        connection.zone_a.neighbors.add(connection.zone_b)
        connection.zone_b.neighbors.add(connection.zone_a)
