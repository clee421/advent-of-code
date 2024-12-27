from typing import Dict, List, Tuple

def print_grid(grid):
    print("\n".join(["".join(row) for row in grid]))

def parse_lines_grid(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for line in lines:
        x = list(line)
        grid.append(x)

    return grid

def find_antennas(grid: List[List[int]]) -> Dict[str, List[Tuple[int, int]]]:
    antennas_map = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != "." and grid[i][j] != "#":
                loc_list = antennas_map.get(grid[i][j], [])
                loc_list.append((i, j))
                antennas_map[grid[i][j]] = loc_list

    return antennas_map

def mark_antinodes(grid: List[List[int]], locations: List[Tuple[int, int]]) -> None:
    for i in range(len(locations)):
        for j in range(1, len(locations)):
            if i == j:
                continue
            # (1, 3) <> [3, 4] | [5, 5] <> (7, 6)
            loc_1 = locations[i]
            loc_2 = locations[j]

            left_antinode_x = (loc_1[0] - loc_2[0]) + loc_1[0]
            left_antinode_y = (loc_1[1] - loc_2[1]) + loc_1[1]
            # print("marking",  (left_antinode_x, left_antinode_y))
            mark_antinode(grid, (left_antinode_x, left_antinode_y))

            right_antinode_x = (loc_2[0] - loc_1[0]) + loc_2[0]
            right_antinode_y = (loc_2[1] - loc_1[1]) + loc_2[1]
            # print("marking",  (right_antinode_x, right_antinode_y))
            mark_antinode(grid, (right_antinode_x, right_antinode_y))

def mark_antinodes_2(grid: List[List[int]], locations: List[Tuple[int, int]]) -> None:
    for i in range(len(locations)):
        for j in range(1, len(locations)):
            if i == j:
                continue
            # (1, 3) <> [3, 4] | [5, 5] <> (7, 6)
            loc_1 = locations[i]
            loc_2 = locations[j]


            direction_x = loc_1[0] - loc_2[0]
            direction_y = loc_1[1] - loc_2[1]
            pos_x = loc_1[0]
            pos_y = loc_1[1]
            mark_antinode(grid, (pos_x, pos_y))
            while is_antinode_valid(grid, (direction_x + pos_x, direction_y + pos_y)):
                mark_antinode(grid, (direction_x + pos_x, direction_y + pos_y))
                pos_x += direction_x
                pos_y += direction_y

            direction_x = loc_2[0] - loc_1[0]
            direction_y = loc_2[1] - loc_1[1]
            pos_x = loc_2[0]
            pos_y = loc_2[1]
            mark_antinode(grid, (pos_x, pos_y))
            while is_antinode_valid(grid, (direction_x + pos_x, direction_y + pos_y)):
                mark_antinode(grid, (direction_x + pos_x, direction_y + pos_y))
                pos_x += direction_x
                pos_y += direction_y


def is_antinode_valid(grid: List[List[int]], loc: Tuple[int, int]) -> bool:
    # print("loc", loc)
    y = loc[0]
    x = loc[1]

    # print("y", y, "x", x)
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[y]):
        return False

    if grid[y][x] != "#" and grid[y][x] != ".":
        print("WARNING: Overwriting antenna", grid[y][x], "at", (y, x))

    return True

def mark_antinode(grid: List[List[int]], loc: Tuple[int, int]) -> None:
    if not is_antinode_valid(grid, loc):
        return

    # y = loc[0]
    # x = loc[1]
    # if grid[y][x] != "#" and grid[y][x] != ".":
    #     return

    grid[loc[0]][loc[1]] = "#"

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))
    antennas_map = find_antennas(grid)

    for antenna in antennas_map:
        # print("Working on", antenna, antennas_map[antenna])
        mark_antinodes(grid, antennas_map[antenna])

    print_grid(grid)
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                count += 1

    print("Count:", count)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))
    antennas_map = find_antennas(grid)

    for antenna in antennas_map:
        # print("Working on", antenna, antennas_map[antenna])
        mark_antinodes_2(grid, antennas_map[antenna])

    print_grid(grid)
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                count += 1

    print("Count:", count)