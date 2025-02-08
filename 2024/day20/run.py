import time
from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for l in lines:
        grid.append(list(l))

    return grid

def find_start_end(maze: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    start, end = None, None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                start = (i, j)
            if maze[i][j] == "E":
                end = (i, j)

    return (start, end)\

def find_shortest_path(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    seen = {start: 0}
    queue = [start]
    while len(queue) > 0:
        curr_pos = queue.pop(0)
        if curr_pos == end:
            return seen[curr_pos]

        for d in directions:
            x, y = curr_pos[0] + d[0], curr_pos[1] + d[1]

            if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[x]):
                continue

            if maze[x][y] == "#" or (x, y) in seen:
                continue

            curr_val = seen[curr_pos]
            queue.append((x, y))
            seen[(x, y)] = curr_val + 1

    return -1

def is_passable_wall(maze: List[List[str]], pos: Tuple[int, int]) -> bool:
    x, y = pos[0], pos[1]
    if maze[x][y] == ".":
        return False

    return (
        (maze[x][y-1] == "." and maze[x][y+1] == ".") or
        (maze[x-1][y] == "." and maze[x+1][y] == ".")
    )


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    # for row in grid:
    #     print(row)

    res = find_start_end(grid)
    start, end = res[0], res[1]

    # we don't need start and end anymore since we have it
    grid[start[0]][start[1]] = "."
    grid[end[0]][end[1]] = "."

    counter = {}
    super_saver_cheats = 0
    standard_steps = find_shortest_path(grid, start, end)
    print("Steps:", standard_steps)

    start_time = time.time()
    elapsed_time = start_time + 5
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[i])-1):
            if time.time() > elapsed_time:
                now = time.time()
                elapsed_time = now + 10
                print(f"Current value: {(i, j)} of {len(grid)-1} by {len(grid[i])-1}. Total elapsed time {now - start_time}")
                print(f"So far has {super_saver_cheats} with over 99 saved")

            if is_passable_wall(grid, (i, j)):
                cp_grid = list(map(lambda x: x.copy(), grid))
                cp_grid[i][j] = "."
                maybe_shorter_steps = find_shortest_path(cp_grid, start, end)
                saved_steps = standard_steps - maybe_shorter_steps
                c = counter.get(saved_steps, 0)
                counter[saved_steps] = c + 1

                if saved_steps >= 100:
                    # print(f"{(i, j)} is passable and saved {saved_steps}")
                    super_saver_cheats += 1

    # sorted_saved_steps = sorted(list(counter.items()), key=lambda x: x[0])
    # for s in sorted_saved_steps:
    #     print(f"{s[1]} cheats saved {s[0]} steps")


    print("Save at least 100 steps:", super_saver_cheats)



def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    print("\n".join(inputs))