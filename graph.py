from zone import Zone


class Graph:

    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.zones: dict[str, Zone] = {}
        self.start: Zone | None = None
        self.end: Zone | None = None

    def add_zone(self, zone: Zone) -> None:

        if zone.name in self.zones:
            raise ValueError("Rejecting duplicate Zones")
        self.zones[zone.name] = zone
