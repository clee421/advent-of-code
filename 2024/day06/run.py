from typing import Dict, List

direction = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

def travel(grid, pos) -> bool:
    blocker_map = {}
    current_direction = 0
    x, y = pos[0], pos[1]
    while x >= 0 and x < len(grid) and y >= 0 and y < len(grid[x]):
        # print("CURRENT", x, y)
        if grid[x][y] != "#":
            grid[x][y] = "X"
        next_x, next_y = x + direction[current_direction][0], y + direction[current_direction][1]
        # print("NEXT", next_x, next_y)
        if next_x < 0 or next_x >= len(grid) or next_y < 0 or next_y >= len(grid[next_x]):
            break

        if grid[next_x][next_y] == "#":
            c = blocker_map.get((next_x, next_y), 0)
            if c > 2:
                return True

            blocker_map[(next_x, next_y)] = c+1
            # print("Direction Change", current_direction)
            current_direction = (current_direction + 1) % 4
            # print("New direction", current_direction)
            continue

        x, y = next_x, next_y

        # print("DEBUG ==========")
        # print("\n".join(list(map(lambda x: "".join(x), grid))))

    return False

def parse_lines_grid(filepath: str) -> List[List[int]]:
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

    pos = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "^":
                pos = (i, j)
                break

    travel(grid, pos)
    # print("CURRENT STATE")
    # print("\n".join(list(map(lambda x: "".join(x), grid))))
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                count += 1

    print("Count:", count)


def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))

    pos = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "^":
                pos = (i, j)
                break

    # copy_grid = list(map(lambda x: x.copy(), grid))
    # copy_grid[7][7] = "#"
    # looped = travel(copy_grid, pos)

    loop_count = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != "^":
                print("Testing", (i, j))
                copy_grid = list(map(lambda x: x.copy(), grid))
                copy_grid[i][j] = "#"

                looped = travel(copy_grid, pos)
                if looped:
                    loop_count += 1
    # print("CURRENT STATE")
    # print("\n".join(list(map(lambda x: "".join(x), grid))))

    # This actually took some time to run
    print("Count:", loop_count)