from drone import Drone
from graph import Graph
import abc
from typing import Iterator


class Visualizer(abc.ABC):

    def __init__(self) -> None:
        super().__init__()

    def start(self, graph: Graph) -> None:
        pass

    @abc.abstractmethod
    def show_turn(self, turn: int, moves: list[Drone]) -> None:
        pass

    def end(self) -> None:
        pass

    def visualize(self, graph: Graph, turns: Iterator[list[Drone]]) -> None:
        self.start(graph)
        for turn, moves in enumerate(turns, 1):
            self.show_turn(turn, moves)
        self.end()


class TerminalVisualizer(Visualizer):

    _ANSI = {
        "red": "\033[31m",
        "green": "\033[32m",
        "blue": "\033[34m",
        "yellow": "\033[33m",
        # "purple": "\033[37m",
        "cyan": "\033[36m",
        "orange": "\033[38;5;208m",
        "magenta": "\033[35m",
        "gold": "\x1b[38;5;220m",
        "brown": "\033[0;33m",
        "lime": "\033[38;5;118m"
    }
    _RESET = "\033[0m"

    def __init__(self) -> None:
        super().__init__()

    def _colorize(self, drone: Drone) -> str:
        token = str(drone)
        color = drone.position.color

        if color is None:
            return token

        code = self._ANSI.get(color)
        if code is None:
            return token

        return f"{code}{token}{self._RESET}"

    def show_turn(self, turn: int, moves: list[Drone]) -> None:
        print_list = []
        for drone in moves:
            print_list.append(self._colorize(drone))
        print(" ".join(print_list))


""" class GraphicalVisualizer(Visualizer):

    def __init__(self) -> None:
        super().__init__()

    def start(self, graph: Graph) -> None:
        return super().start(graph)

    def show_turn(self, turn: int, moves: list[Drone]) -> None:
        return super().show_turn(turn, moves)

    def end(self) -> None:
        return super().end()
 """
