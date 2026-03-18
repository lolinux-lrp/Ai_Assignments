# Assignment 2

This folder contains implementations for basic search algorithms and a simple CAPTCHA generation project.

## Contents

### 1. searches/
Contains C++ implementations of classic graph search algorithms and state-space search problems.
- `bfs.cpp`: Implementation of the Breadth-First Search algorithm.
- `dfs.cpp`: Implementation of the Depth-First Search algorithm.
- `missionary_pb_bfs.cpp`: Solution to the classic Missionaries and Cannibals problem using Breadth-First Search.
- `missionary_pb_dfs.cpp`: Solution to the classic Missionaries and Cannibals problem using Depth-First Search.

### 2. simple_captcha_project/
Contains a Python-based project for generating CAPTCHAs.
- `simple_captcha.py`: A Python script that creates basic CAPTCHAs (including text and math-based challenges) and saves them as images (e.g., `captcha.png`).

## How to Run

### C++ Programs
To compile and run any of the C++ files in the `searches` directory, use a C++ compiler like `g++` or `clang++`:

```bash
cd searches
g++ bfs.cpp -o bfs
./bfs
```
*(Replace `bfs.cpp` and `bfs` with the name of the file you want to compile and run).*

### Python CAPTCHA Generator
To run the CAPTCHA generator in the `simple_captcha_project` directory, make sure you have Python 3 installed, along with any required modules (like `Pillow` if it generates images).

```bash
cd simple_captcha_project
python3 simple_captcha.py
```
