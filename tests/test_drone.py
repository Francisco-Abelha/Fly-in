from zone import Zone
from drone import Drone
from path import Path


def test_drone_walks_its_path() -> None:
    a = Zone("a", 0, 0)
    b = Zone("b", 1, 0)
    g = Zone("g", 2, 0)
    d = Drone(1, Path([a, b, g]))

    assert d.position is a
    assert d.has_arrived is False
    assert d.next_zone() is b

    d.advance()
    assert d.position is b
    assert d.next_zone() is g
    assert d.has_arrived is False

    d.advance()
    assert d.position is g
    assert d.has_arrived is True
    assert d.next_zone() is None
