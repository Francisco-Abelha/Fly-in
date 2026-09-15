from zone import Zone


class Connection:
    """Represents a connection between two zones.
    Carries max_link_capacity so zone occupancy rules are respected.
    """

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
        """Return a human-readable representation of the connection."""
        return (
            "CONNECTION --- "
            f"Zone A: '{self.zone_a.name}', "
            f"Zone B: '{self.zone_b.name}', "
            f"Max Link Capacity: {self.max_link_capacity}"
        )
