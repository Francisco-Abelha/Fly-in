from enum import Enum


class ZoneType(str, Enum):
    """Types of zones"""
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Zone:
    """Define a zone with all its attributes as well as
    how many drones it can hold and all its neighbors.
    """
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
        """Return the cost of moving into a certain zone"""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1

    def is_blocked(self) -> bool:
        """Tell if a zone isn't allowed to be moved into"""
        if self.zone_type == ZoneType.BLOCKED:
            return True
        return False

    def is_priority(self) -> bool:
        """Tell if a zone is of priority status"""
        if self.zone_type == ZoneType.PRIORITY:
            return True
        return False

    def is_restricted(self) -> bool:
        """Tell if a zone is restricted, meaning its cost is higher"""
        if self.zone_type == ZoneType.RESTRICTED:
            return True
        return False

    def __repr__(self) -> str:
        return (
            "ZONE --- "
            f"Name: '{self.name}', "
            f"Coords: {self.coords}, "
            f"Zone Type: {self.zone_type}, "
            f"Color: '{self.color}', "
            f"Max drones allowed: {self.max_drones}"
        )
