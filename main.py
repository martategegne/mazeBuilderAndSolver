import pygame
import random
import time

#  CONFIGURATION 
# Maze dimensions
ROWS = 20
COLS = 20
CELL_SIZE = 25

# Screen size
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 60  # extra space for stats display
FPS = 60

# COLORS 
WHITE = (255, 255, 255)      # Background
BLACK = (0, 0, 0)            # Walls
RED = (255, 0, 0)            # Mouse (solver)
BLUE = (0, 0, 255)           # Dead-end cells
GREEN = (0, 200, 0)          # Start cell
GOLD = (255, 215, 0)         # End cell
LIGHT_RED = (255, 60, 60)    # Visited cells
LIGHT_BLUE = (150, 150, 255) # Current path

# ---------------- WALL ARRAYS (Assignment Spec) ----------------
# Wall integrity:
# - If northwall[i][j] is 1, the (i,j) cell has a solid upper wall; otherwise the wall is missing.
#
# The bottom edge:
# - The zeroth row (i == 0) is a phantom row of cells below the maze whose north walls make up
#   the bottom edge of the maze.
#
# The left edge:
# - eastwall[i][0] specifies where any gaps appear in the left edge of the maze.
#
# Mapping to this program's grid:
# - Grid uses 0-based (r: 0..ROWS-1, c: 0..COLS-1), with r increasing downward on screen.
# - Assignment uses (i: 1..ROWS, j: 1..COLS) for real cells and a phantom row i == 0 below.
#   We map: i = ROWS - r, j = c + 1
#
# Dimensions used here:
# - northwall: (ROWS+1) x (COLS+1)  (j==0 unused)
# - eastwall : (ROWS+1) x (COLS+1)  (i==0 unused; j==0 is phantom-left edge)
northwall = None
eastwall = None

def init_walls():
    global northwall, eastwall
    northwall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
    eastwall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]

def _ij_from_cell(cell):
    i = ROWS - cell.r
    j = cell.c + 1
    return i, j

def has_north(cell):
    i, j = _ij_from_cell(cell)
    return northwall[i][j] == 1

def has_south(cell):
    i, j = _ij_from_cell(cell)
    return northwall[i - 1][j] == 1

def has_east(cell):
    i, j = _ij_from_cell(cell)
    return eastwall[i][j] == 1

def has_west(cell):
    i, j = _ij_from_cell(cell)
    return eastwall[i][j - 1] == 1

def remove_wall_between(a, b):
    """Remove the single wall shared by two orthogonally-adjacent cells."""
    dr = a.r - b.r
    dc = a.c - b.c
    if dr == 1:        # b is north of a
        ia, ja = _ij_from_cell(a)
        northwall[ia][ja] = 0
    elif dr == -1:     # b is south of a
        ia, ja = _ij_from_cell(a)
        northwall[ia - 1][ja] = 0
    elif dc == 1:      # b is west of a
        ia, ja = _ij_from_cell(a)
        eastwall[ia][ja - 1] = 0
    elif dc == -1:     # b is east of a
        ia, ja = _ij_from_cell(a)
        eastwall[ia][ja] = 0
#the bonus question is solved here
def maybe_create_cycle(grid, chance_n=20):
    """
    Bonus: with probability 1/chance_n, remove one additional random wall to create a cycle.
    Returns True if a cycle was created, else False.
    """
    if chance_n <= 0:
        return False
    if random.randrange(chance_n) != 0:
        return False

    # Collect candidate adjacent pairs that still have a wall between them.
    candidates = []
    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]
            if c < COLS - 1:
                right = grid[r][c + 1]
                if has_east(cell):  # wall between cell and right
                    candidates.append((cell, right))
            if r < ROWS - 1:
                down = grid[r + 1][c]
                if has_south(cell):  # wall between cell and down
                    candidates.append((cell, down))

    if not candidates:
        return False

    a, b = random.choice(candidates)
    remove_wall_between(a, b)
    return True

#  CELL CLASS 
# Each cell represents a single grid unit in the maze.
# It stores wall information and visitation state.
class Cell:
    def __init__(self, r, c):
        self.r = r  # Row index
        self.c = c  # Column index

        # Used during maze generation
        self.visited = False


#  GRID CREATION 
# Creates a ROWS x COLS grid of cells
def create_grid():
    return [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]


#  NEIGHBOR DETECTION 
# Returns unvisited neighboring cells (used in DFS generation)
def get_neighbors(grid, cell):
    neighbors = []
    r, c = cell.r, cell.c

    if r > 0 and not grid[r-1][c].visited:
        neighbors.append(grid[r-1][c])
    if r < ROWS-1 and not grid[r+1][c].visited:
        neighbors.append(grid[r+1][c])
    if c > 0 and not grid[r][c-1].visited:
        neighbors.append(grid[r][c-1])
    if c < COLS-1 and not grid[r][c+1].visited:
        neighbors.append(grid[r][c+1])

    return neighbors


# WALL REMOVAL 
# Removes the wall between two adjacent cells
def remove_walls(a, b):
    remove_wall_between(a, b)


# MAZE GENERATION (DFS + STACK) 
# Implements the "mouse eating walls" algorithm using Depth-First Search
def generate_maze(grid, screen, clock):
    stack = []

    # Start from center cell (arbitrary choice)
    current = grid[ROWS//2][COLS//2]
    current.visited = True

    while True:
        clock.tick(FPS)

        # Get all unvisited neighbors
        neighbors = get_neighbors(grid, current)

        # Draw current state of maze
        draw(grid, screen)

        # Highlight current "mouse" position
        pygame.draw.rect(screen, LIGHT_RED,
            (current.c * CELL_SIZE, current.r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

        if neighbors:
            # Choose a random neighbor
            nxt = random.choice(neighbors)

            # Push current cell to stack (for backtracking)
            stack.append(current)

            # Remove wall between current and chosen cell
            remove_walls(current, nxt)

            nxt.visited = True
            current = nxt

        elif stack:
            # Dead-end reached → backtrack
            current = stack.pop()
        else:
            # All cells visited → maze complete
            break


def solve_wall_follower(grid, start, end, screen, clock, font, prefer="right"):
    """
    Shoulder-to-the-wall solver (wall follower).
    Works reliably on simply-connected (perfect) mazes, but can loop with cycles.
    Press R to reset/exit.
    """
    # Directions in screen coords: 0=N,1=E,2=S,3=W
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def can_move(cell, d):
        r, c = cell.r, cell.c
        if d == 0:
            return (r > 0) and (not has_north(cell))
        if d == 1:
            return (c < COLS - 1) and (not has_east(cell))
        if d == 2:
            return (r < ROWS - 1) and (not has_south(cell))
        return (c > 0) and (not has_west(cell))

    def step(cell, d):
        dr, dc = dirs[d]
        return grid[cell.r + dr][cell.c + dc]

    # pick an initial facing that has an open move if possible
    facing = 0
    for d in range(4):
        if can_move(start, d):
            facing = d
            break

    visited = set()
    path = [start]
    current = start
    start_time = time.time()
    steps = 0

    # (cell, facing) repeats => we're looping
    seen_state = set()

    # Right-hand rule: try right, forward, left, back
    if prefer == "left":
        order = [-1, 0, 1, 2]
    else:
        order = [1, 0, -1, 2]

    looping = False
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

        if current == end:
            break

        state = (current.r, current.c, facing)
        if state in seen_state:
            looping = True
            # Keep showing the loop for a bit, but don't run forever.
            if steps > 800:
                break
        else:
            seen_state.add(state)

        # pick next direction based on wall-following preference
        moved = False
        for rel in order:
            nd = (facing + rel) % 4
            if can_move(current, nd):
                facing = nd
                current = step(current, facing)
                path.append(current)
                moved = True
                break

        if not moved:
            # Shouldn't happen in a valid maze, but keep safe.
            break

        visited.add((current.r, current.c))
        steps += 1

        draw(grid, screen)
        for cell in path[-200:]:
            pygame.draw.rect(screen, LIGHT_BLUE,
                (cell.c * CELL_SIZE, cell.r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        draw_mouse(screen,
            current.c * CELL_SIZE + CELL_SIZE//2,
            current.r * CELL_SIZE + CELL_SIZE//2)

        elapsed = round(time.time() - start_time, 2)
        status = "WALL FOLLOWER"
        if looping:
            status += " (LOOPING - cycle detected)"
        text = font.render(f"{status}   Steps: {steps}   Time: {elapsed}s", True, BLACK)
        screen.blit(text, (10, HEIGHT - 50))
        pygame.display.flip()

    # final frame
    while True:
        clock.tick(FPS)
        draw(grid, screen)
        for cell in path[-200:]:
            pygame.draw.rect(screen, LIGHT_BLUE,
                (cell.c * CELL_SIZE, cell.r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, GOLD,
            (end.c * CELL_SIZE + CELL_SIZE//2, end.r * CELL_SIZE + CELL_SIZE//2), 7)
        pygame.draw.circle(screen, GREEN,
            (start.c * CELL_SIZE + CELL_SIZE//2, start.r * CELL_SIZE + CELL_SIZE//2), 7)
        if looping:
            text = font.render("Wall follower looped due to a cycle. Press R to reset.", True, BLACK)
            screen.blit(text, (10, HEIGHT - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return


# VALID MOVES FOR SOLVER 
# Returns reachable neighboring cells (no walls)
def get_moves(grid, cell):
    r, c = cell.r, cell.c
    moves = []

    if not has_north(cell) and r > 0:
        moves.append(grid[r-1][c])
    if not has_south(cell) and r < ROWS-1:
        moves.append(grid[r+1][c])
    if not has_west(cell) and c > 0:
        moves.append(grid[r][c-1])
    if not has_east(cell) and c < COLS-1:
        moves.append(grid[r][c+1])

    return moves


# MAZE SOLVER (BACKTRACKING) 
# Simulates a "mouse" finding a path using DFS
def solve_maze(grid, start, end, screen, clock, font):
    stack = [start]       # Path stack
    visited = set()       # Visited cells
    dead_ends = set()     # Dead-end cells

    steps = 0
    start_time = time.time()
    solved = False

    while stack:
        clock.tick(FPS)

        # Handle user input (reset or exit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

        current = stack[-1]
        visited.add((current.r, current.c))
        steps += 1

        draw(grid, screen)

        # Draw visited cells (red)
        for r, c in visited:
            pygame.draw.rect(screen, LIGHT_RED,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw dead-end cells (blue)
        for r, c in dead_ends:
            pygame.draw.rect(screen, BLUE,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw current path (light blue)
        for cell in stack:
            pygame.draw.rect(screen, LIGHT_BLUE,
                (cell.c * CELL_SIZE, cell.r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw mouse
        draw_mouse(screen,
            current.c * CELL_SIZE + CELL_SIZE//2,
            current.r * CELL_SIZE + CELL_SIZE//2)

        # Display stats
        elapsed = round(time.time() - start_time, 2)
        text = font.render(f"Steps: {steps}   Time: {elapsed}s", True, BLACK)
        screen.blit(text, (10, HEIGHT - 50))

        pygame.display.flip()

        # Check if goal reached
        if current == end:
            solved = True
            break

        # Get valid next moves
        moves = [m for m in get_moves(grid, current)
                 if (m.r, m.c) not in visited]

        if moves:
            # Move forward
            stack.append(random.choice(moves))
        else:
            # Dead end → mark and backtrack
            dead_ends.add((current.r, current.c))
            stack.pop()

    # Keep displaying final solution
    while solved:
        clock.tick(FPS)
        draw(grid, screen)

        for r, c in visited:
            pygame.draw.rect(screen, LIGHT_RED,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for r, c in dead_ends:
            pygame.draw.rect(screen, BLUE,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw start and end points
        pygame.draw.circle(screen, GOLD,
            (end.c * CELL_SIZE + CELL_SIZE//2, end.r * CELL_SIZE + CELL_SIZE//2), 7)
        pygame.draw.circle(screen, GREEN,
            (start.c * CELL_SIZE + CELL_SIZE//2, start.r * CELL_SIZE + CELL_SIZE//2), 7)

        pygame.display.flip()

        # Allow reset
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return


#  DRAW MAZE 
# Draws grid and walls
def draw(grid, screen):
    screen.fill(WHITE)

    for row in grid:
        for cell in row:
            x = cell.c * CELL_SIZE
            y = cell.r * CELL_SIZE

            if has_north(cell):
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
            if has_east(cell):
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y),
                                  (x + CELL_SIZE, y + CELL_SIZE), 2)
            if has_south(cell):
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE),
                                  (x + CELL_SIZE, y + CELL_SIZE), 2)
            if has_west(cell):
                pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 2)


#  DRAW MOUSE 
# Simple visual representation of the solver
def draw_mouse(screen, x, y):
    pygame.draw.ellipse(screen, RED, (x-7, y-5, 14, 10))
    pygame.draw.circle(screen, RED, (x+7, y), 5)
    pygame.draw.circle(screen, BLACK, (x+9, y-2), 2)
    pygame.draw.circle(screen, RED, (x+10, y-5), 2)
    pygame.draw.line(screen, RED, (x-7, y), (x-13, y-2), 2)
    pygame.draw.circle(screen, RED, (x+6, y), 4)
    pygame.draw.circle(screen, BLACK, (x+7, y-1), 1)
    pygame.draw.line(screen, RED, (x-6, y), (x-10, y), 2)


# ---------------- RESET MAZE ----------------
# Generates new maze with entrance on left edge and exit on right edge
def reset_maze(screen, clock, font):
    init_walls()
    grid = create_grid()
    generate_maze(grid, screen, clock)
    #BONUS TRIGGERED HERE
    cycle_created = maybe_create_cycle(grid, chance_n=20)

    # Entrance: opening on the left boundary (column 0)
    start_r = random.randrange(ROWS)
    start = grid[start_r][0]

    # Exit: opening on the right boundary (column COLS-1)
    end_r = random.randrange(ROWS)
    end = grid[end_r][COLS - 1]

    # Create the actual boundary gaps per the addendum's wall-array structure:
    # - Left edge gaps are controlled by eastwall[i][0] (phantom column)
    # - Right edge gaps are controlled by eastwall[i][COLS] (outer boundary)
    si, _ = _ij_from_cell(start)
    ei, _ = _ij_from_cell(end)
    eastwall[si][0] = 0
    eastwall[ei][COLS] = 0

    return grid, start, end, cycle_created


#  MAIN PROGRAM 
def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    # Initialize maze
    grid, start, end, cycle_created = reset_maze(screen, clock, font)

    running = True
    solved = False

    while running:
        clock.tick(FPS)

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid, start, end, cycle_created = reset_maze(screen, clock, font)
                    solved = False
                if event.key == pygame.K_w:
                    # Demonstrate shoulder-to-the-wall rule (wall follower).
                    solve_wall_follower(grid, start, end, screen, clock, font, prefer="right")

        # Draw maze and endpoints
        draw(grid, screen)

        pygame.draw.circle(screen, GREEN,
            (start.c * CELL_SIZE + CELL_SIZE//2, start.r * CELL_SIZE + CELL_SIZE//2), 7)
        pygame.draw.circle(screen, GOLD,
            (end.c * CELL_SIZE + CELL_SIZE//2, end.r * CELL_SIZE + CELL_SIZE//2), 7)

        hint = "Press W: wall follower (shoulder-to-wall)"
        if cycle_created:
            hint += "   BONUS: cycle created (1-in-20)"
        text = font.render(hint, True, BLACK)
        screen.blit(text, (10, HEIGHT - 50))

        pygame.display.flip()

        # Run solver once
        if not solved:
            pygame.time.delay(300)
            solve_maze(grid, start, end, screen, clock, font)
            solved = True

    pygame.quit()


if __name__ == "__main__":
    main()