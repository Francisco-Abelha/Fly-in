import sys
from parser import parser
from pathfinder import Pathfinder
from simulation import Simulation
from distributor import Distributor


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        sys.exit(1)
    try:
        graph = parser(sys.argv[1])
        print(f"drones: {graph.nb_drones}")
        for zone in graph.zones.values():
            print(zone)
        for connection in graph.connections:
            print(connection)
        print()
        print()
        finder = Pathfinder(graph)
        paths = finder.greedy_pathfinder()
        if not paths:
            print("no path found")
        else:
            nb = graph.nb_drones
            if nb is None:
                raise ValueError("no drone count")
            drones = Distributor(paths, nb).distribute()
            sim = Simulation(graph, drones)
            sim.run_simulation()
            print()
            print()
            print(f"TOTAL TURNS: {sim.turn}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
