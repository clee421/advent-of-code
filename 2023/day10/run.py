from math import gcd
from typing import Dict, List, Tuple, Set

WEST = (0, -1)
EAST = (0, 1)
NORTH = (-1, 0)
SOUTH = (1, 0)

def parse_inputs(filepath: str) -> List[List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for l in lines:
        grid.append(list(l))

    return grid

def find_start_pos(grid: List[List[str]]) -> Tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                return (i, j)

    raise Exception("start position not found")

def find_path_from_start(start: Tuple[int, int], grid: List[List[str]]) -> List[List[str|int]]:
    copied_grid = [["."] * len(r) for r in grid]
    pipe_direction = {
        "|": [NORTH, SOUTH],
        "-": [EAST, WEST],
        "L": [NORTH, EAST],
        "J": [NORTH, WEST],
        "7": [SOUTH, WEST],
        "F": [SOUTH, EAST],
    }

    queue = [(start, 0)]
    seen = set([start])
    while len(queue) > 0:
        curr_steps = queue.pop(0)
        curr = curr_steps[0]
        steps = curr_steps[1]
        curr_pipe = grid[curr[0]][curr[1]]

        copied_grid[curr[0]][curr[1]] = steps

        # print(f"curr: {curr}, steps: {steps}, pipe: {curr_pipe}")
        for d in pipe_direction[curr_pipe]:
            dx, dy = d[0] + curr[0], d[1] + curr[1]
            if (dx, dy) in seen:
                continue

            # print(f" -> next: {(dx, dy)}, pipe: {grid[dx][dy]}")
            queue.append(((dx, dy), steps + 1))
            seen.add((dx, dy))

    return copied_grid

# def order_convex_hull(points: Set[Tuple[int, int]]) -> list:
#     try:
#         from scipy.spatial import ConvexHull
#     except ModuleNotFoundError:
#         print("Module scipy is not found, run pip install scipy")

#     if len(points) < 3:
#         raise ValueError("At least 3 points are required to form a polygon.")
#     point_list = list(points)
#     hull = ConvexHull(point_list)
#     return [point_list[i] for i in hull.vertices]

# def shoelace_area(coords):
#     n = len(coords)
#     area = 0
#     for i in range(n):
#         x0, y0 = coords[i]
#         x1, y1 = coords[(i + 1) % n]
#         area += (x0 * y1 - x1 * y0)
#     return abs(area) / 2

# def boundary_points(coords):
#     n = len(coords)
#     boundary = 0
#     for i in range(n):
#         x0, y0 = coords[i]
#         x1, y1 = coords[(i + 1) % n]
#         dx = abs(x1 - x0)
#         dy = abs(y1 - y0)
#         boundary += gcd(dx, dy)
#     return boundary

# def picks_theorem(seen: Set[Tuple[int, int]]):
#     polygon = order_convex_hull(seen)
#     area = shoelace_area(polygon)
#     boundary = boundary_points(polygon)
#     interior = area - boundary / 2 + 1
#     return {
#         "ordered_boundary": polygon,
#         "area": area,
#         "boundary_points": boundary,
#         "interior_points": int(round(interior)),
#     }

# This is what I get for copying from chatgpt
# def get_points(start: Tuple[int, int], grid: List[List[str]]) -> List[Tuple[int, int]]:
#     copied_grid = [["."] * len(r) for r in grid]
#     pipe_direction = {
#         "|": [NORTH, SOUTH],
#         "-": [EAST, WEST],
#         "L": [NORTH, EAST],
#         "J": [NORTH, WEST],
#         "7": [SOUTH, WEST],
#         "F": [SOUTH, EAST],
#     }

#     queue = [(start, 0)]
#     seen = set([start])
#     while len(queue) > 0:
#         curr_steps = queue.pop(0)
#         curr = curr_steps[0]
#         steps = curr_steps[1]
#         curr_pipe = grid[curr[0]][curr[1]]

#         copied_grid[curr[0]][curr[1]] = steps

#         # print(f"curr: {curr}, steps: {steps}, pipe: {curr_pipe}")
#         for d in pipe_direction[curr_pipe]:
#             dx, dy = d[0] + curr[0], d[1] + curr[1]
#             if (dx, dy) in seen:
#                 continue

#             # print(f" -> next: {(dx, dy)}, pipe: {grid[dx][dy]}")
#             queue.append(((dx, dy), steps + 1))
#             seen.add((dx, dy))

#     return picks_theorem(seen)

def fill_grid(start: Tuple[int, int], grid: List[List[str]], value: str) -> None:
    DIRECTIONS = [WEST, NORTH, EAST, SOUTH]

    queue = [start]
    seen = set([start])
    while len(queue) > 0:
        curr = queue.pop(0)
        grid[curr[0]][curr[1]] = value

        for d in DIRECTIONS:
            dx, dy = d[0] + curr[0], d[1] + curr[1]
            if dx < 0 or dx >= len(grid) or dy < 0 or dy >= len(grid[dx]):
                continue
            if grid[dx][dy] != "." or (dx, dy) in seen:
                continue

            queue.append((dx, dy))
            seen.add((dx, dy))

def map_path_to_grid(path_grid: List[List[str|int]], grid: List[List[str]]) -> List[List[str]]:
    CHAR_MAP = {
        "|": "│",
        "-": "─",
        "L": "└",
        "J": "┘",
        "7": "┐",
        "F": "┌",
    }
    copied_grid = [["."] * len(r) for r in grid]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if path_grid[i][j] != ".":
                copied_grid[i][j] = CHAR_MAP[grid[i][j]]

    return copied_grid

def expand_grid(grid: List[List[str]]) ->  List[List[str]]:
    expanded_grid = []
    for r in grid:
        res = list("." + ".".join(r) + ".")
        expanded_grid.append(res)
        expanded_grid.append(["."] * len(res))

    for i in range(1, len(expanded_grid) - 1):
        for j in range(1, len(expanded_grid[i]) - 1):
            if expanded_grid[i][j] == ".":
                left = expanded_grid[i][j-1]
                right = expanded_grid[i][j+1]
                if left in ["─", "└", "┌"] and right in ["─", "┘", "┐"]:
                    expanded_grid[i][j] = "─"

                up = expanded_grid[i-1][j]
                down = expanded_grid[i+1][j]
                if up in ["│", "┐", "┌"] and down in ["│", "┘", "└"]:
                    expanded_grid[i][j] = "│"

    return expanded_grid

def shrink_grid(expanded_grid: List[List[str]]) ->  List[List[str]]:
    shrunk_grid = []
    for i in range(0, len(expanded_grid), 2):
        shrunk_row = []
        for j in range(1, len(expanded_grid[i]), 2):
            shrunk_row.append(expanded_grid[i][j])

        shrunk_grid.append(shrunk_row)

    return shrunk_grid


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))
    starting_pos = find_start_pos(grid)

    if args[0] in ["sample", "input"]:
        start_piece = "F"
    else:
        raise Exception(f"need to account for {args[0]}")

    grid[starting_pos[0]][starting_pos[1]] = start_piece

    clean_grid = find_path_from_start(starting_pos, grid)

    max_step = 0
    for r in clean_grid:
        for e in [c if c != "." else 0 for c in r]:
            max_step = max(max_step, e)

    print("Steps:", max_step)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))
    starting_pos = find_start_pos(grid)

    if args[0] in ["sample", "input"]:
        start_piece = "F"
    else:
        raise Exception(f"need to account for {args[0]}")

    grid[starting_pos[0]][starting_pos[1]] = start_piece

    clean_grid = find_path_from_start(starting_pos, grid)
    visual_grid = map_path_to_grid(clean_grid, grid)
    expanded_grid = expand_grid(visual_grid)

    fill_grid((0, 0), expanded_grid, "X")

    shrunk_grid = shrink_grid(expanded_grid)

    # with open("day10/lazy.txt", "w") as f:
    #     for r in shrunk_grid:
    #         # print("".join(r))
    #         f.write("".join(r) + "\n")

    count = 0
    for r in shrunk_grid:
        for c in r:
            if c == ".":
                count += 1
    print("Count:", count)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX┌┐XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX││XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX│└┐XXX┌┐XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX┌──┐X┌┐XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└┐└┐┌┐││XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└─┐└┐││┌┐XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXX┌─┐┌┐XXXXXXXXXXXXXXXX┌─┐└┐││││└┐XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└┐││└┘└┐XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXX└┐└┘│XX┌┐XXXXXXXXXXXX└┐│X│└┘└┘┌┘XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX┌─┐┌┘││┌──┘XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXX┌─┘┌─┘XX│└┐XX┌┐XXX┌─┐┌─┘└┐└─┐┌─┘XXXXXXXXXXXXXXXXX┌┐XXXXXXXXXXXX└┐└┘┌┘││┌┐┌┐XXXXXXXX┌┐XXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXX└─┐│X┌─┐│┌┘XX│└┐XX└┐│└──┐└┐┌┘└───┐┌─┐XXXXXXXXXX┌─┘└┐┌┐┌┐XX┌──┐┌┐└─┐└┐│││└┘│XXX┌┐XX┌┘└┐XXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXX┌──┘│┌┘┌┘││XX┌┘┌┘X┌─┘└┐┌┐│┌┘└─┐┌──┘│┌┘X┌┐XXXXXXX└──┐└┘││└─┐│┌─┘││┌┐│┌┘│││┌─┘XX┌┘└─┐│┌─┘XXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXX└──┐││┌┘X││┌┐└┐│┌┐└──┐││└┘└┐┌─┘└─┐┌┘└┐┌┘└──┐XXX┌┐┌┐└┐┌┘│┌─┘││┌─┘││││└─┘│││┌┐┌┐└─┐┌┘││X┌┐┌─┐XXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXX┌┐X┌┘└┘│┌┐││││┌┘│││┌┐┌┘│└──┐│└┐┌──┘└┐┌┘│┌─┐┌┘┌┐┌┘└┘└┐│└─┘└┐X││└─┐│││└─┐┌┘││││││X┌┘└─┘│┌┘│└┐│XXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXX│└┐└──┐││││└┘│└┐└┘│││└┐└┐┌┐│└┐│└─┐┌┐││┌┘└┐││┌┘│└─┐┌─┘│┌──┐└─┘└─┐││││┌─┘│┌┘└┘└┘└┐└───┐└┘┌┘┌┘└─┐XXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXX┌┐X│┌┘┌──┘└┘└┘┌┐│X└─┐│││┌┘┌┘││└┐│└─┐└┘└┘└┘┌─┘└┘└┐│X┌┘└┐X└┘┌─┘┌┐┌─┐││└┘│└─┐│└┐┌────┘┌┐┌─┘┌─┘┌┘┌┐┌┘XXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXX││┌┘│X└─┐┌┐┌──┘└┘┌┐┌┘│││└┐│X││X││┌┐└─┐┌──┐└─┐X┌┐│└─┘┌─┘┌┐X└──┘││X│││┌─┘┌┐││X││┌┐┌┐┌┘│└─┐│┌─┘┌┘└┘XXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXX│││┌┘┌┐X└┘││┌──┐┌┘│└┐└┘└─┘└┐│└┐│└┘│┌┐││┌┐└──┘┌┘││┌─┐│┌┐││┌─┐┌┐└┘┌┘└┘│┌┐│││└─┘└┘└┘│└┐└┐X││└┐┌┘XXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXX┌┐││││┌┘│┌──┘│└┐┌┘└┐└┐│┌─────┘│┌┘└┐┌┘││││││┌┐┌┐└┐│└┘X│││││││┌┘│└┐┌┘┌─┐││││││┌──┐┌─┐│┌┘┌┘┌┘└┐││┌┐XXXXXX┌─┐XXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXX│└┘│││└┐│└──┐│X│└─┐└┐│││X┌─┐┌─┘│┌┐│└┐│││└┘└┘└┘└┐│└┐┌─┘││└┘││└┐└┐│└┐│┌┘││││││└─┐└┘X└┘└┐│┌┘┌─┘│└┘└┐XXXXX└┐│XXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXX┌┘┌┐└┘└┐││X┌─┘└─┘┌─┘┌┘││└┐│┌┘└─┐│││└┐└┘└┘┌──────┘│┌┘└─┐││┌─┘└┐│X│└┐└┘└┐││││││┌─┘X┌┐X┌┐│││┌┘┌─┘┌──┘XXXXXX││┌┐XXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXX└─┘└┐┌┐└┘└┐└────┐│X┌┘┌┘└┐└┘└┐┌┐│└┘└┐└─┐┌─┘┌───┐┌┐│└┐┌┐││││┌┐X│└┐└┐└───┘└┘│││││┌─┐│└┐││││││X│┌─┘┌┐XXXXXX┌┘└┘│XXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXX┌──┘│└─┐┌┘┌────┘└┐└┐└┐┌┘┌──┘││└┐┌─┘X┌┘└─┐└┐┌┐││└┘┌┘│││└┘└┘└┐└┐└┐└──────┐└┘││││┌┘│┌┘│││││└─┘│┌┐││┌┐┌─┐┌┘┌──┘XXXXXXXXXXXX
# XXXXXXXXXXXXX┌┐XXXXXX└──┐│┌─┘└┐└────┐┌┘X│┌┘└┐└┐┌┐││X││┌┐┌┘┌──┘┌┘│└┘└─┐└┐││└──┐┌─┘┌┘┌┘┌─────┐└─┐└┘││└─┘└┐│││││┌┐┌┘│││││││┌┘└┐└┐XXXXXXXXXXXXXX
# XXXXXXXXXXXXX││XXXXXXX┌┐└┘└──┐│X┌┐┌┐││┌─┘│┌┐└┐│││││┌┘││││┌┘X┌┐└┐│┌┐┌─┘┌┘│└┐┌┐│└─┐└┐└┐└──┐┌┐└──┘┌┐└┘┌──┐│││││││└┘┌┘└┘└┘└┘└┐┌┘┌┘XXXXXXXXXXXXXX
# XXXXXXXXXXX┌─┘│XXX┌┐┌─┘└─┐┌──┘└┐│└┘││└┘┌─┘││X│└┘└┘│└┐│││││┌┐│└┐│└┘│└─┐└┐└┐││└┘┌─┘X│┌┘┌─┐└┘└────┘│┌─┘┌┐└┘│││││└─┐│┌┐┌─────┘│┌┘XXXXXXXXXXXXXXX
# XXXXXXXXXXX└─┐│┌┐X││└──┐┌┘└───┐│└─┐│└─┐│┌─┘└┐└───┐└┐│└┘└┘└┘│└┐││┌─┘┌┐└┐└─┘│└─┐└┐┌┐│└┐│┌┘X┌┐X┌┐┌┐│└──┘└┐┌┘││└┘┌─┘└┘││┌┐┌┐X┌┘└─┐XXXXXXXXXXXXXX
# XXXXXXXXXX┌┐X││││┌┘└┐┌┐│└┐┌───┘│┌─┘└┐┌┘└┘┌──┘┌┐┌┐└┐│└┐┌┐┌──┘┌┘└┘└┐┌┘└─┘┌──┘┌┐│┌┘│└┘┌┘│└┐┌┘└─┘│││└┐┌───┘└┐││┌─┘┌┐X┌┘└┘└┘└─┘┌──┘┌┐XXXXXXXXXXXX
# XXXXXXXXX┌┘└─┘└┘││┌─┘││└┐└┘┌──┐│└──┐││┌─┐└──┐│└┘│┌┘└─┘││└┐┌┐└┐┌──┘└───┐│┌┐┌┘││└┐│┌┐└┐└┐││┌┐┌┐└┘│┌┘└─┐┌┐┌┘││└─┐││┌┘┌─┐┌───┐└───┘│XXXXXXXXXXXX
# XXXXXXXXX│┌┐┌┐┌┐│││┌┐││X└┐┌┘┌─┘└┐┌┐││││X└───┘└┐┌┘└┐┌──┘└─┘││X│└┐┌┐┌──┐│└┘│└┐││┌┘└┘└┐│┌┘│└┘└┘└─┐││┌┐┌┘││└┐││┌─┘││└┐└┐│└──┐│┌────┘XXXXXXXXXXXX
# XXXXXXXXX││└┘└┘│└┘││└┘│┌┐└┘X└──┐││││└┘└──┐┌┐X┌┘└┐┌┘│┌┐XX┌┐││┌┘┌┘│└┘┌─┘└─┐│┌┘││└┐┌┐X││└┐│X┌┐┌┐┌┘│└┘│└─┘└┐│└┘└─┐│└─┘┌┘└───┘│└───┐XXXXXXXXXXXXX
# XXXXXXXXX└┘┌┐XX└─┐│└┐┌┘││┌┐X┌┐┌┘└┘│└─┐┌──┘││┌┘┌─┘└┐││└┐┌┘││││┌┘X└─┐│X┌──┘││┌┘│┌┘│└┐│└┐│└┐│└┘│└┐└┐┌┘┌───┘│┌───┘└┐┌┐└────┐X└────┘XXXXXXXXXXXXX
# XXXXXXXXXXX││X┌──┘└┐│└┐│││└─┘│└──┐└┐┌┘└─┐┌┘│└┐│┌┐┌┘││┌┘│┌┘│││└─┐X┌┘└┐└──┐└┘└┐││X└┐││┌┘│┌┘└─┐│┌┘┌┘└┐│X┌┐X││┌┐┌┐┌┘││┌┐┌┐┌┘┌┐┌┐┌┐XX┌┐XXXXXXXXXX
# XXXXXXXXXX┌┘└┐└───┐│└┐│││└──┐│┌──┘┌┘└─┐┌┘└┐└─┘│││└┐└┘└┐││┌┘││┌─┘┌┘┌─┘┌─┐└──┐││└┐┌┘││└┐│└┐┌─┘└┘┌┘X┌┘│┌┘└┐│││││└┘┌┘└┘└┘└┘┌┘└┘└┘└─┐││XXXXXXXXXX
# XXXXXXXXXX└─┐│┌───┘└─┘│││┌┐┌┘│└──┐│┌┐X││┌┐└─┐┌┘││X└─┐┌┘││└┐│││┌┐│┌┘┌┐└┐│X┌┐│││┌┘└┐││┌┘└┐│└┐┌──┘┌┐└┐│└┐┌┘│└┘││┌─┘X┌┐X┌┐X└┐┌────┐└┘└┐XXXXXXXXX
# XXXXXXXXXX┌─┘│└──────┐└┘│││└┐└─┐X│└┘│┌┘│││┌┐││┌┘│┌┐┌┘└┐│└┐│││└┘││└┐││┌┘└┐││││││┌┐│││└┐┌┘└┐│└┐┌┐││┌┘└┐││┌┘┌─┘││X┌─┘└─┘└┐┌┘└───┐└───┘XXXXXXXXX
# XXXXXXXXXX└─┐└───────┘┌┐└┘└─┘┌┐│┌┘┌┐││┌┘│││││└┘┌┘│││┌┐││┌┘│││┌┐│└┐└┘│└┐┌┘│││││││││││┌┘└┐.││┌┘│││└┘┌┐└┘└┘.└──┘└─┘┌──┐┌─┘│┌────┘X┌─┐XXXXXXXXXX
# XXXXXXXX┌─┐X└┐┌─┐┌┐┌──┘└──┐┌┐│││└─┘││││┌┘└┘└┘┌─┘┌┘│└┘│││└┐││└┘││┌┘┌─┘┌┘└─┘││└┘││└┘└┘│┌─┘┌┘│└┐│└┘.┌┘└───────┐┌┐┌─┘┌┐└┘┌─┘│┌┐┌┐┌┐│┌┘XXXXXXXXXX
# XXXXXXXX└┐│XX└┘X└┘└┘X┌─┐┌─┘│└┘│└───┘└┘│└─┐┌──┘┌┐│┌┘┌─┘└┘.││└┐┌┘│└┐└─┐│┌───┘│┌─┘└───┐│└┐.└┐└┐│└┐┌┐└─┐┌─┐┌──┐││││┌─┘└─┐│┌─┘││││││││XXXXXXXXXXX
# XXXXXXXXX│└┐┌─┐┌┐┌┐X┌┘┌┘└──┘X┌┘┌┐┌───┐└─┐││┌┐┌┘││└┐└────┐││.│└┐└┐│┌─┘│└┐┌─┐│└┐┌┐┌┐┌┘│┌┘┌┐│┌┘│┌┘│└──┘└┐└┘.┌┘└┘└┘└┐┌──┘││┌┐│││││└┘└─┐XXXXXXXXX
# XXXXXXXXX│┌┘└┐└┘└┘└┐└┐└─────┐└─┘└┘X┌┐└┐.││└┘│└┐│└┐└┐┌──┐│└┘┌┘┌┘┌┘│└┐┌┘┌┘│.││.└┘│││└┐│└─┘││└┐└┘.└──┐┌─┘┌──┘X┌┐X┌┐││┌┐X│└┘└┘└┘└┘┌───┘XXXXXXXXX
# XXXXX┌┐┌─┘│┌┐│┌───┐└─┘┌────┐└┐X┌─┐┌┘└─┘┌┘└─┐└┐│└─┘┌┘└─┐││┌┐└┐│.└┐│┌┘│┌┘┌┘┌┘└──┐││└┐│└┐┌┐│└┐└─┐.┌┐┌┘│┌┐└────┘└┐│││││└─┘┌┐┌───┐┌┘┌─┐XXXXXXXXXX
# XXXXX│└┘┌┐│││└┘┌┐X└───┘┌┐┌┐└┐└┐│┌┘└──┐.└┐┌─┘┌┘└┐┌─┘┌┐┌┘│└┘│┌┘└┐┌┘│└┐│└┐│┌┘┌─┐┌┘│└┐└┘.││└┘.│┌┐└┐││└┐││└──────┐└┘└┘└┘┌┐┌┘│└─┐X│└─┘┌┘XXXXXXXXXX
# XXXXX└──┘│└┘│┌┐││┌───┐┌┘└┘│X└┐└┘│┌┐┌─┘┌┐└┘┌─┘┌┐││┌┐││└┐│┌─┘│┌┐│└┐│.││┌┘│└┐└┐│└┐└┐│┌──┘│.┌┐└┘└─┘││┌┘││┌─┐┌┐┌┐└─┐┌─┐┌┘└┘┌┘┌┐│┌┘┌┐┌┘XXXXXXXXXXX
# XXXXX┌─┐┌┘┌┐└┘└┘│└─┐┌┘└──┐└─┐└─┐└┘└┘┌─┘└┐.└─┐│└┘││││└┐││└─┐└┘│└┐│└┐└┘└┐│┌┘┌┘└┐└┐└┘└┐┌┐└─┘└────┐││└─┘└┘.└┘└┘└─┐│└┐│└──┐└─┘└┘│┌┘│└┐XXXXXXXXXXX
# XXX┌┐└┐│└─┘└───┐│┌┐││X┌──┘┌┐└─┐└────┘┌─┐└┐┌┐└┘.┌┘││└┐││└┐┌┘┌─┘┌┘└┐│┌──┘││┌┘┌┐│┌┘.┌┐││└┐┌───┐┌┐││└──┐┌┐┌──────┘└┐││┌──┘┌┐┌┐X││X└─┘XXXXXXXXXXX
# ┌──┘│┌┘│┌──────┘└┘└┘└─┘┌┐┌┘│┌┐└──────┘.└┐└┘└──┐└┐││┌┘│└┐││.└─┐└─┐└┘└──┐││└─┘│││┌─┘└┘└┐││┌──┘│└┘└──┐│││└──────┐X└┘└┘┌──┘└┘└┐│└─┐┌┐XXXXXXXXXXX
# └──┐│└┐└┘┌──────┐┌┐┌─┐┌┘││X└┘└─────────┐│┌───┐│┌┘│└┘.│┌┘└┘┌──┘┌┐└─┐┌──┘│└┐┌─┘└┘│┌┐┌┐┌┘└┘└┐┌┐└─┐┌──┘└┘└──────┐└──┐┌─┘┌┐┌───┘└─┐└┘└─┐XXXXXXXXX
# ┌──┘└─┘┌─┘┌┐┌──┐└┘└┘X└┘X└┘┌────┐┌──────┘└┘┌┐┌┘│└┐└─┐┌┘└──┐└┐┌┐││┌┐│└─┐┌┘┌┘└─┐┌┐│││││└───┐└┘│┌─┘└─────┐┌────┐└───┘│┌─┘└┘┌────┐│┌┐┌─┘XXXXXXXXX
# └┐┌┐┌──┘┌─┘││┌┐└┐X┌┐X┌┐X┌┐└───┐└┘┌────┐.┌┐││└─┘.└┐┌┘└┐┌┐┌┘.││││││└┘┌─┘└┐└┐┌┐└┘│││└┘│┌┐┌┐│┌─┘│┌───────┘│┌───┘┌──┐X││X┌┐X└┐┌┐┌┘││└┘XXXXXXXXXXX
# X└┘│└┐┌─┘┌┐└┘│└┐└─┘└─┘└─┘└─┐X┌┘┌─┘┌──┐└─┘└┘│.┌┐..│└─┐││└┘┌┐│││││└─┐└─┐┌┘.│││┌─┘└┘.┌┘│││└┘└┐┌┘└┐┌┐┌┐┌─┐│└─┐┌┐└┐┌┘┌┘└─┘└──┘│└┘X└┘XXXXXXXXXXXXX
# XXX└─┘└┐┌┘└─┐│┌┘┌┐┌─┐┌─┐┌─┐└─┘┌┘┌┐└┐.└┐┌┐┌┐└─┘└┐┌┘┌┐││└┐┌┘└┘│└┘└──┘.┌┘│┌─┘││└─┐.┌┐└┐││└─┐┌┘└┐┌┘│││││.└┘┌┐└┘└─┘└─┘┌┐┌┐┌──┐└┐┌┐┌────┐XXXXXXXXX
# XXXXXXX││┌──┘│└─┘│└┐││┌┘│X└─┐┌┘┌┘└─┘┌┐└┘└┘└─┐┌─┘└─┘│││┌┘└┐┌┐└───┐┌──┘┌┘└─┐││┌┐│┌┘└─┘│└┐┌┘└┐┌┘└─┘└┘└┘┌──┘└──────┐┌┘└┘│└┐X└┐└┘││┌───┘XXXXXXXXX
# XXXXXXX││└──┐│X┌┐└┐│└┘└┐│┌──┘│X└────┘└─┐┌┐┌┐└┘┌─┐┌┐││└┘┌─┘││┌┐┌┐│└┐┌─┘┌──┘│└┘││└┐┌─┐│.││┌─┘└┐.┌┐┌┐┌┐└─────────┐└┘X┌┐└┐└─┐│┌┐└┘└─┐XXXXXXXXXXX
# XXXXXXX└┘XXX└┘┌┘│X└┘┌──┘│└─┐┌┘┌───┐┌┐┌┐└┘└┘└─┐└┐└┘││└─┐└┐┌┘││└┘└┘.└┘┌┐└┐┌┐└─┐││┌┘│┌┘└┐│││┌┐┌┘┌┘││└┘│┌┐┌───┐┌──┘X┌─┘│X└┐┌┘│││┌┐┌─┘XXXXXXXXXXX
# XXXXXXXXXXXX┌┐└┐│┌┐X└──┐│┌─┘│X└┐┌┐└┘└┘└┐┌───┐└─┘┌─┘└─┐│┌┘└┐│└┐...┌──┘└─┘││┌─┘└┘└─┘└──┘└┘└┘└┘.└┐│└─┐│││└──┐│└────┘┌┐│┌┐└┘X└┘└┘└┘XXXXXXXXXXXXX
# XXXXXXXXXXX┌┘└─┘└┘│┌┐┌┐└┘└──┘┌┐└┘│┌───┐││┌┐.└┐┌┐└┐┌┐.└┘│┌─┘└┐└┐┌┐└─┐┌┐┌─┘│└───┐┌──────┐┌┐┌─┐┌─┘└──┘└┘└───┘│┌─────┘│└┘│┌──┐┌┐┌─┐XXXXXXXXXXXXX
# XXXXXXXXX┌─┘┌┐┌──┐└┘└┘└──────┘└─┐└┘┌─┐│└┘│└─┐│││┌┘││┌┐.│└┐.┌┘┌┘│└──┘││└┐.└┐┌─┐││┌┐┌┐┌┐└┘└┘┌┘└┐┌┐┌─┐┌───┐┌┐└┘┌┐X┌─┐│┌┐└┘┌┐└┘└┘┌┘XXXXXXXXXXXXX
# XXXXXXXXX└──┘└┘┌┐└────────────┐┌┘X┌┘.└┘.┌┘┌┐││││└─┘││└┐│┌┘┌┘┌┘.└┐┌┐┌┘│┌┘┌─┘└┐││││└┘└┘└───┐└─┐└┘└┘.└┘┌┐.└┘│┌─┘└┐│┌┘└┘│┌─┘└─┐┌┐└┐XXXXXXXXXXXXX
# XXXXXXXXX┌─────┘└┐┌┐X┌─┐X┌┐┌┐┌┘└─┐└──┐┌┐└┐│└┘└┘└┐┌─┘│┌┘└┘.└┐└──┐└┘│└┐││┌┘┌┐┌┘└┘└┘.┌┐┌┐.┌─┘┌┐└┐┌─┐┌┐┌┘└──┐└┘┌─┐└┘└─┐X└┘┌┐┌┐└┘└┐│XXXXXXXXXXXXX
# XXXXXXXXX└┐┌────┐└┘└┐└┐│┌┘└┘│└┐┌┐│┌──┘│└─┘└────┐└┘.┌┘│┌┐┌┐.└┐┌┐│..└─┘││└┐││└─┐┌───┘└┘└─┘┌┐│└┐│└┐│││└───┐└──┘┌┘┌┐┌─┘┌┐┌┘└┘└┐┌┐└┘XXXXXXXXXXXXX
# XXXXXXXXXX└┘X┌┐X└──┐│┌┘└┘┌─┐│X││└┘└───┘┌───────┘.┌┐│┌┘│└┘└┐.└┘└┘.....└┘.└┘└┐┌┘│┌────────┘└┘┌┘└─┘└┘└──┐.└───┐└─┘│└──┘└┘┌──┐└┘└───┐XXXXXXXXXXX
# XXXXXXXXXX┌┐┌┘└────┘└┘┌─┐│┌┘│┌┘└──────┐└──┐┌┐┌┐.┌┘└┘└─┘┌┐┌┘................│└┐││┌─────────┐└────────┐│┌────┘┌─┐│┌┐┌───┘┌┐└──────┘XXXXXXXXXXX
# XXXXXXXXX┌┘└┘┌───────┐└┐└┘└┐└┘┌┐┌────┐│┌┐┌┘│││└─┘┌─┐┌──┘└┘.................└─┘└┘└┐┌─┐┌─┐┌┐└─────────┘└┘┌───┐│┌┘└┘└┘┌───┘└┐X┌──┐XXXXXXXXXXXXX
# XXXXXXXXX└───┘┌──────┘┌┘X┌┐└┐┌┘└┘┌┐┌─┘└┘│└┐│││┌──┘┌┘└───┐......................┌┐└┘┌┘└┐││└┐┌─┐┌┐┌┐┌┐┌┐┌┘┌──┘│└─┐X┌┐│┌─┐┌┐└─┘┌┐└─┐XXXXXXXXXXX
# XXXXXXXXXX┌──┐└───┐┌┐┌┘X┌┘└┐└┘┌──┘└┘┌┐┌┐└─┘│└┘└──┐└┐┌┐┌┐│┌─┐..................┌┘│┌┐└──┘││.└┘.└┘└┘└┘└┘└┘.└──┐│┌┐└┐│└┘└┐└┘└───┘└─┐│XXXXXXXXXXX
# XXXXXXXXXX└─┐└─┐┌─┘│││┌─┘┌┐└──┘┌┐┌──┘└┘└┐┌┐│┌─┐┌┐└┐└┘└┘│└┘┌┘..................└┐│││.┌┐.└┘┌─┐┌─┐┌┐┌─┐┌┐┌─┐┌┐└┘│└─┘│┌──┘┌────┐X┌┐└┘XXXXXXXXXXX
# XXXXXXXXXX┌┐└─┐│└──┘└┘└──┘└──┐┌┘││┌─────┘││││.│││┌┘.┌┐.│┌─┘...................┌┘└┘└─┘└┐┌┐└┐│└┐└┘│└┐│││└┐└┘└┐┌┘┌┐X│└───┘┌──┐└─┘└┐XXXXXXXXXXXX
# XXXXXXX┌┐┌┘└──┘│┌┐┌┐┌┐┌┐┌────┘│┌┘│└──────┘└┘└┐└┘│└──┘└┐└┘┌┐┌┐...............┌─┘┌┐┌┐┌─┐└┘└─┘└┐└─┐│┌┘└┘└┐└──┐││┌┘└┐│┌────┘┌┐└───┐│XXXXXXXXXXXX
# XXXXXXX│└┘┌───┐└┘└┘└┘└┘└┘┌────┘└─┘X┌┐┌┐┌┐┌┐┌┐└─┐└┐┌┐┌┐│..││││.┌┐............└──┘└┘││┌┘┌┐┌─┐┌┘┌┐│└┘┌──┐└┐┌─┘└┘│┌─┘││┌────┘└┐┌─┐└┘XXXXXXXXXXXX
# XXXXXXX└─┐│┌┐X└─┐┌───────┘┌┐┌┐X┌┐┌─┘└┘└┘└┘│││┌┐└┐└┘└┘└┘.┌┘││└─┘└┐............┌─┐..└┘└┐│└┘┌┘│┌┘└┘┌─┘┌─┘┌┘└────┘└──┘└┘┌─────┘│┌┘XXXXXXXXXXXXXX
# XXXXXXXXX└┘│└───┘│X┌───┐┌─┘└┘└─┘└┘┌─────┐.└┘└┘└─┘┌┐┌─┐┌┐└┐││┌─┐┌┘.........┌─┐└┐│.┌┐┌┐└┘┌┐└┐└┘┌─┐│┌─┘┌┐└┐.┌┐┌─┐┌┐┌─┐┌┘┌┐┌──┐│└┐XXXXXXXXXXXXXX
# XXXXXXXXXXX└┐┌───┘┌┘┌─┐│└──┐┌──┐┌─┘┌┐┌──┘┌┐┌────┐│││┌┘││┌┘└┘│.└┘..........└┐│┌┘└─┘└┘│┌┐││┌┘┌┐└┐└┘└┐┌┘└┐└─┘└┘X└┘└┘X│└─┘││┌─┘│┌┘XXXXXXXXXXXXXX
# XXXXXXXXXXXX└┘X┌──┘┌┘┌┘└┐┌┐└┘┌┐││┌─┘└┘┌┐┌┘└┘┌┐┌┐└┘││└─┘└┘┌┐┌┘┌┐............││└─────┐│││││└┐││┌┘.┌┐└┘┌┐└────────┐┌┐│┌┐┌┘│└──┘└─┐XXXXXXXXXXXXX
# XXXXXXXXXXX┌───┘┌──┘X│┌┐└┘│┌┐││└┘└────┘└┘┌──┘└┘│┌┐└┘┌─┐┌┐│││.│└─┐..........│└──────┘└┘└┘└┐└┘││┌─┘└──┘└─────────┘││└┘│└─┘┌┐┌┐┌┐│┌┐┌┐XXXXXXXXX
# XXXXXXXXX┌─┘┌───┘┌───┘││┌┐└┘└┘└┐┌┐┌──────┘┌┐┌─┐└┘└──┘.└┘└┘└┘┌┘┌─┘.........┌┘┌┐┌─────────┐└──┘│└────┐┌┐┌┐┌───────┘└─┐└┐┌┐│└┘└┘└┘││││XXXXXXXXX
# XXXXXXXXX└┐┌┘X┌─┐└────┘└┘│┌┐┌─┐└┘│└─┐┌┐┌──┘└┘┌┘.┌─────┐┌┐┌──┘┌┘...........└─┘││┌───────┐│┌┐┌┐│┌────┘│└┘└┘┌┐┌──────┐└┐└┘└┘┌┐┌┐┌┐│└┘└───┐XXXXX
# XXXXXXXXXX││┌─┘┌┘┌───────┘│└┘X│┌┐└──┘│└┘┌────┘.┌┘┌────┘│└┘┌┐┌┘...............└┘└──────┐└┘│││││└──┐┌┐└┐┌──┘└┘┌┐┌──┐└┐└──┐┌┘└┘└┘│└─┐┌───┘XXXXX
# XXXXXXXXXX└┘└─┐└┐└────┐┌─┐│┌──┘│└────┘┌┐└─────┐└┐│┌─┐┌┐│┌─┘└┘..................┌──────┘┌┐│└┘└┘┌─┐└┘│┌┘└───┐X│└┘┌─┘X└┐┌─┘│┌┐┌┐┌┘┌─┘└─┐XXXXXXX
# XXXXXXXXXXXX┌┐└┐└────┐│└┐└┘└┐┌┐└┐┌────┘└────┐┌┘.│└┘┌┘│││└┐┌┐┌┐.................└───┐┌┐┌┘│└┐┌┐.└┐│┌┐└┘┌┐┌──┘┌┘┌┐│┌┐┌┐│└┐┌┘│└┘└┘┌┘┌───┘XXXXXXX
# XXXXXXXXXXXX││X└─┐┌─┐└┘┌┘X┌┐││└─┘└────────┐.└┘.┌┘┌┐│┌┘└┘┌┘│└┘└┐.................┌──┘│└┘.└─┘││┌┐││││┌┐││└───┘┌┘└┘│└┘││┌┘└┐└┐┌─┐└┐└─────┐XXXXX
# XXXXXXXXXXXX│└───┘│X└─┐│┌┐│└┘└┐┌──────────┘┌┐┌┐└┐│└┘│┌─┐└─┘┌┐┌┘┌┐..............┌┘┌┐┌┘┌┐┌──┐│││││└┘└┘└┘└┐┌───┘┌┐X│┌─┘└┘┌─┘┌┘└┐└─┘┌─────┘XXXXX
# XXXXXXXXXX┌┐└─────┘┌┐X└┘│└┘┌┐┌┘└─┐┌───────┐│└┘│┌┘└──┘└┐└┐┌┐│└┘┌┘└┐........┌───┐└─┘││┌┘└┘┌┐└┘└┘││┌─┐┌──┐│└────┘└┐│└──┐X└─┐└──┘┌──┘┌┐XXXXXXXXX
# XXXXXXXXXX│└───────┘└───┘┌┐│││┌┐┌┘│┌──────┘└─┐└┘┌┐┌─┐┌┘┌┘│││┌┐└┐┌┘┌┐┌┐┌┐┌┐└──┐│...└┘└─┐┌┘└───┐└┘└┐└┘┌┐│└──┐┌┐┌┐││┌──┘┌┐┌┘┌───┘┌─┐│└┐XXXXXXXX
# XXXXXXXXXX└──────────┐┌─┐│││└┘││└─┘│┌────┐.┌┐│┌─┘│└┐│└┐└┐│└┘│└┐││┌┘│││││││.┌─┘└┐.┌───┐│└┐.┌┐┌┘┌──┘┌─┘└┘┌─┐└┘└┘└┘││┌┐X││└┐│X┌┐X└┐││┌┘XXXXXXXX
# XXXXXXXXX┌──┐┌──────┐└┘X││││┌─┘└───┘│┌───┘┌┘└┘└─┐└─┘└┐└┐└┘┌─┘┌┘│││┌┘││││││.└──┐└┐└──┐│└─┘┌┘└┘┌┘.┌─┘┌┐┌┐│┌┘┌┐X┌┐┌┘└┘└─┘└─┘└┐││┌─┘└┘└─┐┌─┐XXXX
# XXXXXXXXX└─┐│└─────┐└───┘│││└───────┘└────┘┌───┐└──┐.│┌┘┌┐└─┐└─┘││└─┘││└┘│┌───┘┌┘┌─┐│└┐.┌┘┌┐┌┘┌┐└┐┌┘││└┘└─┘│┌┘└┘┌┐┌┐┌────┐└┘││┌─────┘│┌┘XXXX
# XXXXXXXXX┌─┘└┐X┌┐┌─┘┌┐┌┐┌┘││┌───┐┌───┐┌─┐┌┐└─┐┌┘┌──┘┌┘│.││┌┐└─┐┌┘└┐┌─┘│┌─┘└─┐┌┐│┌┘┌┘│┌┘┌┘┌┘││┌┘│.└┘.└┘┌───┐└┘┌─┐│└┘└┘┌─┐┌┘┌┐└┘└────┐┌┘└┐XXXX
# XXXXXXXXX└┐┌┐│┌┘└┘┌┐│└┘││X││└──┐│└──┐│└┐│││┌─┘└─┘┌┐.└─┘┌┘││└──┘│┌┐││┌┐│└┐┌┐.└┘│││┌┘┌┘└┐└┐└┐└┘└┐└──┐.┌┐└──┐└─┐└┐│└┐┌┐X│┌┘└┐││┌─┐┌──┐└┘┌─┘XXXX
# XXXXXXXXX┌┘││└┘┌──┘└┘┌─┘└┐└┘┌──┘└───┘└┐│└┘└┘.┌┐.┌┘└─┐┌┐└┐│└─┐┌┐└┘││└┘└┘┌┘│└┐.┌┘└┘└┐└─┐└┐└─┘┌─┐└┐┌┐└─┘└───┘┌┐│┌┘└┐└┘└─┘└─┐││││┌┘└─┐└──┘XXXXXX
# XXXXXXXXX└─┘└─┐└┐┌───┘┌─┐└┐┌┘┌┐┌─────┐└┘┌┐┌┐┌┘└─┘┌──┘││┌┘└┐.└┘│┌─┘└─┐┌─┘.└┐└┐└┐┌──┘┌┐└┐└┐.┌┘┌┘┌┘│└┐┌┐┌┐┌─┐││└┘XX└────┐┌┐│└┘└┘└─┐┌┘┌─┐XXXXXXX
# XXXXXXXXXXXXX┌┘┌┘└───┐│X└─┘└─┘││┌────┘┌┐│└┘└┘┌──┐└──┐│││┌─┘┌┐┌┘└┐┌┐┌┘│┌┐┌┐└┐└┐│└──┐│└─┘┌┘┌┘┌┘.└─┘.└┘└┘└┘.└┘└─┐X┌┐┌┐┌┐└┘└┘X┌┐┌─┐│└─┘┌┘XXXXXXX
# XXXXXXXXX┌┐┌┐└┐└─┐┌─┐└┘┌┐┌┐┌──┘│└─────┘└┘┌┐┌┐│┌┐└───┘││││┌┐││└┐┌┘││└┐│││││┌┘┌┘│┌──┘└┐┌─┘.└┐│┌┐┌┐┌┐┌┐┌───────┐└┐│││└┘└─┐┌──┘└┘┌┘│┌─┐└┐XXXXXXX
# XXXXXXX┌┐││││X└──┘└┐│┌┐││││└───┘X┌───────┘└┘└┘│└┐┌┐┌┐││││││││┌┘│┌┘└─┘└┘││││┌┘┌┘└┐┌┐┌┘└┐┌─┐│││││││││││┌┐┌───┐└┐└┘└┘┌┐┌─┘└┐┌───┘┌┘│┌┘┌┘XXXXXXX
# XXXXXXX│└┘└┘└─┐┌─┐┌┘└┘│││││┌┐┌┐┌┐└────┐.┌┐┌─┐┌┘┌┘│││││││││└┘└┘┌┘└─────┐││└┘└┐└┐┌┘││└┐┌┘└┐│││││││││││└┘└┘┌──┘┌┘┌┐┌┐││└─┐┌┘└───┐└┐│└─┘XXXXXXXX
# XXXXXXX└─────┐││┌┘└┐┌┐└┘└┘└┘└┘│││┌┐┌─┐└─┘└┘┌┘└┐│┌┘││││└┘│└─┐┌─┘┌─┐┌──┐││└─┐┌┘.│└┐│└┐││.┌┘└┘││││└┘││└┐.┌┐└──┐└─┘└┘└┘└─┐└┘┌────┘X│└┐┌┐XXXXXXXX
# XXXXXXXXXX┌┐┌┘└┘│┌┐└┘│┌──────┐└┘└┘│└┐│┌┐┌┐┌┘┌─┘└┘┌┘│││┌─┘┌┐││.┌┘┌┘└─┐││└─┐││┌┐└┐││┌┘│└┐└─┐┌┘│││┌┐└┘┌┘┌┘└───┘X┌──────┐│┌┐└────┐X└┐│││X┌┐XXXXX
# XXXXXXX┌┐┌┘│└─┐┌┘││┌┐└┘┌┐┌┐┌─┘┌┐┌┐└─┘││└┘└┘┌┘┌───┘┌┘│││┌┐│└┘└┐└┐│┌──┘└┘┌─┘│└┘│.│└┘└┐└┐└──┘│.││└┘└┐┌┘.└───────┘┌┐┌──┐│││└─────┘┌┐└┘│└─┘└┐XXXX
# XXXXXX┌┘│└┐│┌─┘│X││││X┌┘└┘│└──┘└┘└──┐└┘┌┐┌┐└┐│┌─┐.│┌┘││││└──┐└─┘│└────┐└─┐└┐┌┘┌┘┌──┘.└──┐┌┘┌┘└──┐│└─┐┌─────┐┌┐│││┌┐└┘└┘X┌────┐│└──┘┌───┘XXXX
# XXXXXX└┐└─┘│└─┐└─┘└┘└┐└──┐└┐┌┐┌┐X┌──┘.┌┘││└┐│││┌┘┌┘│┌┘│││.┌─┘┌──┘.┌──┐└─┐└┐│└┐└┐│┌┐┌┐┌┐.│└┐└┐┌──┘└┐┌┘└────┐││└┘└┘││X┌┐┌┐│┌───┘│┌───┘XXXXXXXX
# XXXXXXX└──┐│┌┐└─┐┌┐┌┐└─┐X└┐└┘└┘└┐└─┐┌─┘┌┘│┌┘││││.│┌┘└┐└┘└┐└─┐└───┐└─┐│┌┐└┐││┌┘┌┘└┘│││││┌┘┌┘┌┘└┐.┌┐││┌┐.┌┐┌┘└┘X┌─┐│└┐│││└┘└┐┌──┘└────┐XXXXXXX
# XXXXX┌┐┌──┘│││┌─┘│└┘└─┐│┌─┘┌─┐┌┐└──┘└─┐│┌┘└┐││││┌┘└┐┌┘┌──┘┌┐│┌───┘┌─┘└┘└┐││││.└┐┌┐└┘└┘│└┐└┐└─┐└┐││││││┌┘└┘┌┐┌┐│┌┘│┌┘│││┌──┘│┌──┐┌───┘XXXXXXX
# XXX┌─┘└┘┌─┐│││└─┐│┌┐┌─┘│└─┐└┐└┘└┐┌─┐.┌┘││┌─┘│└┘│└─┐│└┐│┌┐.││││.┌┐.└────┐││└┘└┐┌┘│└┐┌──┘.└┐│┌┐│┌┘│││└┘│└───┘└┘└┘└┐││┌┘└┘└───┘└─┐│└───┐XXXXXXX
# XXX└─┐┌┐│┌┘└┘└┐X└┘│└┘┌┐└──┘┌┘┌──┘│X└┐└┐└┘└┐┌┘┌─┘.┌┘└┐│││└┐│││└┐│└─┐┌──┐│││┌──┘└─┘┌┘└┐┌┐┌┐││││││┌┘│└─┐└┐┌┐┌──┐┌─┐└┘└┘┌┐┌─┐┌────┘│┌───┘XXXXXXX
# XXXXX└┘└┘└─┐┌─┘┌──┘┌┐│└────┘X│┌┐┌┘┌─┘.└─┐┌┘└┐│.┌┐└┐┌┘││└┐││││┌┘└┐┌┘└┐┌┘││││┌┐┌┐┌┐└┐┌┘││││││││││└┐│┌┐│┌┘││└─┐│└┐│┌┐┌─┘└┘┌┘└────┐│└──┐XXXXXXXX
# XX┌┐┌┐┌┐X┌─┘└──┘┌┐┌┘││┌─────┐└┘└┘┌┘┌┐┌┐┌┘└┐┌┘└┐││┌┘│┌┘└┐│││││└┐┌┘└┐┌┘│┌┘││││││││└┐│└┐│││└┘│││││┌┘│││││┌┘│┌┐│└┐│└┘│└───┐└┐┌┐┌──┘└───┘XXXXXXXX
# XX│└┘└┘└─┘┌┐┌─┐┌┘││X││└────┐│X┌──┘┌┘││└┘┌─┘└─┐││└┘X└┘X┌┘│││││┌┘│┌┐││┌┘└┐└┘││└┘││┌┘└┐││││X┌┘│└┘││┌┘│││└┘X└┘│└┐└┘┌┐└┐┌──┘┌┘││└──────┐XXXXXXXXX
# XX└──┐┌┐┌┐│└┘┌┘└┐││┌┘│┌──┐┌┘└─┘┌┐┌┘X│└─┐└┐┌┐┌┘│└──┐X┌┐└┐│└┘││└┐└┘│└┘└─┐└┐┌┘└─┐││└┐┌┘││││┌┘┌┘┌─┘│└┐││└───┐X└─┘┌─┘│┌┘└──┐└┐││┌┐┌┐┌┐┌┘XXXXXXXXX
# XX┌┐┌┘│└┘│└┐X└──┘└┘└┐││┌┐└┘┌─┐┌┘│└─┐│┌┐│┌┘││└┐│┌──┘┌┘└─┘└─┐└┘X│┌┐└─┐┌┐│┌┘└┐┌┐││└┐││┌┘││││┌┘┌┘┌┐│┌┘│└─┐┌─┘┌───┘┌─┘└┐┌─┐└┐││└┘└┘└┘└┘XXXXXXXXXX
# ┌─┘└┘┌┘X┌┘┌┘┌────┐X┌┘│└┘└──┘X││X└─┐│││││└┐││┌┘│└─┐X└┐┌┐┌┐┌┘X┌─┘││┌┐││└┘└─┐││└┘└┐│││└┐││││└┐│┌┘│││┌┘┌─┘└──┘┌───┘┌┐┌┘└┐│┌┘│└────┐XXXXXXXXXXXXX
# └┐┌──┘XX│┌┘┌┘┌┐┌┐└─┘┌┘X┌─────┘└──┐└┘││└┘X││││X│┌─┘┌─┘││││└┐┌┘┌┐│└┘└┘└┐┌──┘│└──┐│││└┐└┘└┘│┌┘││┌┘││└┐└┐┌─┐┌┐└────┘│└┐┌┘└┘┌┘┌┐┌──┘XXXXXXXXXXXXX
# X││XX┌┐┌┘└┐└┐││││┌┐┌┘┌┐└─┐┌┐┌┐┌┐┌┘X┌┘│X┌─┘││└┐└┘┌─┘┌┐││││┌┘│┌┘│└──┐┌─┘└─┐┌┘┌┐┌┘││└┐│┌───┘└┐││└┐││┌┘X││X└┘└┐┌┐┌┐┌┘X│└─┐X└─┘└┘XXXXXXXXXXXXXXXX
# X└┘┌─┘└┘┌┐│┌┘│└┘└┘└┘┌┘└─┐└┘│││││└─┐└┐│┌┘┌┐│└┐└─┐│┌┐││││││└┐│└┐└┐┌─┘│┌┐┌┐││┌┘└┘┌┘└┐│││┌──┐┌┘└┘┌┘│└┘X┌┘└┐┌┐┌┘│└┘└┘┌┐│┌┐└────┐XXXXXXXXXXXXXXXXX
# XXX└───┐│└┘└─┘X┌┐┌──┘┌─┐└──┘││││┌─┘X└┘│┌┘││X│┌─┘││││└┘│││┌┘│┌┘┌┘└─┐└┘│││││└──┐└──┘││││┌─┘└─┐X└┐└─┐┌┘┌┐└┘│└┐└─┐┌┐││└┘└┐┌─┐┌┘XXXXXXXXXXXXXXXXX
# XXXX┌──┘└┐X┌───┘└┘┌─┐└┐└┐┌┐┌┘││└┘X┌───┘│X└┘┌┘└─┐└┘│└┐┌┘│││┌┘│X│┌─┐└─┐││││└┐┌─┘┌─┐X└┘││└────┘┌┐│┌┐│└─┘│┌─┘X│┌┐└┘└┘└──┐└┘X│└───┐XXXXXXXXXXXXXX
# XXXX│┌┐┌┐└┐│┌─┐┌┐┌┘┌┘┌┘┌┘│││┌┘└──┐└─┐┌┐└─┐┌┘┌──┘┌┐│┌┘└┐│││└┐└┐│└┐│┌┐│││└┘┌┘└──┘┌┘┌┐X└┘┌─────┘└┘││└─┐┌┘└──┐└┘│┌──┐┌──┘┌┐┌┘┌┐┌─┘XXXXXXXXXXXXXX
# XXXX└┘└┘│┌┘││┌┘│││┌┘┌┘X└┐│││└┐┌─┐└┐┌┘││┌┐│└┐└─┐┌┘└┘│┌┐││││X└┐││┌┘││└┘└┘┌─┘┌┐┌┐┌┘X│└──┐└──┐┌┐┌┐┌┘│┌─┘└┐┌──┘┌┐│└─┐│└───┘│└┐│└┘XXXXXXXXXXXXXXXX
# XXXXX┌──┘│X└┘└┐│└┘└─┘XXX└┘││X└┘┌┘┌┘└┐││││└┐│┌┐│└┐┌┐││└┘│└┘┌─┘││└┐│└───┐│┌┐│└┘│└──┘┌┐┌┘X┌┐└┘│││└┐│└┐┌┐│└───┘││┌─┘│┌┐┌┐┌┘X└┘XXXXXXXXXXXXXXXXXX
# XXXXX│┌──┘XXX┌┘│┌─┐X┌┐X┌──┘└──┐└─┘┌─┘│││└─┘││└┘X││└┘└─┐│┌┐└┐┌┘│┌┘│┌──┐│││└┘X┌┘┌┐┌─┘││┌─┘└──┘││┌┘│┌┘│└┘┌┐┌─┐││└─┐││└┘│└─┐XXXXXXXXXXXXXXXXXXXX
# XXXXX└┘XXXXXX│┌┘└┐└─┘└┐└─┐┌┐┌┐└┐┌─┘┌┐││└─┐X└┘X┌─┘└┐┌──┘││└─┘└┐│└┐│└─┐└┘└┘┌──┘┌┘│└─┐││└─┐┌─┐┌┘│└┐└┘X└─┐│└┘X└┘│┌┐││└─┐│┌┐│XXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXX││XX└┐┌─┐└──┘│└┘│┌┘└┐┌┘│││┌┐└─┐┌┐└──┐│└┐┌┐│└┐┌──┘└┐│└┐┌┘┌──┐└┐┌┐│X│┌─┘││┌─┘└┐││┌┘┌┘┌────┘└───┐┌┘│└┘└┐┌┘└┘└┘XXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXX└┘XX┌┘│┌┘┌┐┌┐└─┐│└┐X││X└┘└┘└┐┌┘││X┌─┘└┐└┘││┌┘└───┐└┘X││┌┘┌┐│┌┘││└┐│└┐┌┘│└┐┌┐│└┘└┐└┐│┌───┐┌─┐┌┘└┐└──┐│└─┐XXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXX│┌┘└┐│└┘└┐┌┘└─┘┌┘└───┐┌┐│└┐│└─┘┌─┐│┌─┘│└─┐┌┐┌┘┌──┘└┘┌┘└┘└┐│└┐││┌┘└┐│┌┘│└┘X┌─┘┌┘└┘X┌─┘└┐└┘┌┐└┐┌─┘│┌┐└─┐XXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXX└┘XX││X┌┐│└─┐┌─┘┌┐┌──┘││└─┘│┌─┐└┐││└─┐└┐┌┘││└┐└┐┌┐┌┐└┐X┌┐│└┐│││└─┐└┘└┐└──┐└──┘┌┐┌┐└┐┌┐└──┘│┌┘└┐┌┘││┌─┘XXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXX┌┘│┌┘└┘┌┐││┌┐││└───┘└─┐┌┘│X│┌┘└┘┌┐│┌┘└─┘│┌┘X└┘││└┐└┐││└┐│││└┐┌┘X┌─┘┌──┘X┌┐┌┘└┘└─┘││┌──┐│└┐┌┘└┐│││XXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXX└┐││┌─┐│└┘│││││┌─┐┌┐┌─┘│┌┘┌┘└─┐┌┘└┘└───┐│└┐┌──┘└┐└┐└┘│┌┘│└┘X││┌─┘┌─┘┌───┘└┘┌──┐┌┐││└─┐└┘┌┘└─┐││││XXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXX└┘││┌┘└─┐└┘│││└┐││└┘┌─┘└┐└┐┌┐│└──┐┌──┐│└┐││┌┐┌┐│┌┘┌─┘└┐└┐XX└┘└┐┌┘XX└─┐┌┐┌┐│┌─┘││││┌─┘┌┐└───┘││└┘XXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXX││└─┐┌┘┌─┘││┌┘│└─┐└─┐┌┘X││││┌──┘└─┐└┘┌┘│││││││└┐└──┐└┐└┐XX┌─┘└┐XX┌┐└┘└┘└┘└┐┌┘│││└──┘└───┐X└┘XXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXX└┘┌─┘│┌┘┌┐│└┘X│┌─┘XX││XX│││││┌┐┌┐┌┘┌┐└┐│└┘││││┌┘┌──┘X└┐└┐X└─┐┌┘┌─┘└─┐X┌───┘│┌┘││┌──┐┌┐┌┐│XXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXX└──┘└─┘│└┐XX││XXX┌┘└┐X└┘└┘│││││└─┘└┐└┘┌─┘│└┘└┐└─┐XXX└┐└┐XX└┘X└─┐┌┐└┐└───┐│└─┘││┌┐└┘└┘└┘XXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX┌┘┌┘XX└┘XXX└┐┌┘XXXXX└┘└┘│┌┐┌─┘XX│┌─┘┌──┘┌─┘XXXX└─┘XXXXXXX││└┐└────┘│┌──┘└┘└──────┐XXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXX┌─┘┌┘XXXXXXXXX└┘XXXXXXXX┌─┘│││XXXX│└┐X│┌─┐└┐XXXXXXXXXXXXXXX└┘X└─┐┌──┐│└───┐┌───────┘XXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXX└──┘XXXXXXXXXXXXXXXXXXXX│┌┐│└┘XXXX└─┘X└┘X└┐│XXXXXXXXXXXXXXXXXXXX││┌─┘│┌───┘└──┐┌┐X┌┐XXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX││└┘XXXXXXXXXXXXX┌┘│XXXXXXXXXXXXXXXXXXXX│││┌─┘└─┐┌┐┌┐┌┘│└─┘│XXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX┌─┘└┐XXXXXXXXXXXXXX└─┘XXXXXXXXXXXXXXXXXXXX└┘││┌───┘││││└─┘┌┐┌┘XXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└───┘XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└┘└┐┌┐┌┘│││┌──┘│└┐XXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX││└┘┌┘││└──┐└┐└┐XXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└┘┌─┘┌┘│┌┐┌┘X└─┘XXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└┐┌┘X│││└──┐XXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX└┘XX└┘└───┘XXXXXXXXXXXXXXXXXXXXXXXXXXXX
