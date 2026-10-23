import glob
import pytest
from parser import parser


VALID_MAPS = [
    m for m in glob.glob("maps/**/*.txt", recursive=True)
    if "invalid" not in m
]


@pytest.mark.parametrize("m", VALID_MAPS)
def test_neighbors_match_connections(m: str) -> None:
    g = parser(m)
    conn = {frozenset({c.zone_a, c.zone_b}) for c in g.connections}
    adj = {frozenset({z, n}) for z in g.zones.values() for n in z.neighbors}
    assert conn == adj
