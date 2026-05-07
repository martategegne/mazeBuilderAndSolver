# **Maze Generator and Solver (DFS + Backtracking)**
📌 Project Overview

This project generates and solves a randomized rectangular maze (R × C grid) using Python and Pygame.

The maze is:

Generated using Depth-First Search (DFS) with backtracking
Guaranteed to be a perfect maze (initially fully connected, no cycles)
Visually solved using a stack-based pathfinding algorithm

**A "mouse" is simulated to:**

Generate the maze by "eating walls"
Solve the maze from a random start to a random end
Display visited paths and dead ends visually
# **Features**
**Maze Generation**
Randomized DFS algorithm
Uses a stack for backtracking
Starts from the center of the grid
Ensures all cells are reachable
# ** Maze Representation**
Each cell stores wall information:

north, south, east, west walls
Walls are removed during generation to form paths

This represents the conceptual structure:

northWall[R][C]
eastWall[R][C]
# ** Maze Solving Algorithm**
Stack-based backtracking search
Random movement through valid paths
Marks:
.Current path (mouse movement)
.Dead ends
. Backtracking path
.BONUS FEATURE: Cycle Creation

To make the maze more interesting and challenging:

After generating a perfect maze,
Randomly removes extra walls with a 1 in 20 probability
This creates cycles (loops) inside the maze

# ** Effect of bonus:**

Breaks the "perfect maze" property
Makes multiple paths possible
Prevents simple wall-following solutions
# **Controls**
Key	Action
R	Reset and generate a new maze
Close window	Exit program
# **Algorithm Summary**
Maze Generation
Depth-First Search (DFS)
Stack-based backtracking
Randomized neighbor selection
Maze Solving
Backtracking search (DFS-style)
Uses visited tracking + stack
Detects dead ends
# **Data Structure Used**

Each cell contains:

north, south, east, west  # wall states
visited                   # generation tracking

This ensures:

Efficient traversal
Easy visualization
Clear wall manipulation
# **Key Concepts Demonstrated**
Graph traversal (DFS)
Backtracking algorithm
Stack usage
Randomized algorithms
Grid-based graph representation
Visualization using Pygame
# **Demonstration (Loom Video)**

The program shows:

Maze generation in real-time ("eating mouse")
Solver traversal (red dot movement)
Dead ends marked in blue
Final path discovery
# **How to Run**
pip install pygame
python maze.py
# **Project Structure**
maze-project/

│── main.py

│── README.md
# **Notes**
The maze is guaranteed to be connected.
The solver uses backtracking, not shortest path optimization.
Bonus feature introduces cycles for added complexity.
# **Author**

Built as part of a maze generation and pathfinding assignment using Python and Pygame.
##  **Student Information**

| Field      | Details            |
|------------|--------------------|
| Name       | Marta Tegegne      |
| ID         | UGR/4457/16        |
| Section    | Section-1          |
