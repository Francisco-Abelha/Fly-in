from drone import Drone
import abc
from typing import Iterator


class Visualizer(abc.ABC):
    """Parent visualizer class that holds the method that renders
    the per-turn interface
    """

    @abc.abstractmethod
    def show_turn(self, turn: int, moves: list[Drone]) -> None:
        """Render a single turn's moves."""
        pass

    def visualize(self, turns: Iterator[list[Drone]]) -> None:
        """Drive the visualizer, rendering each turn's moves in order."""
        for turn, moves in enumerate(turns, 1):
            self.show_turn(turn, moves)


class TerminalVisualizer(Visualizer):
    """Terminal color based visualizer that renders the graph's
    status each turn in a linear format
    """
    _ANSI = {
        "red": "\033[31m",
        "green": "\033[32m",
        "blue": "\033[34m",
        "yellow": "\033[33m",
        "cyan": "\033[36m",
        "orange": "\033[38;5;208m",
        "magenta": "\033[35m",
        "gold": "\x1b[38;5;220m",
        "brown": "\033[0;33m",
        "lime": "\033[38;5;118m"
    }
    _RESET = "\033[0m"

    def _colorize(self, drone: Drone) -> str:
        """Wrap a drone's token in the ANSI code for its zone's colour."""
        token = str(drone)
        color = drone.position.color

        if color is None:
            return token

        code = self._ANSI.get(color)
        if code is None:
            return token

        return f"{code}{token}{self._RESET}"

    def show_turn(self, turn: int, moves: list[Drone]) -> None:
        """Prints a line worth of moves made in a singular turn"""
        print_list = []
        for drone in moves:
            print_list.append(self._colorize(drone))
        print(" ".join(print_list))
