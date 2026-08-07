from path import Path
from zone import Zone, ZoneType


def test_path_cost_and_set() -> None:
    a = Zone("a", 0, 0)
    r = Zone("r", 1, 0, ZoneType.RESTRICTED)
    g = Zone("g", 2, 0)
    p = Path([a, r, g])
    assert p.cost == 3
    assert p.zone_set == {a, r, g}
