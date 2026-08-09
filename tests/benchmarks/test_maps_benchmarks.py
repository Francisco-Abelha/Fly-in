from typing import Callable
import pytest
from conftest import run_turns


@pytest.mark.parametrize("map_path, target", [
    ("maps/easy/01_linear_path.txt", 6),
    ("maps/easy/02_simple_fork.txt", 8),
    ("maps/easy/03_basic_capacity.txt", 6),
])
def test_easy_benchmark(run_turns: Callable[[str], int], map_path: str, target: int) -> None:
    assert run_turns(map_path) <= target


@pytest.mark.parametrize("map_path, target", [
    ("maps/medium/01_dead_end_trap.txt", 12),
    ("maps/medium/02_circular_loop.txt", 15),
    ("maps/medium/03_priority_puzzle.txt", 12),
])
def test_medium_benchmark(run_turns: Callable[[str], int], map_path: str, target: int) -> None:
    assert run_turns(map_path) <= target


@pytest.mark.parametrize("map_path, target", [
    ("maps/hard/01_maze_nightmare.txt", 30),
    ("maps/hard/02_capacity_hell.txt", 35),
    ("maps/hard/03_ultimate_challenge.txt", 45)
])
def test_hard_benchmark(run_turns: Callable[[str], int], map_path: str, target: int) -> None:
    assert run_turns(map_path) <= target
