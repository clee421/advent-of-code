import time
from heapq import heappush, heappop
from typing import Dict, List, Tuple, Set

def parse_inputs(filepath: str) -> List[List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for l in lines:
        grid.append(list(l))

    return grid

def find_start_end(maze: List[List[str]]) -> List[Tuple[int, int]]:
    start, end = None, None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                start = (i, j)

            if maze[i][j] == "E":
                end = (i, j)

            if start is not None and end is not None:
                break

    return [start, end]

# def find_best_path(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
#     DIRECTION_MAP = {
#         (0, 1): [(-1, 0), (1, 0)],
#         (1, 0): [(0, -1), (0, 1)],
#         (0, -1): [(1, 0), (-1, 0)],
#         (-1, 0): [(0, 1), (0, -1)],
#     }


#     time_start = time.time()
#     elapsed_time = time_start + 5

#     seen = set()
#     min_points = float('inf')
#     current_direction = (0, 1)
#     current_points = 0
#     item = [start, current_points, current_direction]
#     seen.add((start, current_direction))

#     queue: List[Tuple[Tuple[int, int], int, Tuple[int, int], set]] = [item]
#     while len(queue) > 0:
#     # for i in range(50):
#         if time.time() > elapsed_time:
#             now = time.time()
#             elapsed_time = now + 10
#             print(queue)
#             print(f"Queue is size: {len(queue)}. Total elapsed time {now - time_start}")
#             print(f"Top of queue is {queue[0]}")

#         curr = queue.pop(0)
#         curr_pos, curr_points, curr_direction = curr[0], curr[1], curr[2]

#         x, y = curr_pos[0], curr_pos[1]
#         if maze[x][y] == "#":
#             continue

#         if (x, y) == end:
#             print("curr_points", curr_points, "min_points", min_points)
#             min_points = min(min_points, curr_points)

#         n_x, n_y = x + curr_direction[0], y + curr_direction[1]
#         if ((n_x, n_y), curr_direction) not in seen:
#             # print(i, "seen", seen, "adding", [(n_x, n_y), curr_points + 1, curr_direction])
#             seen.add(((n_x, n_y), curr_direction))
#             queue.append([(n_x, n_y), curr_points + 1, curr_direction])

#         for expensive_turn in DIRECTION_MAP[curr_direction]:
#             if ((x, y), expensive_turn) not in seen:
#                 # print(i, "seen", seen, "adding", [(x, y), curr_points + 1000, expensive_turn])
#                 seen.add(((x, y), expensive_turn))
#                 queue.append([(x, y), curr_points + 1000, expensive_turn])

#     return min_points

def find_best_path_2(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    DIRECTION_MAP = {
        (0, 1): [(-1, 0), (1, 0)],
        (1, 0): [(0, -1), (0, 1)],
        (0, -1): [(1, 0), (-1, 0)],
        (-1, 0): [(0, 1), (0, -1)],
    }

    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = "."

    queue = [(start, (0, 1), 0)]
    while len(queue) > 0:
        curr = queue.pop(0)
        curr_pos, curr_direction, expected_points = curr[0], curr[1], curr[2]

        curr_points = maze[curr_pos[0]][curr_pos[1]]
        if expected_points > curr_points:
            # if this happens then a position in the queue has found a cheaper path
            continue

        nx, ny = curr_pos[0] + curr_direction[0], curr_pos[1] + curr_direction[1]
        potential_points = curr_points + 1
        if maze[nx][ny] != "#" and (maze[nx][ny] == "." or potential_points < maze[nx][ny]):
            queue.append(((nx, ny), curr_direction, potential_points))
            maze[nx][ny] = potential_points

        for expensive_turn in DIRECTION_MAP[curr_direction]:
            nx, ny = curr_pos[0] + expensive_turn[0], curr_pos[1] + expensive_turn[1]
            potential_points = curr_points + 1 + 1000
            if maze[nx][ny] != "#" and (maze[nx][ny] == "." or potential_points < maze[nx][ny]):
                queue.append(((nx, ny), expensive_turn, potential_points))
                maze[nx][ny] = potential_points

    # for row in maze:
    #     print(list(map(lambda x: f"{x}".zfill(5) if x != "#" else "#####", row)))

    return maze[end[0]][end[1]]

def write_maze(maze: List[List[str]], marks: Set[Tuple[int, int]], name: str):
    f = open(f"{name}.txt", "a")

    for t in marks:
        maze[t[0]][t[1]] = "O"

    for row in maze:
        f.write(f"{"".join(row)}\n")

    f.close()

# def find_tiles_of_best_paths(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
#     DIRECTION_MAP = {
#         (0, 1): [(-1, 0), (1, 0)],
#         (1, 0): [(0, -1), (0, 1)],
#         (0, -1): [(1, 0), (-1, 0)],
#         (-1, 0): [(0, 1), (0, -1)],
#     }

#     time_start = time.time()
#     elapsed_time = time_start + 5

#     min_points = float('inf')
#     min_paths = []
#     current_direction = (0, 1)
#     current_points = 0
#     item = [start, current_points, current_direction, set([start])]

#     queue: List[Tuple[Tuple[int, int], int, Tuple[int, int], set], Set] = [item]
#     while len(queue) > 0:
#         if time.time() > elapsed_time:
#             now = time.time()
#             elapsed_time = now + 10
#             print(f"Queue is size: {len(queue)}. Total elapsed time {now - time_start}")
#             write_maze(maze, queue[0][3], int(now - time_start))

#         curr = queue.pop(0)
#         curr_pos, curr_points, curr_direction, seen = curr[0], curr[1], curr[2], curr[3]

#         x, y = curr_pos[0], curr_pos[1]

#         if (x, y) == end:
#             # print("curr_points", curr_points, "min_points", min_points)
#             if curr_points < min_points:
#                 min_points = curr_points
#                 min_paths = [seen]
#             elif curr_points == min_points:
#                 min_paths.append(seen)

#         # because we copy seen, we have to do the expensive turns first before the straight path
#         for expensive_turn in DIRECTION_MAP[curr_direction]:
#             nx, ny = x + expensive_turn[0], y + expensive_turn[1]
#             if maze[nx][ny] != "#" and (nx, ny) not in seen:
#                 turn_seen = seen.copy()
#                 turn_seen.add((nx, ny))
#                 queue.append([(nx, ny), curr_points + 1 + 1000, expensive_turn, turn_seen])

#         nx, ny = x + curr_direction[0], y + curr_direction[1]
#         if maze[nx][ny] != "#" and (nx, ny) not in seen:
#             seen.add((nx, ny))
#             queue.append([(nx, ny), curr_points + 1, curr_direction, seen])

#     # print(min_points)
#     # print(min_paths)

#     tile_set = set()
#     for mp in min_paths:
#         tile_set.update(mp)

#     # for t in tile_set:
#     #     maze[t[0]][t[1]] = "O"

#     # for row in maze:
#     #     print("".join(row))

#     return len(tile_set)

# def find_tiles_of_best_paths_2(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
#     DIRECTION_MAP = {
#         (0, 1): [(-1, 0), (1, 0)],
#         (1, 0): [(0, -1), (0, 1)],
#         (0, -1): [(1, 0), (-1, 0)],
#         (-1, 0): [(0, 1), (0, -1)],
#     }

#     time_start = time.time()
#     elapsed_time = time_start + 5
#     print_time = time_start + 60

#     min_points = float('inf')
#     min_paths = []
#     current_direction = (0, 1)
#     current_points = 0

#     # done_count = 0
#     priority_queue: List[int, Tuple[Tuple[int, int], Tuple[int, int], set], Set] = []
#     heappush(priority_queue, (current_points, start, current_direction, set([start])))
#     while len(priority_queue) > 0:
#         curr = heappop(priority_queue)
#         curr_points, curr_pos, curr_direction, seen = curr[0], curr[1], curr[2], curr[3]

#         if time.time() > elapsed_time:
#             now = time.time()
#             elapsed_time = now + 10
#             print(f"Queue is size: {len(priority_queue)}. Total elapsed time {now - time_start}")
#             if now > print_time:
#                 print_time = now + 60
#                 write_maze(maze, seen, int(now - time_start))
#         # print("curr", curr_points, curr_pos, curr_direction)
#         if curr_points > min_points:
#             continue

#         x, y = curr_pos[0], curr_pos[1]

#         if (x, y) == end:
#             # done_count += 1
#             # print("done! curr_points", curr_points)
#             # write_maze(maze, seen, f"done-{done_count}")
#             if curr_points < min_points:
#                 min_points = curr_points
#                 min_paths = [seen]
#             elif curr_points == min_points:
#                 min_paths.append(seen)

#         for expensive_turn in DIRECTION_MAP[curr_direction]:
#             nx, ny = x + expensive_turn[0], y + expensive_turn[1]
#             # print((nx, ny), maze[nx][ny], expensive_turn, seen)
#             if maze[nx][ny] != "#" and (nx, ny) not in seen:
#                 turn_seen = seen.copy()
#                 turn_seen.add((nx, ny))
#                 p = curr_points + 1 + 1000
#                 heappush(priority_queue, (p, (nx, ny), expensive_turn, turn_seen))

#         nx, ny = x + curr_direction[0], y + curr_direction[1]
#         # print((nx, ny), maze[nx][ny], curr_direction, seen)
#         if maze[nx][ny] != "#" and (nx, ny) not in seen:
#             seen.add((nx, ny))
#             p = curr_points + 1
#             heappush(priority_queue, (p, (nx, ny), curr_direction, seen))

#     # print(min_points)
#     # print(min_paths)

#     tile_set = set()
#     for mp in min_paths:
#         tile_set.update(mp)

#     # for t in tile_set:
#     #     maze[t[0]][t[1]] = "O"

#     # for row in maze:
#     #     print("".join(row))

#     return len(tile_set)

# def find_best_path_3(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> Dict[Tuple[int, int], Tuple[int, Tuple[int, int]]]:
#     DIRECTION_MAP = {
#         (0, 1): [(-1, 0), (1, 0)],
#         (1, 0): [(0, -1), (0, 1)],
#         (0, -1): [(1, 0), (-1, 0)],
#         (-1, 0): [(0, 1), (0, -1)],
#     }

#     maze[start[0]][start[1]] = 0
#     maze[end[0]][end[1]] = "."

#     min_points = float("inf")
#     end_paths = []

#     queue = [(start, (0, 1), 0, {start: (0, (0, 1))})]
#     while len(queue) > 0:
#         curr = queue.pop(0)
#         curr_pos, curr_direction, expected_points, seen = curr[0], curr[1], curr[2], curr[3]

#         if curr_pos == end:
#             if expected_points < min_points:
#                 min_points = expected_points
#                 end_paths = [seen]
#             elif expected_points == min_points:
#                 end_paths.append(seen)

#         curr_points = maze[curr_pos[0]][curr_pos[1]]
#         if expected_points > curr_points:
#             # if this happens then a position in the queue has found a cheaper path
#             continue

#         for expensive_turn in DIRECTION_MAP[curr_direction]:
#             nx, ny = curr_pos[0] + expensive_turn[0], curr_pos[1] + expensive_turn[1]
#             potential_points = curr_points + 1 + 1000
#             if maze[nx][ny] != "#" and (maze[nx][ny] == "." or potential_points < maze[nx][ny]):
#                 turn_seen = seen.copy()
#                 turn_seen[(nx, ny)] = (potential_points, expensive_turn)
#                 queue.append(((nx, ny), expensive_turn, potential_points, turn_seen))
#                 maze[nx][ny] = potential_points

#         nx, ny = curr_pos[0] + curr_direction[0], curr_pos[1] + curr_direction[1]
#         potential_points = curr_points + 1
#         if maze[nx][ny] != "#" and (maze[nx][ny] == "." or potential_points < maze[nx][ny]):
#             seen[(nx, ny)] = (potential_points, curr_direction)
#             queue.append(((nx, ny), curr_direction, potential_points, seen))
#             maze[nx][ny] = potential_points

#     # in testing i found that there is only 1 best path based on the above algo
#     return end_paths[0]

# def find_tiles_of_best_paths_3(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
#     copy_maze = [r.copy() for r in maze]
#     # best_path_dict[pos] = (potential_points, curr_direction)
#     best_path_dict = find_best_path_3(copy_maze, start, end)

#     DIRECTION_MAP = {
#         (0, 1): [(-1, 0), (1, 0)],
#         (1, 0): [(0, -1), (0, 1)],
#         (0, -1): [(1, 0), (-1, 0)],
#         (-1, 0): [(0, 1), (0, -1)],
#     }

#     # time_start = time.time()
#     # elapsed_time = time_start + 5

#     queue = [(start, (0, 1), 0, {start: (0, (0, 1))})]
#     while len(queue) > 0:
#         # if time.time() > elapsed_time:
#         #     now = time.time()
#         #     elapsed_time = now + 10
#         #     print(f"Queue is size: {len(queue)}. Total elapsed time {now - time_start}")
#         #     write_maze(maze, queue[0][3], int(now - time_start))

#         curr = queue.pop(0)
#         curr_pos, curr_direction, curr_points, seen = curr[0], curr[1], curr[2], curr[3]

#         if curr_pos in best_path_dict:
#             val = best_path_dict[curr_pos]
#             if val == (curr_points, curr_direction):
#                 seen.update(best_path_dict)
#                 best_path_dict = seen

#         x, y = curr_pos[0], curr_pos[1]
#         # because we copy seen, we have to do the expensive turns first before the straight path
#         for expensive_turn in DIRECTION_MAP[curr_direction]:
#             nx, ny = x + expensive_turn[0], y + expensive_turn[1]
#             if maze[nx][ny] != "#" and (nx, ny) not in seen:
#                 potential_points = curr_points + 1 + 1000
#                 turn_seen = seen.copy()
#                 turn_seen[(nx, ny)] = (potential_points, expensive_turn)
#                 queue.append([(nx, ny), expensive_turn, potential_points, turn_seen])

#         nx, ny = x + curr_direction[0], y + curr_direction[1]
#         if maze[nx][ny] != "#" and (nx, ny) not in seen:
#             potential_points = curr_points + 1
#             seen[(nx, ny)] = (potential_points, curr_direction)
#             queue.append([(nx, ny), curr_direction, potential_points, seen])

#     return len(best_path_dict)

def find_tiles_of_best_paths_4(maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    DIRECTION_MAP = {
        (0, 1): [(-1, 0), (1, 0)],
        (1, 0): [(0, -1), (0, 1)],
        (0, -1): [(1, 0), (-1, 0)],
        (-1, 0): [(0, 1), (0, -1)],
    }

    time_start = time.time()
    elapsed_time = time_start + 5

    min_points = float('inf')
    min_paths = []
    current_direction = (0, 1)
    current_points = 0

    global_seen = {(start, current_direction): current_points}
    item = [start, current_points, current_direction, set([start])]

    queue: List[Tuple[Tuple[int, int], int, Tuple[int, int], set], Set] = [item]
    while len(queue) > 0:
        if time.time() > elapsed_time:
            now = time.time()
            elapsed_time = now + 10
            print(f"Queue is size: {len(queue)}. Total elapsed time {now - time_start}")
            write_maze(maze, queue[0][3], int(now - time_start))

        curr = queue.pop(0)
        curr_pos, curr_points, curr_direction, seen = curr[0], curr[1], curr[2], curr[3]

        x, y = curr_pos[0], curr_pos[1]

        if (x, y) == end:
            # print("curr_points", curr_points, "min_points", min_points)
            if curr_points < min_points:
                min_points = curr_points
                min_paths = [seen]
            elif curr_points == min_points:
                min_paths.append(seen)

        # because we copy seen, we have to do the expensive turns first before the straight path
        for expensive_turn in DIRECTION_MAP[curr_direction]:
            nx, ny = x + expensive_turn[0], y + expensive_turn[1]
            potential_points = curr_points + 1 + 1000

            if maze[nx][ny] != "#" and (nx, ny) not in seen:
                global_key = ((nx, ny), expensive_turn)
                if global_key in global_seen and potential_points > global_seen[global_key]:
                    continue

                global_seen[global_key] = potential_points
                turn_seen = seen.copy()
                turn_seen.add((nx, ny))
                queue.append([(nx, ny), potential_points, expensive_turn, turn_seen])

        nx, ny = x + curr_direction[0], y + curr_direction[1]
        potential_points = curr_points + 1

        if maze[nx][ny] != "#" and (nx, ny) not in seen:
            global_key = ((nx, ny), curr_direction)
            if global_key in global_seen and potential_points > global_seen[global_key]:
                continue

            global_seen[global_key] = potential_points
            seen.add((nx, ny))
            queue.append([(nx, ny), potential_points, curr_direction, seen])

    tile_set = set()
    for mp in min_paths:
        tile_set.update(mp)

    return len(tile_set)

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    maze = parse_inputs(options.get("filepath", args[0]))

    pos = find_start_end(maze)
    start, end = pos[0], pos[1]

    points = find_best_path_2(maze.copy(), start, end)

    print(f"Points: {points}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    maze = parse_inputs(options.get("filepath", args[0]))

    pos = find_start_end(maze)
    start, end = pos[0], pos[1]

    # tiles = find_tiles_of_best_paths(maze.copy(), start, end)
    tiles = find_tiles_of_best_paths_4(maze.copy(), start, end)

    print(f"Tiles: {tiles}")