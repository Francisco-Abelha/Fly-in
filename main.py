import sys
from parser import parser
from pathfinder import Pathfinder
from simulation import Simulation
from distributor import Distributor
from visualizer import TerminalVisualizer
from menu import Menu


def run_one_map(map_file: str) -> None:
    """Access the map file, parse and validate it. Build a graph,
    and simulate the drone pathfinding and movement logic
    while rendering a visualization
    """
    graph = parser(map_file)
    finder = Pathfinder(graph)
    paths = finder.greedy_pathfinder()
    if not paths:
        print("no path found")
        return
    nb = graph.nb_drones
    if nb is None:
        raise ValueError("no drone count")
    drones = Distributor(paths, nb).distribute()
    sim = Simulation(graph, drones)
    drone_list = sim.run_simulation()
    viz = TerminalVisualizer()
    viz.visualize(drone_list)


def main() -> None:
    """Central method for this program, reads the arguments and either
    runs the given map or opens the menu loop when none is given
    """
    if len(sys.argv) == 1:
        # if no arguments are provided then run the map option loop
        menu = Menu(run_one_map)
        menu.run()
    elif len(sys.argv) == 2:
        try:
            run_one_map(sys.argv[1])
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python main.py <map_file>")
        sys.exit(1)


if __name__ == "__main__":
    main()
