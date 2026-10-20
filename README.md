_This project has been created as part of the 42 curriculum by fgoncal2._

# Fly-in

Route a fleet of drones through a network of zones, from a start hub to an end hub, in as few simulation turns as possible.

## Description
This program is designed to route N drones from start to end in the fewest turns possible.
It receives a map (a txt file with info about number of drones, info about its zones and connections between them)
and prints the paths taken to route all the drones.
Zones have coords, type (normal, restricted, priority, blocked), color and max number of drones allowed in it.
Connections have max_link_capacity that tells us how many drones can traverse it in any given turn.


## Instructions
- Requirements: Python 3.10+, virtual environment
- Install:  make install
- Run:      make run (opens the menu) and python3 main.py <map_file> (runs one map).
- Lint:     make lint   (optional stricter check: make lint-strict)
- Tests:    make test   (or manually: python3 -m pytest -v tests)
a single file: python3 -m pytest -v tests/test_simulation.py
- Map file format: one line for drone number, one line per zone and one line per connection

## Algorithm & implementation strategy

### 1. Pipeline

The program parses the input map files and stores info about zones, drones and connections and stores them in a graph object that represents the map's structure.
The pathfinder object runs on the graph's zones and finds the optimal path (subsequently finding other less optimal paths that can run in parallel with the main one to find the fastest program run)
Distributor then assigns those paths to the available drones, then the program will begin simulation where the drones will fly through the zones in their assigned paths, respecting the zone and connection occupancy rules.
The visualizer prints those movements and colors them according to the color data from each zone.

### 2. Finding the path: Dijkstra

Dijkstra was chosen over bfs because of zone movement costs (bfs only counts steps as a unifom number)
Priority: the distance is the pair (cost, number of non-priority zones), and pairs are compared cost first. So priority zones only break ties between routes of equal cost. The algorithm never takes a longer route just to pass through a priority zone.
Blocked zones are skipped entirely.

### 3. Multiple paths: the greedy disjoint search and the Distributor.

After each path is found, its intermediate zones are reserved and Dijkstra runs again. This repeats until no path is left. The paths share only the start and the end ("vertex-disjoint").
The Distributor gives each drone to the path with the smallest cost plus the number of drones already assigned to it. That number estimates when the drone would arrive, so the drones spread out and finish at about the same time.
On the provided maps everything goes through one shared bottleneck, so only one path exists. There the throughput comes from the simulation letting several drones share high-capacity zones and links. maps/custom/disjoint_lanes.txt demonstrates where multiple paths pay off (4 turns instead of 7).

### 4. The turn-by-turn simulation.

- Drones are processed in order, so a drone that moves out of a zone frees its spot for a drone behind it on that same turn.
- Zone capacity counts drones heading into a zone as well as drones already in it.
- Each connection lets at most max_link_capacity drones start crossing it in the same turn.
- Moving into a restricted zone reserves that zone right away, so the drone can't get stuck on the connection.
- The start and end zones have no capacity limit.
- Deadlock guard: if no drone can move during a turn, the program stops with an error instead of looping forever.
- Self-check: after every turn, every zone is checked against its max_drones and no drone may stand in a blocked zone. Any violation stops the run, so an illegal solution can never pass as a fast one.

### 5. Complexity, caching and memory

V = number of zones, E = number of connections, D = number of drones, T = number of turns, k = number of paths found.
Dijkstra with a binary heap is O((V + E) log V). The greedy search runs it about k + 1 times.
Paths are computed once, before the simulation, and never recalculated. Each drone keeps a reference to a shared Path object rather than a copy, so memory is O(V + E + D).
The simulation keeps a count of drones per zone for each turn, updated whenever a drone moves, so checking whether a zone has room is a single lookup. Drones that have arrived are no longer processed. Each turn costs O(D + V), so the whole simulation is O(T · (D + V)). With 1000 drones on capacity_hell the run went from 78 s to about 1.4 s, with exactly the same turn counts on every map.

### 6. Results

| Map | Drones | Turns | Target |
|---|---|---|---|
| easy/01_linear_path | 2 | 4 | 6 |
| easy/02_simple_fork | 4 | 6 | 8 |
| easy/03_basic_capacity | 4 | 4 | 6 |
| medium/01_dead_end_trap | 5 | 8 | 12 |
| medium/02_circular_loop | 6 | 15 | 15 |
| medium/03_priority_puzzle | 5 | 8 | 12 |
| hard/01_maze_nightmare | 8 | 13 | 30 |
| hard/02_capacity_hell | 12 | 16 | 35 |
| hard/03_ultimate_challenge | 15 | 26 | 45 |
| challenger/01_the_impossible_dream (optional) | 25 | 67 | record 45 |

Every reference target is met or beaten. The challenger map forces drones through long single-file chains of capacity-1 zones; beating 45 turns would need capacity-aware routing over overlapping paths (max-flow over time), which I chose not to implement since it is optional.


## Visual representation

The simulation is shown as colored terminal output (ANSI escape codes):

- Each move is printed in the color of the zone the drone is in, taken from the color metadata of the map. Colors without a matching terminal color are printed as plain text, so any map still works.
- One line per turn, moves separated by spaces:
  - `D<ID>-<zone>`: the drone moved into that zone.
  - `D<ID>-<from>-<to>`: the drone is on the connection towards a restricted zone and will land next turn.
  - Drones that don't move in a turn are left out of that line.
- How it helps: colors show at a glance which area of the map each drone is in, drones can be followed turn by turn, restricted transits stand out as their own token, and drones missing from a line show where they are waiting at a bottleneck.
- Running with no arguments opens a menu that lists every map by difficulty, so maps can be explored without typing paths.
- `Visualizer` is an abstract base class and `TerminalVisualizer` is one implementation of it. A graphical interface could be added as another subclass without changing the simulation.

## Example input and expected output

`maps/easy/01_linear_path.txt`:

```
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

`python3 main.py maps/easy/01_linear_path.txt` prints (shown without colors):

```
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

Zones hold one drone by default, so D2 can only leave the start once D1 has moved on. All drones are delivered in 4 turns (target: 6 or fewer).

Restricted transit and multiple paths, `maps/custom/restricted_lane_penalty.txt` (lane A is all normal, cost 3; lane B goes through the restricted zone `risky1`, cost 4):

```
D1-clear1 D4-start-risky1
D1-clear2 D2-clear1 D4-risky1
D1-goal D2-clear2 D3-clear1 D4-risky2 D5-start-risky1
D2-goal D3-clear2 D4-goal D5-risky1
D3-goal D5-risky2
D5-goal
```

The cheaper lane gets 3 drones and the restricted lane gets 2. `D4-start-risky1` is D4 spending its first turn on the connection; it lands in `risky1` on the next turn.

## Resources

- Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm, and *Introduction to Algorithms* (CLRS), chapter on single-source shortest paths
- Python heapq documentation: https://docs.python.org/3/library/heapq.html
- Vertex-disjoint paths and Menger's theorem: https://en.wikipedia.org/wiki/Menger%27s_theorem
- Maximum flow / Edmonds-Karp (the approach considered for capacity-aware routing): https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm
- ANSI escape codes: https://en.wikipedia.org/wiki/ANSI_escape_code
- PEP 8 (style), PEP 257 (docstrings), PEP 484 (type hints)
- mypy, flake8 and pytest documentation

### Use of AI

I used Claude Code (Anthropic) throughout the project as a tutor and reviewer:

- Project planning: breaking the subject into steps and checking progress against the subject and the evaluation sheet.
- Explaining concepts: Dijkstra, vertex-disjoint paths, max-flow, complexity analysis.
- Code review: reading my code and pointing out bugs and edge cases as hints, which I then fixed myself.
- Tooling: the Makefile and the test scaffolding.
- Documentation: parts of this README were written by AI from my code and then reviewed by me.

The solution code (parser, graph, pathfinding, distribution, simulation and visualizer) was written by me.
