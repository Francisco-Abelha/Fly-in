import sys
from typing import Callable
from graph import Graph
from zone import Zone, ZoneType
from connection import Connection


Handler = Callable[[str, Graph], None]


def validate_int(value: str) -> int:

    if not value:
        raise ValueError("Number of drones can't be empty")
    try:
        num: int = int(value)
    except ValueError:
        raise ValueError("Number of drones must be an integer")

    if num <= 0:
        raise ValueError("Number of drones must be greater than 0")

    return num


def parse_nb_drones(value: str, graph: Graph) -> None:
    if graph.nb_drones is not None:
        raise ValueError("nb_drones defined twice")
    graph.nb_drones = validate_int(value)


def split_metadata(value: str) -> tuple[str, dict[str, str]]:
    if "[" not in value:
        return value, {}
    fixed, _, rest = value.partition("[")
    if not rest.endswith("]"):
        raise ValueError("malformed metadata bracket")
    meta: dict[str, str] = {}
    rest = rest.removesuffix("]")
    split: list = rest.split(" ")
    for element in split:
        k, v = element.split("=")
        meta[k] = v
    return fixed, meta


def parse_zone(value: str) -> Zone:
    fixed, meta = split_metadata(value)
    parts = fixed.split()
    if len(parts) != 3:
        raise ValueError(f"Zone needs 'name x y', got: {fixed}")
    name, x_str, y_str = parts
    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError:
        print("Coords need to be integers")

    zone_type = ZoneType(meta.get("zone", "normal"))
    color = meta.get("color")
    max_drones = validate_int(meta.get("max_drones", "1"))

    return Zone(name, x, y, zone_type, color, max_drones)


def parse_hub(value: str, graph: Graph) -> None:
    graph.add_zone(parse_zone(value))


def parse_start(value: str, graph: Graph) -> None:
    if graph.start is not None:
        raise ValueError("Multiple starting points!!")
    zone = parse_zone(value)
    graph.start = zone
    graph.add_zone(zone)


def parse_end(value: str, graph: Graph) -> None:
    if graph.end is not None:
        raise ValueError("Multiple ending points!!")
    zone = parse_zone(value)
    graph.end = zone
    graph.add_zone(zone)


def parse_connection(value: str, graph: Graph) -> None:
    fixed, meta = split_metadata(value)
    parts = fixed.strip().split("-")
    if len(parts) != 2:
        raise ValueError(f"Connection needs 'hub_a - hub_b', got: {fixed}")

    zone_a_name, zone_b_name = parts
    zone_a = graph.zones.get(zone_a_name)
    zone_b = graph.zones.get(zone_b_name)
    if zone_a is None or zone_b is None:
        raise ValueError(
            "Unknown zone in connection: "
            f"{zone_a_name}, {zone_b_name}"
        )

    max_link = validate_int(meta.get("max_link_capacity", "1"))
    graph.add_connection(Connection(zone_a, zone_b, max_link))


def parser() -> Graph:

    if len(sys.argv) != 2:
        raise ValueError("Map file needs to be passed as an argument")

    graph = Graph()
    HANDLERS: dict[str, Handler] = {
        "nb_drones": parse_nb_drones,
        "start_hub": parse_start,
        "hub": parse_hub,
        "end_hub": parse_end,
        "connection": parse_connection,
    }

    try:
        with open(sys.argv[1]) as file:
            for n, raw in enumerate(file, start=1):

                line = raw.strip()

                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    raise ValueError(f"Line {n}: invalid format")

                key, value = line.split(":", 1)

                if key not in HANDLERS:
                    raise ValueError(f"Line {n}: unknown key '{key}'")

                HANDLERS[key](value.strip(), graph)

    except FileNotFoundError:
        raise ValueError(f"File '{sys.argv[1]}' not found")

    return graph


def main() -> None:

    try:
        graph = parser()
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
