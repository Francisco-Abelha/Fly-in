import sys
from typing import TypedDict, Any, Callable


class Config(TypedDict):
    nb_drones: int
    start_hub: tuple[str, int, int]
    hub: tuple[str, int, int]
    end_hub: tuple[str, int, int]
    connection: str

def validate_int(value: int) -> int:

    if not value:
        raise ValueError("Number of drones can't be empty")
    try:
        num: int = int(value)
    except ValueError:
        raise ValueError("Number of drones must be an integer")
    
    if num <= 0:
        raise ValueError("Number of drones must be greater than 0")
    
    return num


def parser() -> Config:

    args: int = len(sys.argv)

    if args != 2:
        raise ValueError("Map file needs to be passed as an argument")
    
    VALIDATORS: dict[str, Callable[[str], Any]] = {
        "nb_drones": validate_int,
        #"start_hub": validate_hub,
        #"hub": validate_hub,
        #"end_hub": validate_hub,
        #"connection": validate_connection,
    }
    
    config: dict[str, Any] = {}
    
    try:
        with open(sys.argv[1], "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    raise ValueError("Invalid line format")
                
                key, value = line.split(":", 1)

                if key not in VALIDATORS:
                    raise ValueError(f"Unknown key: {key}")
                
                if key in config:
                    raise ValueError(f"Duplicate key: ''{key}")
                
                config[key] = VALIDATORS[key](value)

    except FileNotFoundError:
        raise ValueError(f"File '{sys.argv[1]}' not found")
    
    validated_config: Config = {
        "nb_drones": config["nb_drones"],
        "start_hub": config["start_hub"],
        "hub": config["hub"],
        "end_hub": config["end_hub"],
        "connection": config["connection"],
    }
    
    return validated_config
    

def main() -> None:

    try:
        config: Config = parser()
        print(config.items)
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    

if __name__ == "__main__":
    main()