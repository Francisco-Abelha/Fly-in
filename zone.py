from enum import Enum


class ZoneType(str, Enum):

    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Zone:

    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            zone_type: ZoneType = ZoneType.NORMAL,
            color: str | None = None,
            max_drones: int = 1
    ) -> None:

        self.name = name
        self.coords = (x, y)
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.neighbors: set["Zone"] = set()

    @property
    def movement_cost(self) -> int:
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1

    def __repr__(self) -> str:
        return (
            f"Name: '{self.name}', "
            f"Coords: {self.coords}, "
            f"Zone Type: {self.zone_type}, "
            f"Color: '{self.color}', "
            f"Max drones allowed: {self.max_drones}"
        )
