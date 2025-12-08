from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return list(map(lambda l: list(l), lines))


def print_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print("".join(row))

def valid_pos(pos: Tuple[int, int], grid: List[List[str]]) -> bool:
    if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False

    return True

def split_beam(grid: List[List[str]]) -> int:
    start = None
    for i in range(len(grid[0])):
        if grid[0][i] == "S":
            start = ("S", (0, i))

    split_count = 0
    seen = set()
    queue = [start]
    while queue:
        curr = queue.pop(0)
        curr_char = curr[0]
        curr_pos = curr[1]
        match curr_char:
            case "S":
                next_pos = (curr_pos[0] + 1, curr_pos[1])
                grid[next_pos[0]][next_pos[1]] = "|"
                queue.append(("|", next_pos))
            case "|":
                next_pos = (curr_pos[0] + 1, curr_pos[1])
                if not valid_pos(next_pos, grid) or next_pos in seen:
                    continue

                if grid[next_pos[0]][next_pos[1]] != "^":
                    grid[next_pos[0]][next_pos[1]] = "|"
                    queue.append(("|", next_pos))
                    seen.add(next_pos)
                    continue

                if grid[next_pos[0]][next_pos[1]] == "^":
                    split_left, split_right = False, False
                    left = (next_pos[0], next_pos[1] - 1)
                    if valid_pos(left, grid):
                        grid[left[0]][left[1]] = "|"
                        queue.append(("|", left))
                        seen.add(left)
                        split_left = True
                    right = (next_pos[0], next_pos[1] + 1)
                    if valid_pos(right, grid):
                        grid[right[0]][right[1]] = "|"
                        queue.append(("|", right))
                        seen.add(right)
                        split_right = True

                    if split_left and split_right:
                        # print(next_pos)
                        split_count += 1
            case "^":
                pass
            case _:
                raise Exception(f"The char {curr_char} is unsupported")

    # print_grid(grid)
    return split_count

def split_beam_2(grid: List[List[str]]) -> int:
    start_col = None
    for i in range(len(grid[0])):
        if grid[0][i] == "S":
            start_col = i
            break

    if start_col is None:
        raise Exception("No start position found")

    width = len(grid[0])
    current_row_counts = [0] * width
    current_row_counts[start_col] = 1
    total_timelines = []

    for r in range(0, len(grid) - 1):
        next_row_counts = [0] * width

        # print(current_row_counts)
        for c, count in enumerate(current_row_counts):
            if count == 0:
                continue

            ch = grid[r][c]

            if ch == "^":
                targets = [(r + 1, c - 1), (r + 1, c + 1)]
            else:
                targets = [(r + 1, c)]

            for nr, nc in targets:
                if valid_pos((nr, nc), grid):
                    next_row_counts[nc] += count

        current_row_counts = next_row_counts
        total_timelines.append(sum(current_row_counts))

    # print(current_row_counts)
    # total_timelines += sum(current_row_counts)
    # print(total_timelines)

    return total_timelines

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    count = split_beam(grid)
    print(f"Split count: {count}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_inputs(options.get("filepath", args[0]))

    total_timelines = split_beam_2(grid)
    print(f"Total timelines: {total_timelines[-1]}")
