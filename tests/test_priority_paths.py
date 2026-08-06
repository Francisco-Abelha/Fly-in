from parser import parser
from pathlib import Path
from pathfinder import Pathfinder


def test_pathfinder_prefers_priority(tmp_path: Path) -> None:
    m = tmp_path / "priority.txt"
    m.write_text("""\
    nb_drones: 1
    start_hub: start 0 0 [color=green]
    hub: p1 1 1 [zone=priority color=blue]
    hub: p2 2 1 [zone=priority color=blue]
    hub: n1 1 -1 [color=orange]
    hub: n2 2 -1 [color=orange]
    end_hub: goal 3 0 [color=green]
    connection: start-p1
    connection: p1-p2
    connection: p2-goal
    connection: start-n1
    connection: n1-n2
    connection: n2-goal
    """)
    g = parser(str(m))
    names = [z.name for z in Pathfinder(g).dijkstra()]
    assert "p1" in names and "p2" in names
