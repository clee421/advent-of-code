import time
from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[Tuple[int, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    coords = []
    for l in lines:
        r = l.split(",")
        coords.append((int(r[0]), int(r[1])))

    return coords

def mark_grid_with_blocks(og_grid: List[List[str]], marks: List[Tuple[int, int]]) -> List[List[str]]:
    grid = og_grid.copy()
    marks_set = set(marks)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            mark = "."
            if (i, j)in marks_set:
                mark = "#"

            grid[i][j] = mark

    return grid

def solve_maze_min_steps(maze: List[List[str]],  start: Tuple[int, int], end: Tuple[int, int]) -> int:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    seen = set([start])
    queue = [(start, 0)]
    while len(queue) > 0:
        curr = queue.pop(0)
        pos, steps = curr[0], curr[1]

        if pos == end:
            return steps

        for d in directions:
            x, y = pos[0] + d[0], pos[1] + d[1]

            if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[x]):
                continue

            if maze[x][y] == "#":
                continue

            if (x, y) not in seen:
                queue.append(((x, y), steps + 1))
                seen.add((x, y))

    return -1


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    coords = parse_inputs(options.get("filepath", args[0]))

    grid_size = 71
    bytes = 1024
    if args[0] == "sample":
        grid_size = 7
        bytes = 12

    grid = []
    for _ in range(grid_size):
        r = [None] * grid_size
        grid.append(r)

    maze = mark_grid_with_blocks(grid, coords[:bytes])
    # for row in maze:
    #     print("".join(row))


    steps = solve_maze_min_steps(maze, (0, 0), (grid_size-1, grid_size-1))
    print("Steps:", steps)


def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    coords = parse_inputs(options.get("filepath", args[0]))

    grid_size = 71
    bytes = 1024
    if args[0] == "sample":
        grid_size = 7
        bytes = 12

    grid = []
    for _ in range(grid_size):
        r = [None] * grid_size
        grid.append(r)

    blocker = None

    start = time.time()
    elapsed_time = start + 5
    # I thought I might have had to do a b-search but ended up just waiting 10seconds
    for i in range(bytes, len(coords)):
        if time.time() > elapsed_time:
            now = time.time()
            elapsed_time = now + 10
            print(f"Current value: {i}. Total elapsed time {now - start}")

        maze = mark_grid_with_blocks(grid, coords[:i])
        steps = solve_maze_min_steps(maze, (0, 0), (grid_size-1, grid_size-1))

        if steps == -1:
            blocker = coords[i-1]
            break

    print("Blocker:", blocker)