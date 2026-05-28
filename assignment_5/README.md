# AI Algorithms and Models - Assignment 5

This repository contains implementations of various Artificial Intelligence systems, spanning probabilistic graphical models, adversarial search algorithms, and knowledge-based expert systems. 

## Project Structure

The project contains the following core scripts:
* **bayesian_network.py**: Probabilistic graphical model representing the classic Alarm Network using pgmpy.
* **search_algorithms.py**: Implementation of tree search algorithms (Minimax, Alpha-Beta, Heuristic Alpha-Beta, MCTS) in a Tic-Tac-Toe environment.
* **travel_planner.py**: A rule-based expert travel system utilising local knowledge bases to construct personalised travel itineraries.

---

## Setup and Installation

A virtual environment is provided in the repository directory. To get started, follow these instructions.

### 1. Activate the Virtual Environment
On macOS or Linux, run the following command in your terminal from the project root:
```bash
source .venv/bin/activate
```

### 2. Install Dependencies
Only the Bayesian Network implementation requires external libraries. Install the dependencies using pip:
```bash
pip install pgmpy
```

---

## Script Overviews and Usage

### 1. Bayesian Network Inference (bayesian_network.py)

This module implements Judea Pearl's classic Alarm Network using the `pgmpy` package. It defines five binary variables (0 = False, 1 = True):
* **Burglary**: Direct cause of Alarm.
* **Earthquake**: Direct cause of Alarm.
* **Alarm**: Triggers phone calls from John and Mary.
* **JohnCalls**: Observation dependent on Alarm.
* **MaryCalls**: Observation dependent on Alarm.

#### How to Run
```bash
python3 bayesian_network.py
```

#### What It Evaluates
* **Causal and Diagnostic Queries**: Calculates probabilities such as the likelihood of a burglary given that both neighbours call.
* **Explaining Away**: Demonstrates Berkson's Paradox, showing how the probability of an earthquake decreases when we know a burglary has already occurred to explain the active alarm.

---

### 2. Game Playing Search Algorithms (search_algorithms.py)

This module implements key game-playing search algorithms applied to the game of Tic-Tac-Toe:
* **Minimax**: Complete depth-first search that guarantees optimal moves by traversing the full game tree.
* **Alpha-Beta Pruning**: An optimised version of Minimax that cuts off branches that cannot affect the final decision, reducing search time.
* **Heuristic Alpha-Beta**: Evaluates non-terminal states using a custom static evaluation function when the search depth limit is reached.
* **Monte Carlo Tree Search (MCTS)**: Uses selection (UCB1), expansion, rollout/simulation, and backpropagation to find near-optimal moves.

#### How to Run
```bash
python3 search_algorithms.py
```

#### Test Scenarios Evaluated
* **Immediate Win**: A board state where player X can win immediately by selecting index 2.
* **Blocking Move**: A board state where player X must block player O from winning on the next turn by selecting index 5.

---

### 3. Knowledge-Based AI Travel Planner (travel_planner.py)

This module demonstrates a mock knowledge-based system designed to plan a holiday itinerary. It utilises local data dictionaries (Knowledge Bases) representing:
* **Wine Preferences**: Red, white, and sparkling wine pairings.
* **Destinations**: Places matching specific themes (Adventure, Culture, Relaxation).
* **Food Specialties**: Culinary recommendations mapped from places to countries.
* **Estimated Costs**: Cost of travel to each location.

#### How to Run
```bash
python3 travel_planner.py
```

#### Simulated User Profiles
* **Alice** (Culture, Red Wine, Budget: $2500): Validates destination filtering and pairing recommendations.
* **Bob** (Relaxation & Adventure, Sparkling Wine, Budget: $6000): Validates high-budget multi-interest recommendations.
* **Charlie** (Adventure, Budget: $1000): Demonstrates graceful handling of constraint violations (budget too low).
