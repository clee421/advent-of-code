from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return lines

def can_access(point: Tuple[int, int], grid: List[str]) -> bool:
    if grid[point[0]][point[1]] != "@":
        return False

    _limit = 4
    adj_points = 0

    adj_positions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]

    for ap in adj_positions:
        nx, ny = point[0] + ap[0], point[1] + ap[1]
        if nx < 0 or nx >= len(grid) or ny < 0 or ny >= len(grid[nx]):
            continue

        if grid[nx][ny] == "@":
            adj_points += 1

    return adj_points < _limit

def find_forklift_access_points(grid: List[str]) -> List[Tuple[int, int]]:
    points = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if can_access((i, j), grid):
                points.append((i, j))

    return points

def remove_forklift_access_points(_str_grid: List[str]) -> List[Tuple[int, int]]:
    grid = [list(l) for l in _str_grid]

    all_points = []
    have_points_to_remove = True

    while have_points_to_remove:
        points = find_forklift_access_points(grid)
        if len(points) < 1:
            have_points_to_remove = False

        all_points.extend(points)
        for p in points:
            grid[p[0]][p[1]] = "."

    return all_points

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    points = find_forklift_access_points(grid)
    print(f"Total: {len(points)}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    points = remove_forklift_access_points(grid)
    print(f"Total: {len(points)}")