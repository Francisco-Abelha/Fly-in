from path import Path
from zone import Zone


class Drone:

    def __init__(self, drone_id: int, path: Path) -> None:
        self.drone_id = drone_id
        self.path = path
        self.step: int = 0

    @property
    def position(self) -> Zone:
        return self.path.zones[self.step]

    @property
    def has_arrived(self) -> bool:
        return (self.step == len(self.path.zones) - 1)

    def next_zone(self) -> Zone | None:
        if self.has_arrived:
            return None
        return self.path.zones[self.step + 1]

    def advance(self) -> None:
        self.step += 1

    def __repr__(self) -> str:
        return f"D{self.drone_id}-{self.position.name}"
