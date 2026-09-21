import os
from collections.abc import Callable

MAPS_DIR = "maps"


class Menu:
    """Create and run a menu loop with map
    difficulties and options to chose from
    """

    def __init__(
        self,
        runner: Callable[[str], None],
        maps_dir: str = MAPS_DIR,
    ) -> None:
        self.runner = runner
        self.maps_dir = maps_dir
        self.categories = self._scan_maps()

    def _scan_maps(self) -> dict[str, list[str]]:
        """Walk the maps directory and group every .txt map by its folder."""
        categories: dict[str, list[str]] = {}
        for root, _, files in os.walk(self.maps_dir):
            maps = sorted(
                os.path.join(root, name)
                for name in files
                if name.endswith(".txt")
            )
            if not maps:
                continue
            label = os.path.relpath(root, self.maps_dir)
            categories[self.maps_dir if label == "." else label] = maps
        return dict(sorted(categories.items()))

    def _select(
        self,
        title: str,
        labels: list[str],
        back_label: str | None = None,
    ) -> int | str:
        """Display numbered options, read the user input and validate it,
        re-prompting on anything invalid.

        Return the index of the chosen label, "b" to go back or "q" to quit.
        """
        while True:
            print(f"\n{title}")
            for index, label in enumerate(labels, start=1):
                print(f"  {index}. {label}")
            if back_label is not None:
                print(f"  b. {back_label}")
            print("  q. Quit")

            try:
                choice = input("Enter your choice: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return "q"

            if choice == "q":
                return "q"
            if choice == "b" and back_label is not None:
                return "b"
            if choice.isdigit() and 1 <= int(choice) <= len(labels):
                return int(choice) - 1
            print("Invalid choice. Please try again.")

    def _run_helper(self, path: str) -> None:
        """Run one map, keeping any map error from escaping the menu loop."""
        print(f"\nRunning {path}\n")
        try:
            self.runner(path)
        except (ValueError, OSError) as e:
            print(f"Error: {e}")

    def _category_loop(self, category: str) -> bool:
        """Let the user run maps of one category.

        Return True when the user asked to quit the program.
        """
        paths = self.categories[category]
        labels = [os.path.basename(path) for path in paths]
        while True:
            picked = self._select(
                f"Select a map from '{category}':",
                labels,
                back_label="Back",
            )
            if isinstance(picked, str):
                return picked == "q"
            self._run_helper(paths[picked])

    def run(self) -> None:
        """Run the menu loop, allowing the user to select and run a map."""
        if not self.categories:
            print(f"No maps found in '{self.maps_dir}'.")
            return

        names = list(self.categories)
        while True:
            picked = self._select("Select a map difficulty:", names)
            if isinstance(picked, str):
                print("Exiting the program.")
                return
            if self._category_loop(names[picked]):
                print("Exiting the program.")
                return
