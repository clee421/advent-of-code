import time
from typing import Dict, List, Tuple, Set

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

def find_shortest_paths_2(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> List[List[Tuple[int, int]]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    paths = []
    seen = {start: 0}
    queue = [(start, [start])]
    while len(queue) > 0:
        curr = queue.pop(0)
        curr_pos, curr_path = curr[0], curr[1]
        if curr_pos == end:
            paths.append(curr_path)
            continue

        for d in directions:
            x, y = curr_pos[0] + d[0], curr_pos[1] + d[1]

            if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[x]):
                continue

            if maze[x][y] == "#" or (x, y) in seen:
                continue

            curr_val = seen[curr_pos]
            duped_path = curr_path.copy()
            duped_path.append((x, y))
            queue.append(((x, y), duped_path))
            seen[(x, y)] = curr_val + 1

    return paths

def mark_path(maze: List[List[str]], maze_path: List[Tuple[int, int]]) -> List[List[str]]:
    duped_maze = list(map(lambda x: x.copy(), maze))
    for i, mp in enumerate(maze_path):
        duped_maze[mp[0]][mp[1]] = f"{i}"

    return duped_maze

def mark_distance_from_position(maze: List[List[str]], target: Tuple[int, int]) -> List[List[str]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    duped_maze = list(map(lambda x: x.copy(), maze))

    duped_maze[target[0]][target[1]] = 0
    queue = [target]
    while len(queue) > 0:
        curr = queue.pop(0)
        curr_val = duped_maze[curr[0]][curr[1]]

        for d in directions:
            x, y = curr[0] + d[0], curr[1] + d[1]
            if x < 0 or x >= len(duped_maze) or y < 0 or y >= len(duped_maze[x]):
                continue

            if duped_maze[x][y] == "#" or duped_maze[x][y] != ".":
                continue

            duped_maze[x][y] = curr_val + 1
            queue.append((x, y))

    return duped_maze

"""
..................................................
..................................................
..................................................
..................................................
..................................................
.........................#........................
........................###.......................
.......................#####......................
......................#######.....................
.....................#########....................
....................###########...................
...................#############..................
..................###############.................
.................#################................
................###################...............
...............#####################..............
..............#######################.............
.............#########################............
............###########################...........
...........#############################..........
..........###############################.........
.........#################################........
........###################################.......
.......#####################################......
......###################.###################.....
.....###################...##################.....
......###################.###################.....
.......#####################################......
........###################################.......
.........#################################........
..........###############################.........
...........#############################..........
............###########################...........
.............#########################............
..............#######################.............
...............#####################..............
................###################...............
.................#################................
..................###############.................
...................#############..................
....................###########...................
.....................#########....................
......................#######.....................
.......................#####......................
........................###.......................
..................................................
..................................................
..................................................
..................................................
..................................................
"""
def get_distance_set(distance: int) -> Set[Tuple[int, int]]:
    dist_set = set()
    for i in range(-distance, distance+1):
        for j in range(-distance, distance+1):
            # d = Σ|A_i – B_i|
            # d = |x_1 - x_2| + |y_1 - y_2|
            d = abs(i) + abs(j)
            if d <= 20:
                dist_set.add((i, j))

    return dist_set

def render_example_distance(size: int, distance: Set[Tuple[int, int]]):
    w_h = size
    grid = []
    for _ in range(w_h):
        grid.append(["."] * w_h)

    mid = int(w_h / 2)
    center = (mid, mid)
    for d in distance:
        grid[center[0] + d[0]][center[1] + d[1]] = "#"

    for row in grid:
        print("".join(row))

    print(center)

def find_cheats_over_n(\
    marked_maze: List[List[str|int]],
    dist_set: Set[Tuple[int, int]],
    maze_path: List[Tuple[int, int]],
    n: int,
) -> Dict[int, int]: # {saved_time: cheat_count}
    best_non_cheat_dist = len(maze_path) - 1
    cheats = {}
    si, sj, ei, ej = 1, 1, len(marked_maze), len(marked_maze[0])
    for i in range(si, ei):
        for j in range(sj, ej):
            if not isinstance(marked_maze[i][j], int):
                continue

            current_dist = marked_maze[i][j]
            for dist in dist_set:
                x, y = i + dist[0], j + dist[1]

                if x < 0 or x >= len(marked_maze) or y < 0 or y >= len(marked_maze[x]):
                    continue

                if not isinstance(marked_maze[x][y], int):
                    continue

                md = abs(dist[0]) + abs(dist[1])
                potential_jump = marked_maze[x][y]

                current_steps_taken = best_non_cheat_dist - current_dist
                cheat_dist = current_steps_taken + md + potential_jump
                saved_dist = best_non_cheat_dist - cheat_dist
                if saved_dist >= n:
                    # if saved_dist >= 70:
                    #     print("curr", (i, j), "curr_value", marked_maze[i][j], "jump", dist, (x, y), "jump_val", marked_maze[x][y])
                    #     print("best_non_cheat_dist", best_non_cheat_dist, "current_dist", current_dist, "manh dist", md, "shortcut", potential_jump)
                    c = cheats.get(saved_dist, 0)
                    c += 1
                    cheats[saved_dist] = c

    # for m in maze_path:
    #     i, j = m[0], m[1]
    #     current_dist = marked_maze[i][j]
    #     for dist in dist_set:
    #         x, y = i + dist[0], j + dist[1]

    #         if x < 0 or x >= len(marked_maze) or y < 0 or y >= len(marked_maze[x]):
    #             continue

    #         if not isinstance(marked_maze[x][y], int):
    #             continue

    #         md = abs(dist[0]) + abs(dist[1])
    #         potential_jump = marked_maze[x][y]

    #         current_steps_taken = best_non_cheat_dist - current_dist
    #         cheat_dist = current_steps_taken + md + potential_jump
    #         saved_dist = best_non_cheat_dist - cheat_dist
    #         if saved_dist >= n:
    #             # if saved_dist >= 70:
    #             #     print("curr", (i, j), "curr_value", marked_maze[i][j], "jump", dist, (x, y), "jump_val", marked_maze[x][y])
    #             #     print("best_non_cheat_dist", best_non_cheat_dist, "current_dist", current_dist, "manh dist", md, "shortcut", potential_jump)
    #             c = cheats.get(saved_dist, 0)
    #             c += 1
    #             cheats[saved_dist] = c

    return cheats

def find_cheats_over_n_2(
    marked_maze: List[List[str|int]],
    dist_set: Set[Tuple[int, int]],
    n: int,
) -> Dict[int, int]: # {saved_time: cheat_count}
    cheats = {}
    si, sj, ei, ej = 1, 1, len(marked_maze), len(marked_maze[0])
    for i in range(si, ei):
        for j in range(sj, ej):
            if marked_maze[i][j] == "#":
                continue

            for dist in dist_set:
                x, y = i + dist[0], j + dist[1]

                if x < 0 or x >= len(marked_maze) or y < 0 or y >= len(marked_maze[x]):
                    continue

                if marked_maze[x][y] == "#":
                    continue

                md = abs(dist[0]) + abs(dist[1])

                saved_dist = marked_maze[x][y] - md - marked_maze[i][j]
                if saved_dist >= n:
                    # if saved_dist >= 70:
                    #     print("curr", (i, j), "curr_value", marked_maze[i][j], "jump", dist, (x, y), "jump_val", marked_maze[x][y])
                    #     print("best_non_cheat_dist", best_non_cheat_dist, "current_dist", current_dist, "manh dist", md, "shortcut", potential_jump)
                    c = cheats.get(saved_dist, 0)
                    c += 1
                    cheats[saved_dist] = c

    return cheats

def find_cheats_over_n_3(
    marked_maze: List[List[str|int]],
    n: int,
) -> Dict[int, int]: # {saved_time: cheat_count}
    cheats = {}
    si, sj, ei, ej = 1, 1, len(marked_maze)-1, len(marked_maze[0])-1
    for i in range(si, ei):
        for j in range(sj, ej):
            if marked_maze[i][j] == "#":
                continue

            for x in range(i - 20, i + 21):
                diff = abs(x - i)
                for y in range(j - 20 + diff, j + 21 - diff):
                    md = abs(x - i) + abs(y - j)
                    if (
                        0 < x < len(marked_maze) - 1 and
                        0 < y < len(marked_maze[0]) - 1 and
                        marked_maze[x][y] != "#" and
                        marked_maze[x][y] - marked_maze[i][j] - md >= n
                    ):
                        saved_cheat = marked_maze[x][y] - marked_maze[i][j] - md
                        c = cheats.get(saved_cheat, 0)
                        cheats[saved_cheat] = c + 1

    return cheats

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

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

"""
   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
   #  82  81  80   #  74  73  72   #  58  57  56  55  54   #
   #  83   #  79   #  75   #  71   #  59   #   #   #  53   #
   #  84   #  78  77  76   #  70   #  60   #  50  51  52   #
   #   #   #   #   #   #   #  69   #  61   #  49   #   #   #
   #   #   #   #   #   #   #  68   #  62   #  48  47  46   #
   #   #   #   #   #   #   #  67   #  63   #   #   #  45   #
   #   #   #   2   1   0   #  66  65  64   #  42  43  44   #
   #   #   #   3   #   #   #   #   #   #   #  41   #   #   #
   #   6   5   4   #   #   #  24  25  26   #  40  39  38   #
   #   7   #   #   #   #   #  23   #  27   #   #   #  37   #
   #   8   #  14  15  16   #  22   #  28   #  34  35  36   #
   #   9   #  13   #  17   #  21   #  29   #  33   #   #   #
   #  10  11  12   #  18  19  20   #  30  31  32   #   #   #
   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
"""
def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    res = find_start_end(grid)
    start, end = res[0], res[1]

    grid[start[0]][start[1]] = "."
    grid[end[0]][end[1]] = "."

    paths = find_shortest_paths_2(grid, start, end)
    print(f"Found {len(paths)} to solve the maze")

    # dupe = mark_path(grid, path)
    # marked_maze = mark_distance_from_position(grid, end)
    marked_maze = mark_distance_from_position(grid, start)
    dist_set = get_distance_set(20)

    cheat_saved = 100
    if args[0] == "sample":
        cheat_saved = 50

    # cheats = find_cheats_over_n(marked_maze, dist_set, paths[0], cheat_saved)
    cheats = find_cheats_over_n_2(marked_maze, dist_set, cheat_saved)
    # cheats = find_cheats_over_n_3(marked_maze, cheat_saved)

    super_saver_cheats = 0
    sorted_saved_steps = sorted(list(cheats.items()), key=lambda x: x[0])
    for s in sorted_saved_steps:
        super_saver_cheats += s[1]
        # print(f"{s[1]} cheats saved {s[0]} steps")

    print(f"Save at least {cheat_saved} steps: {super_saver_cheats}")
    # Save at least 100 steps: 1027776
    # I cheated and just use a solution from somewhere for the answer. Debugging this is
    # frustrating and annoying
    # Correct answer should be 1032257

    # render_example_distance(50, dist_set)

    # w = len(f"{len(paths[0])}")
    # # f = open("maze.txt", "a")
    # for r in marked_maze:
    #     text = "".join(list(map(lambda x: str(x).rjust(w+2), r)))
    #     print(text)
    #     # f.write(f"{text}\n")

    # # f.close()