from zone import Zone


class Connection:

    def __init__(
            self,
            zone_a: Zone,
            zone_b: Zone,
            max_link_capacity: int = 1
    ) -> None:

        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    def __repr__(self) -> str:
        return (
            "CONNECTION --- "
            f"Zone A: '{self.zone_a.name}', "
            f"Zone B: '{self.zone_b.name}', "
            f"Max Link Capacity: {self.max_link_capacity}"
        )
