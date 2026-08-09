import sys
from parser import parser
from pathfinder import Pathfinder
from path import Path
from drone import Drone
from simulation import Simulation


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
        path_list = finder.dijkstra()
        if not path_list:
            print("no path found")
        else:
            path = Path(path_list)
            drones = [
                Drone(i, path) for i in range(1, (graph.nb_drones or 0) + 1)
            ]
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
