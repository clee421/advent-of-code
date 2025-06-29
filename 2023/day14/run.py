from typing import Dict, List
from copy import deepcopy

def parse_inputs(filepath: str) -> List[List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for l in lines:
        grid.append(list(l))

    return grid

def tilt_north(grid: List[List[str]]) -> List[List[str]]:
    for i in range(1, len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "O" and i - 1 >= 0:
                curr = i
                above = i - 1
                while above >= 0:
                    if grid[above][j] == ".":
                        grid[curr][j], grid[above][j] = grid[above][j], grid[curr][j]
                    else:
                        break

                    curr = above
                    above -= 1

    return grid

def tilt_south(grid: List[List[str]]) -> List[List[str]]:
    for i in range(len(grid) - 2, -1, -1):
        for j in range(len(grid[i])):
            if grid[i][j] == "O" and i + 1 < len(grid):
                curr = i
                below = i + 1
                while below < len(grid):
                    if grid[below][j] == ".":
                        grid[curr][j], grid[below][j] = grid[below][j], grid[curr][j]
                    else:
                        break

                    curr = below
                    below += 1

    return grid

def tilt_west(grid: List[List[str]]) -> List[List[str]]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "O" and j - 1 >= 0:
                curr = j
                left = j - 1
                while left >= 0:
                    if grid[i][left] == ".":
                        grid[i][curr], grid[i][left] = grid[i][left], grid[i][curr]
                    else:
                        break

                    curr = left
                    left -= 1

    return grid

def tilt_east(grid: List[List[str]]) -> List[List[str]]:
    for i in range(len(grid)):
        for j in range(len(grid[i]) - 2, -1, -1):
            if grid[i][j] == "O" and j + 1 < len(grid[i]):
                curr = j
                right = j + 1
                while right < len(grid[i]):
                    if grid[i][right] == ".":
                        grid[i][curr], grid[i][right] = grid[i][right], grid[i][curr]
                    else:
                        break

                    curr = right
                    right += 1

    return grid


def calc_load(grid: List[List[str]]) -> int:
    load = 0
    col_len = len(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "O":
                load += (col_len - i)

    return load

def render(grid: List[List[str]]) -> None:
    for l in grid:
        print("".join(l))

def hash_grid(nested_list: List[List[str]]) -> int:
    return hash(tuple(tuple(sublist) for sublist in nested_list))

def tilt_cycles(grid: List[List[str]], n: int) -> List[List[str]]:
    seen: Dict[int, int] = {}
    history: List[List[List[str]]] = [deepcopy(grid)]

    tilted_grid = grid
    for cycle in range(n):
        tilted_grid = tilt_north(tilted_grid)
        tilted_grid = tilt_west(tilted_grid)
        tilted_grid = tilt_south(tilted_grid)
        tilted_grid = tilt_east(tilted_grid)

        hashed_grid = hash_grid(tilted_grid)
        if hashed_grid in seen:
            first = seen[hashed_grid]
            period = cycle + 1 - first
            remaining = (n - (cycle + 1)) % period

            return history[first + remaining]

        seen[hashed_grid] = cycle + 1
        history.append(deepcopy(tilted_grid))

    return tilted_grid


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    # for l in grid:
    #     print(l)
    tilted_grid = tilt_north(grid)
    # print("--")
    # for l in tilted_grid:
    #     print(l)

    load = calc_load(tilted_grid)

    print("Total", load)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    # print("======--original")
    # render(grid)

    tilted_grid = tilt_cycles(grid, 1_000_000_000)
    load = calc_load(tilted_grid)

    print("Total", load)