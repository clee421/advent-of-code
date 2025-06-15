from typing import Dict, List, Set, Tuple

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return [list(l) for l in lines]

def expand_universe(grid: List[List[str]]) -> List[List[str]]:
    row_set = set()
    col_set = set()

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "#":
                row_set.add(r)
                col_set.add(c)

    new_grid = []
    for r in range(len(grid)):
        new_row = []
        for c in range(len(grid[r])):
            new_row.append(grid[r][c])
            if c not in col_set:
                new_row.append(".")

        new_grid.append(new_row)
        if r not in row_set:
            new_grid.append(["."] * len(new_row))

    return new_grid

def get_empty_space(grid: List[List[str]], expansion: int) -> Tuple[List[int], List[int]]:
    row_set = set()
    col_set = set()

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "#":
                row_set.add(r)
                col_set.add(c)
    row_dist = []
    for r in range(len(grid)):
        if r not in row_set:
            row_dist.append(expansion)
        else:
            row_dist.append(1)

    col_dist = []
    for c in range(len(grid[0])):
        if c not in col_set:
            col_dist.append(expansion)
        else:
            col_dist.append(1)

    return (row_dist, col_dist)

def find_galaxy_list(grid: List[List[str]]) -> Tuple[int, int]:
    galaxy_list = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                galaxy_list.append((i, j))

    return galaxy_list

def find_shortest_path(start: Tuple[int, int], end: Tuple[int, int], grid: List[List[str]]) -> int:
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    seen = set()
    queue = [(start, 0)]
    while queue:
        curr = queue.pop(0)
        pos = curr[0]
        steps = curr[1]
        if pos == end:
            return steps

        for d in directions:
            x, y = pos[0] + d[0], pos[1] + d[1]

            if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[x]):
                continue

            if (x, y) in seen:
                continue

            queue.append(((x, y), steps + 1))
            seen.add((x, y))

    return -1

def find_shortest_path_2(start: Tuple[int, int], end: Tuple[int, int]) -> int:
    abs_x = abs(start[0] - end[0])
    abs_y = abs(start[1] - end[1])

    return abs_x + abs_y

def find_shortest_path_3(
    start: Tuple[int, int],
    end: Tuple[int, int],
    row_dist: List[int],
    col_dist: List[int],
) -> int:
    abs_x = 0
    for r in range(min(start[0], end[0]) + 1, max(start[0], end[0]) + 1):
        abs_x += row_dist[r]

    abs_y = 0
    for c in range(min(start[1], end[1]) + 1, max(start[1], end[1]) + 1):
        abs_y += col_dist[c]

    return abs_x + abs_y

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    expanded_grid = expand_universe(grid)
    galaxy_list = find_galaxy_list(expanded_grid)

    pairs = []
    for i in range(len(galaxy_list)):
        for j in range(i + 1, len(galaxy_list)):
            pairs.append((galaxy_list[i], galaxy_list[j]))

    total = 0
    for i, p in enumerate(pairs):
        # if i % 100 == 0:
        #     print(f"in progress... {i + 1} / {len(pairs)}")
        steps = find_shortest_path_2(p[0], p[1])
        # print(f"from: {p[0]}, to: {p[1]}; steps {steps}")
        total += steps

    print("Total:", total)


def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    expanded_space = 10
    if args[0] == "input":
        expanded_space = 1_000_000
    row_dist, col_dist = get_empty_space(grid, expanded_space)

    galaxy_list = find_galaxy_list(grid)

    pairs = []
    for i in range(len(galaxy_list)):
        for j in range(i + 1, len(galaxy_list)):
            pairs.append((galaxy_list[i], galaxy_list[j]))

    total = 0
    for i, p in enumerate(pairs):
        # if i % 100 == 0:
        #     print(f"in progress... {i + 1} / {len(pairs)}")
        steps = find_shortest_path_3(p[0], p[1], row_dist, col_dist)
        # print(f"from: {p[0]}, to: {p[1]}; steps {steps}")
        total += steps

    print("Total:", total)
