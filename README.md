# Maze Generator and Solver (DFS + Backtracking)
## Project Overview
#### This project generates and solves a randomized rectangular maze (R × C grid) using Python and Pygame.
The maze is:

Generated using Depth-First Search (DFS) with backtracking
Initially a perfect maze (fully connected with no cycles)
Visually solved using a stack-based pathfinding algorithm
A simulated "mouse" is used to:
Generate the maze by “eating” walls
Solve the maze from a random start to a random end
Visually display visited paths and dead ends

# Features

Maze Generation

Randomized DFS algorithm

Uses a stack for backtracking

Starts from the center of the grid

Ensures all cells are reachable (connected graph)

# Maze Representation The maze follows the assignment’s required structure using wall arrays:

northWall[i][j] → indicates top wall

eastWall[i][j] → indicates right wall

A value of 1 means the wall exists

A value of 0 means the wall is removed

Additionally, each cell conceptually has:

North, South, East, West walls

# Maze Solving Algorithm
Stack-based backtracking (DFS-style)

Moves randomly through valid paths

Tracks:

# Current path (mouse movement)

Dead ends

Backtracking path

# BONUS FEATURE: Cycle Creation

To make the maze more challenging:

After generating a perfect maze

The program randomly removes one additional wall (1 in 20 chance)

# Effect of Bonus

Introduces cycles (loops) in the maze

Breaks the perfect maze property

Creates multiple possible paths

# Bonus Demonstration: Breaking Wall-Following Rule
The project includes a wall-following solver (shoulder-to-the-wall rule):

Activated using the W key

Works correctly on perfect mazes

Fails when a cycle exists

# Why it fails

The wall-following algorithm assumes no cycles.

When cycles exist, the mouse can:

Loop infinitely

Never reach the goal

The program detects this and displays:

"LOOPING - cycle detected"

## Controls

| Key           | Action                                      |
|--------------|---------------------------------------------|
| R            | Reset and generate a new maze               |
| W            | Run wall-following solver (shoulder-to-wall rule) |
| Close Window | Exit program                                |

# Algorithm Summary

Maze Generation

Depth-First Search (DFS)

Stack-based backtracking

Random neighbor selection

# Maze Solving

Backtracking search (DFS-style)

Uses:

Stack

Visited tracking

Detects and marks dead ends



# Data Structures Used

Wall Arrays (Assignment Requirement)


northWall[][]


eastWall[][]


Cell Representation

Each cell includes:


Position (row, column)


Visited flag (for generation)



# Key Concepts Demonstrated


Graph traversal (DFS)


Backtracking algorithms


Stack data structure


Randomized algorithms


Grid-based graph modeling


Visualization using Pygame



# Demonstration (Loom Video)
The program demonstrates:


Maze generation in real-time (“eating mouse”)


Solver traversal (red mouse movement)


Dead ends marked in blue


Final path discovery


# Bonus demonstration:


Cycle creation


Wall-following failure (loop detection)



# How to Run

pip install pygame

python main.py

# Project Structure

maze-project/

|loom/link.txt

│── main.py

│── README.md

# Notes

. The maze is always connected

. The DFS solver does not guarantee shortest path

. Bonus feature introduces cycles for advanced behavior

. Wall-following algorithm demonstrates limitations in cyclic graphs


## Student Information

| Field   | Details         |
|--------|-----------------|
| Name   | Marta Tegegne   |
| ID     | UGR/4457/16     |
| Section| Section-1       |

