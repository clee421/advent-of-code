from typing import Dict, List, Tuple

directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
    (-1, -1),
    (1, -1),
    (1, 1),
    (-1, 1),
]

def validate_xmas(
    grid: List[List[str]],
    start: Tuple[int, int],
    direction: Tuple[int, int],
) -> bool:
    next_x = start[0]
    next_y = start[1]

    for letter in list("XMAS"):
        if next_x < 0 or next_x >= len(grid):
            return False
        if next_y < 0 or next_y >= len(grid[next_x]):
            return False

        if grid[next_x][next_y] != letter:
            return False

        next_x += direction[0]
        next_y += direction[1]

    return True

def validate_x_mas(
    grid: List[List[str]],
    pos: Tuple[int, int],
) -> bool:
    def valid_range(x, y):
        if x < 0 or x >= len(grid):
            return False
        if y < 0 or y >= len(grid[x]):
            return False
        return True

    all_valid = (
        valid_range(pos[0], pos[1]) and
        valid_range(pos[0]-1, pos[1]-1) and
        valid_range(pos[0]+1, pos[1]-1) and
        valid_range(pos[0]-1, pos[1]+1) and
        valid_range(pos[0]+1, pos[1]+1)
    )
    if not all_valid:
        return False

    if grid[pos[0]][pos[1]] != "A":
        return False

    ms_list = [grid[pos[0]-1][pos[1]-1], grid[pos[0]+1][pos[1]+1]]
    if "M" not in ms_list or "S" not in ms_list:
        return False

    ms_list = [grid[pos[0]+1][pos[1]-1], grid[pos[0]-1][pos[1]+1]]
    if "M" not in ms_list or "S" not in ms_list:
        return False

    return True

def parse_lines_grid(filepath: str) ->List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for line in lines:
        x = list(line)
        grid.append(x)

    return grid


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            for direction in directions:
                if validate_xmas(grid, (i, j), direction):
                    total += 1

    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if validate_x_mas(grid, (i, j)):
                total += 1

    print("Total:", total)