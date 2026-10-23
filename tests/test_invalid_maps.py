import glob
import pytest
from parser import parser


@pytest.mark.parametrize("m", glob.glob("maps/invalid/*.txt"))
def test_invalid_map_is_rejected(m: str) -> None:
    with pytest.raises(ValueError):
        parser(m)
