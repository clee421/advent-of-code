from typing import Dict, List, Tuple

def parse_lines_grid(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for line in lines:
        x = list(map(lambda x: int(x), list(line)))
        grid.append(x)

    return grid

def find_trailheads(grid: List[List[int]]) -> List[Tuple[int, int]]:
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                trailheads.append((i, j))

    return trailheads

def next_valid_steps(grid: List[List[int]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    next_steps = []
    for delta in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        new_x = pos[0] + delta[0]
        new_y = pos[1] + delta[1]

        if new_x < 0 or new_x >= len(grid) or new_y < 0 or new_y >= len(grid[new_x]):
            continue

        next_steps.append((new_x, new_y))

    return next_steps

def calculate_trailhead_score(grid: List[List[int]], pos: Tuple[int, int]) -> int:
    score = set()
    queue = [pos]
    while len(queue) > 0:
        curr = queue.pop(0)
        curr_value = grid[curr[0]][curr[1]]
        if curr_value == 9 and curr not in score:
            score.add(curr)
            continue

        for maybe_next_step in next_valid_steps(grid, curr):
            if (curr_value+1) == grid[maybe_next_step[0]][maybe_next_step[1]]:
                queue.append(maybe_next_step)

    return len(score)

def calculate_trailhead_score_2(grid: List[List[int]], pos: Tuple[int, int]) -> int:
    score = 0
    queue = [pos]
    while len(queue) > 0:
        curr = queue.pop(0)
        curr_value = grid[curr[0]][curr[1]]
        # only real change here
        if curr_value == 9:
            score += 1
            continue

        for maybe_next_step in next_valid_steps(grid, curr):
            if (curr_value+1) == grid[maybe_next_step[0]][maybe_next_step[1]]:
                queue.append(maybe_next_step)

    return score


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))

    trailheads = find_trailheads(grid)

    total = 0
    for th in trailheads:
        score = calculate_trailhead_score(grid, th)
        # print(f"Trailhead {th} has score of {score}")

        total += score

    print(f"Total score: {total}")


def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))

    trailheads = find_trailheads(grid)

    total = 0
    for th in trailheads:
        score = calculate_trailhead_score_2(grid, th)
        # print(f"Trailhead {th} has score of {score}")

        total += score

    print(f"Total score: {total}")