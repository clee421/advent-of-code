import time
import re
from typing import Dict, List, Tuple

def parse_robot_locations(filepath: str) -> List[Tuple[int, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    robots = []
    for line in lines:
        result = re.search("^p=(\\d+)\\,(\\d+)\\sv=(-?\\d+)\\,(-?\\d+)$", line)
        robots.append([(int(result[1]), int(result[2])), (int(result[3]), int(result[4]))])

    return robots

def print_robots(robots: List[Tuple[int, int]], w_h: Tuple[int, int]):
    width = w_h[0]
    height = w_h[1]

    grid = []
    for _ in range(height):
        grid.append([0] * width)

    for r in robots:
        row = r[0][1]
        col = r[0][0]
        grid[row][col] += 1

    for row in grid:
        new_row = list(map(lambda x: "." if x == 0 else f"{x}", row))
        print(f"{"".join(new_row)}\n")

def elapse_time(robots: List[Tuple[int, int]], grid: Tuple[int, int], time_sec: int) -> List[Tuple[int, int]]:
    new_robots = []
    width = grid[0]
    height = grid[1]
    for r in robots:
        p_x, p_y, v_x, v_y = r[0][0], r[0][1], r[1][0], r[1][1]
        p_x += (v_x * time_sec)
        p_y += (v_y * time_sec)

        p_x %= width
        p_y %= height
        new_robots.append([(p_x, p_y), (v_x, v_y)])

    return new_robots

def calculate_safety_factor(robots: List[Tuple[int, int]], grid: Tuple[int, int]) -> int:
    width = grid[0]
    height = grid[1]

    half_width = int(width / 2)
    half_height = int(height / 2)

    q1, q2, q3, q4 = 0, 0, 0, 0
    for r in robots:
        if r[0][0] < half_width and r[0][1] < half_height:
            q1 += 1
        elif r[0][0] > half_width and r[0][1] < half_height:
            q2 += 1
        elif r[0][0] < half_width and r[0][1] > half_height:
            q3 += 1
        elif r[0][0] > half_width and r[0][1] > half_height:
            q4 += 1

    # print(q1, q2, q3, q4)
    return q1 * q2 * q3 * q4

def detect_xmas_tree(robots: List[Tuple[int, int]], w_h: Tuple[int, int]) -> bool:
    width = w_h[0]
    height = w_h[1]

    grid = []
    for _ in range(height):
        grid.append([0] * width)

    for r in robots:
        row = r[0][1]
        col = r[0][0]
        grid[row][col] += 1

    for row in grid:
        new_row = "".join(list(map(lambda x: "." if x == 0 else "#", row)))
        if "######" in new_row:
            return True

    return False


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    robots = parse_robot_locations(options.get("filepath", args[0]))

    width = 101
    height = 103
    if args[0] == "sample":
        width = 11
        height = 7

    # print_robots(robots, (width, height))
    # print("==========")
    robots = elapse_time(robots, (width, height), 100)
    # print_robots(robots, (width, height))
    safe_factor = calculate_safety_factor(robots, (width, height))

    print(f"Safety factor: {safe_factor}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    robots = parse_robot_locations(options.get("filepath", args[0]))

    width = 101
    height = 103
    if args[0] == "sample":
        width = 11
        height = 7

    start = time.time()
    elapsed_time = start + 5
    for i in range(1000000):
        if time.time() > elapsed_time:
            now = time.time()
            elapsed_time = now + 10
            print(f"On elapsed time: {i + 1}. Total elapsed time {now - start}")
        robots = elapse_time(robots, (width, height), 1)
        if detect_xmas_tree(robots, (width, height)):
            print_robots(robots, (width, height))
            print(f"========== {i} ====")
