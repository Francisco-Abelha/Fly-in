import sys
from parser import parser


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
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
