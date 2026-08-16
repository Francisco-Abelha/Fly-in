from drone import Drone
from path import Path
from parser import parser
from pathfinder import Pathfinder
from simulation import Simulation
import pathlib


def test_sim_respects_capacity(tmp_path: pathlib.Path) -> None:
    m = tmp_path / "narrow.txt"
    m.write_text("""\
    nb_drones: 4
    start_hub: start 0 0
    hub: a 1 0
    hub: b 2 0
    end_hub: goal 3 0
    connection: start-a
    connection: a-b
    connection: b-goal
    """)
    g = parser(str(m))
    path = Path(Pathfinder(g).dijkstra())
    drones = [Drone(i, path) for i in range(1, (g.nb_drones or 0) + 1)]
    sim = Simulation(g, drones)

    for _ in sim.run_simulation():
        pass
    assert all(d.has_arrived for d in drones)
