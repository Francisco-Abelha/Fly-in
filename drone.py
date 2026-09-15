from path import Path
from zone import Zone


class Drone:
    """Drone object with its id, path, which step it's in
    and if is in transit or in a zone
    """

    def __init__(self, drone_id: int, path: Path) -> None:
        self.drone_id = drone_id
        self.path = path
        self.step: int = 0
        self.in_transit: bool = False

    @property
    def position(self) -> Zone:
        """Returns the position of the drone"""
        return self.path.zones[self.step]

    @property
    def has_arrived(self) -> bool:
        """Tells you if the drone has arrived at the final zone"""
        return (self.step == len(self.path.zones) - 1)

    @property
    def reserved_zone(self) -> Zone:
        """Return the destination zone while in transit,
        otherwise the current position
        """
        if self.in_transit:
            return self.path.zones[self.step + 1]
        return self.position

    def next_zone(self) -> Zone | None:
        """return the next zone in the drone's path
        or None if it has arrived
        """
        if self.has_arrived:
            return None
        return self.path.zones[self.step + 1]

    def advance(self) -> None:
        """advances the drone.
        A normal zone is entered in one call.
        A restricted zone is entered in two
        — first call enters transit (connection)
        second completes the move.
        """
        to = self.next_zone()
        if to is None:
            return None
        if to.is_restricted():
            if self.in_transit:
                self.in_transit = False
                self.step += 1
            else:
                self.in_transit = True
        else:
            self.step += 1

    def __repr__(self) -> str:
        if self.in_transit:
            dest = self.path.zones[self.step + 1].name
            return f"D{self.drone_id}-{self.position.name}-{dest}"
        return f"D{self.drone_id}-{self.position.name}"
