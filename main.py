import sys
from parser import parser
from pathfinder import Pathfinder


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
        path = Pathfinder(graph)
        shortest_path = path.bfs()
        for element in shortest_path:
            print(element.name)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
