from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return [list(l) for l in lines]

def traverse_maze(maze: List[List[str]], start_pos: Tuple[int, int] = (0, 0), start_dir: Tuple[int, int] = (0, 1)) -> List[Tuple[int, int]]:
    next_direction_map = {
        (0, 1): {
            "|": [(-1, 0), (1, 0)],
            "/": [(-1, 0)],
            "\\": [(1, 0)],
        },
        (0, -1): {
            "|": [(-1, 0), (1, 0)],
            "/": [(1, 0)],
            "\\": [(-1, 0)],
        },
        (-1, 0): {
            "-": [(0, -1), (0, 1)],
            "/": [(0, 1)],
            "\\": [(0, -1)],
        },
        (1, 0): {
            "-": [(0, -1), (0, 1)],
            "/": [(0, -1)],
            "\\": [(0, 1)],
        },
    }

    # the algo assumes we don't look
    seen = set([(start_pos, start_dir)])
    queue = [(start_pos, start_dir)]
    while queue:
        curr_pos, curr_dir = queue.pop(0)
        # print(curr_pos, curr_dir)
        current_val = maze[curr_pos[0]][curr_pos[1]]
        next_dirs = next_direction_map[curr_dir].get(current_val, [curr_dir])

        for dx, dy in next_dirs:
            x, y = curr_pos[0] + dx, curr_pos[1] + dy

            if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[x]):
                continue

            if ((x, y), (dx, dy)) in seen:
                continue

            seen.add(((x, y), (dx, dy)))
            queue.append(((x, y), (dx, dy)))

    no_directions = list(set([e[0] for e in list(seen)]))

    return no_directions

def max_energized_tiles(maze: List[List[str]]) -> int:
    up, down, left, right = (-1, 0), (1, 0), (0, -1), (0, 1)

    max_tiles = 0
    for col in range(len(maze[0])):
        # print(f"down: {col} / {len(maze[0])}")
        travelled_paths = traverse_maze(maze, (0, col), down)
        max_tiles = max(max_tiles, len(travelled_paths))

    n = len(maze) - 1
    for col in range(len(maze[n])):
        # print(f"up: {col} / {len(maze[n])}")
        travelled_paths = traverse_maze(maze, (n, col), up)
        max_tiles = max(max_tiles, len(travelled_paths))

    for row in range(len(maze)):
        # print(f"right: {row} / {len(maze)}")
        travelled_paths = traverse_maze(maze, (row, 0), right)
        max_tiles = max(max_tiles, len(travelled_paths))

    for row in range(len(maze)):
        # print(f"left: {row} / {len(maze)}")
        travelled_paths = traverse_maze(maze, (row, 0), left)
        max_tiles = max(max_tiles, len(travelled_paths))

    return max_tiles

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    maze = parse_inputs(options.get("filepath", args[0]))

    travelled_paths = traverse_maze(maze)

    for tp in travelled_paths:
        maze[tp[0]][tp[1]] = "#"

    # print("\n".join(["".join(r) for r in maze]))

    print(f"Tiles: {len(travelled_paths)}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    maze = parse_inputs(options.get("filepath", args[0]))

    max_tiles = max_energized_tiles(maze)

    print(f"Tiles: {max_tiles}")