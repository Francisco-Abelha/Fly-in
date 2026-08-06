from parser import parser
from pathfinder import Pathfinder
from zone import ZoneType
from pathlib import Path


def test_pathfinder_avoids_blocked(tmp_path: Path) -> None:
    m = tmp_path / "blocked.txt"
    m.write_text("""\
    nb_drones: 1
    start_hub: start 0 0 [color=green]
    hub: wall 1 0 [zone=blocked color=gray]
    hub: d1 1 1 [color=blue]
    hub: d2 2 1 [color=blue]
    end_hub: goal 2 0 [color=green]
    connection: start-wall
    connection: wall-goal
    connection: start-d1
    connection: d1-d2
    connection: d2-goal
    """)
    g = parser(str(m))
    path = Pathfinder(g).dijkstra()
    assert all(z.zone_type != ZoneType.BLOCKED for z in path)


def test_no_path_when_goal_only_via_blocked(tmp_path: Path) -> None:
    m = tmp_path / "trapped.txt"
    m.write_text("""\
nb_drones: 1
start_hub: start 0 0 [color=green]
hub: wall 1 0 [zone=blocked color=gray]
end_hub: goal 2 0 [color=green]
connection: start-wall
connection: wall-goal
""")
    g = parser(str(m))
    path = Pathfinder(g).dijkstra()
    assert path == []
