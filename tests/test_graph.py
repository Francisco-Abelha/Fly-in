import glob
import pytest
from parser import parser


@pytest.mark.parametrize("m", glob.glob("maps/**/*.txt", recursive=True))
def test_neighbors_match_connections(m: str) -> None:
    g = parser(m)
    conn = {frozenset({c.zone_a, c.zone_b}) for c in g.connections}
    adj = {frozenset({z, n}) for z in g.zones.values() for n in z.neighbors}
    assert conn == adj
