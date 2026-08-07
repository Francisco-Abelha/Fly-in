from zone import Zone


class Path:

    def __init__(self, zones: list[Zone]) -> None:
        self.zones = zones
        self.zone_set: set[Zone] = set(self.zones)

    @property
    def cost(self) -> int:
        total_cost: int = 0
        for zone in self.zones[1:]:
            total_cost += zone.movement_cost
        return total_cost

    def __repr__(self) -> str:
        string: str = " -> ".join(z.name for z in self.zones)
        string += f"  (cost {self.cost})"
        return string
