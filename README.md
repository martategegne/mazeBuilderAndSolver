# Maze Generator and Solver (DFS + Backtracking)
## Project Overview
#### This project generates and solves a randomized rectangular maze (R × C grid) using Python and Pygame.
The maze is:

**Maze Property (Perfect Maze + Optional Cycles)**

The maze is initially generated as a perfect maze using Depth-First Search (DFS), meaning:

Every cell is reachable
There is exactly one unique path between any two cells
No cycles exist in the base generation

**However**, to increase difficulty, a bonus feature randomly introduces cycles by removing additional walls (1 in 20 chance).
This means the final displayed maze may no longer strictly remain a perfect maze, but the underlying generation process is still DFS-based and correct.

## Start and End Position

The maze is constructed according to the assignment requirement:

Start cell: randomly selected from the left edge of the maze (column 0)

End cell: randomly selected from the right edge of the maze (last column)

This ensures that every maze run begins on the left boundary and finishes on the right boundary, matching the required specification.

## Features

Maze Generation

Randomized DFS algorithm

Uses a stack for backtracking

Starts from the center of the grid

Ensures all cells are reachable (connected graph)

## Maze Representation The maze follows the assignment’s required structure using wall arrays:

northWall[i][j] → indicates top wall

eastWall[i][j] → indicates right wall

A value of 1 means the wall exists

A value of 0 means the wall is removed

Additionally, each cell conceptually has:

North, South, East, West walls

## Maze Solving Algorithm
Stack-based backtracking (DFS-style)

Moves randomly through valid paths

Tracks:

## Current path (mouse movement)

Dead ends

Backtracking path

## BONUS FEATURE: Cycle Creation

To make the maze more challenging:

After generating a perfect maze

The program randomly removes one additional wall (1 in 20 chance)

## Effect of Bonus

Introduces cycles (loops) in the maze

Breaks the perfect maze property

Creates multiple possible paths

## Bonus Demonstration: Breaking Wall-Following Rule

**This feature is implemented as an optional enhancement and does not affect the correctness of the initial perfect maze generation phase.**

The project includes a wall-following solver (shoulder-to-the-wall rule):

Activated using the W key

Works correctly on perfect mazes

Fails when a cycle exists

## Why it fails

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
| W            | Runs wall-following (shoulder-to-wall) solver to demonstrate behavior in both perfect and cyclic mazes |
| Close Window | Exit program                                |

## Algorithm Summary

Maze Generation

Depth-First Search (DFS)

Stack-based backtracking

Random neighbor selection

## Maze Solving

Backtracking search (DFS-style)

Uses:

Stack

Visited tracking

Detects and marks dead ends



## Data Structures Used

Wall Arrays (Assignment Requirement)


northWall[][]


eastWall[][]


Cell Representation

Each cell includes:


Position (row, column)


Visited flag (for generation)



## Key Concepts Demonstrated


Graph traversal (DFS)


Backtracking algorithms


Stack data structure


Randomized algorithms


Grid-based graph modeling


Visualization using Pygame



## Demonstration (Loom Video)
The program demonstrates:


Maze generation in real-time (“eating mouse”)


Solver traversal (red mouse movement)


Dead ends marked in blue


Final path discovery


## Bonus demonstration:

Cycle creation

Wall-following failure (loop detection)

## Queue vs Stack in Maze Generation

The maze generation algorithm in this project uses a **stack**, implementing a Depth-First Search (DFS) approach. This method explores one path as far as possible before backtracking, resulting in long, deep, and winding paths. Such mazes tend to look more complex and “twisty,” which makes them visually interesting and challenging.

If a **queue** were used instead (Breadth-First Search, BFS):

- The maze would be generated level by level rather than depth-first
- 
- Paths would be shorter and more evenly distributed
- 
- The maze would appear more uniform and less complex  

Therefore, a **stack-based DFS approach** is preferred for this project, as it produces more complex, irregular mazes that better satisfy the assignment requirement for a challenging and fully connected grid structure.

## How to Run

pip install pygame

python main.py

## Project Structure

maze-project/

|loom/link.txt

│── main.py

│── README.md

## Notes

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

