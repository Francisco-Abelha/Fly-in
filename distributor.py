from drone import Drone
from path import Path


class Distributor:
    """Assign drones across the available paths to minimise total turns."""

    def __init__(self, paths: list[Path], nb_drones: int) -> None:
        self.paths = paths
        self.nb_drones = nb_drones

    def distribute(self) -> list[Drone]:
        """greedily places each drone on the path
        with the lowest resulting finish time
        (cost + drones already assigned), so shorter paths get more drones
        """
        drones: list[Drone] = []
        counters = [0] * len(self.paths)
        drone_id = 1
        for _ in range(self.nb_drones):
            argmin = min(
                range(len(self.paths)),
                key=lambda i: self.paths[i].cost + counters[i]
            )
            counters[argmin] += 1
        for i in range(len(self.paths)):
            num_drones = counters[i]
            while num_drones > 0:
                drone = Drone(drone_id, self.paths[i])
                drones.append(drone)
                num_drones -= 1
                drone_id += 1
        return drones
