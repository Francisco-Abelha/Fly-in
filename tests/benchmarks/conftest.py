import pytest
from parser import parser
from path import Path
from pathfinder import Pathfinder
from drone import Drone
from simulation import Simulation


@pytest.fixture
def run_turns():
    def _run(map_path: str) -> int:
        g = parser(map_path)
        path = Path(Pathfinder(g).dijkstra())
        drones = [Drone(i, path) for i in range(1, (g.nb_drones or 0) + 1)]
        sim = Simulation(g, drones)
        sim.run_simulation()
        return sim.turn
    return _run
