# ---- Configuration ------------------------------------------------------
PYTHON := python3
MAIN   := parser.py
# Default map passed to `run` / `debug`; override on the CLI, e.g.
#   make run MAP=maps/hard/01_maze_nightmare.txt
MAP    := maps/easy/01_linear_path.txt

MYPY_FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports \
              --disallow-untyped-defs --check-untyped-defs

# ---- Targets ------------------------------------------------------------
.PHONY: install run debug clean lint lint-strict help

install:
	$(PYTHON) -m pip install flake8 mypy

run:
	$(PYTHON) $(MAIN) $(MAP)

debug:
	$(PYTHON) -m pdb $(MAIN) $(MAP)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict

help:
	@echo "Targets: install | run | debug | clean | lint | lint-strict"
	@echo "Override the map with: make run MAP=path/to/map.txt"
