# Constraint Satisfaction Problems (CSPs) in Python

This repository contains Python executable files for four classic Constraint Satisfaction Problems assigned in AI coursework. We utilize a central backtracking search algorithm defined in `csp.py` to solve all four problems.

## Files Structure

- `csp.py`: The core constraint satisfaction logic. It contains generic `Constraint` and `CSP` classes that handle backtracking search.
- `1_australia.py`: Map coloring problem for the principal states and territories of Australia using three colors.
- `2_telangana.py`: Map coloring problem for the districts of Telangana using four colors. It downloads an actual GeoJSON file, deduces geographical adjacencies, calculates the CSP, and generates a visual map image output (`telangana_colored_map.png`).
- `3_sudoku.py`: A Sudoku solver. It formulates a 9x9 Sudoku puzzle where constraints ensure each row, column, and 3x3 block contains unique numbers.
- `4_cryptarithmetic.py`: A solver for the well-known cryptarithmetic puzzle `TWO + TWO = FOUR`.

## Dependencies & Setup

Because modern Mac/system Python environments block global installs (PEP 668), a local virtual environment (`venv`) has been created for you containing the necessary graphing libraries (`geopandas` and `matplotlib`) needed for Problem 2.

## How to Run

Navigate to this directory in your terminal and execute the Python files using the provided virtual environment:

```bash
# Run using the python executable inside the local venv folder:
./venv/bin/python 1_australia.py
./venv/bin/python 2_telangana.py
./venv/bin/python 3_sudoku.py
./venv/bin/python 4_cryptarithmetic.py
```

- When you run `2_telangana.py`, it will dynamically download the geospatial boundary data, compute the neighbors, solve the CSP, and draw the literal colored map as an image file on your machine.
- The other scripts will calculate the results and print their solutions strictly to the console.
