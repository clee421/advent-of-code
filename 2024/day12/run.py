from typing import Dict, List, Set, Tuple
import time

def parse_lines_grid(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    for line in lines:
        x = list(line)
        grid.append(x)

    return grid

def get_regions(grid: List[List[int]], pos: Tuple[int, int], memo: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    region = set()

    region.add(pos)
    memo.add(pos)

    queue = [pos]
    start = time.time()
    elapsed_time = start + 5
    while len(queue) > 0:
    # for i in range(5):
        # print("queue", queue)
        curr = queue.pop(0)
        # print(f"curr {curr}, region {region}")

        if time.time() > elapsed_time:
            now = time.time()
            elapsed_time = now + 10
            print(f"Currently working on pos {curr}, q size: {len(queue)}")
            print(f"Found {len(region)} plots. Total elapsed time {now - start}")

        x, y = curr[0], curr[1]
        curr_value = grid[x][y]

        for dx_dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            dx, dy = dx_dy[0], dx_dy[1]
            nx, ny = x + dx, y + dy
            # print("trying", (nx, ny))

            if nx < 0 or nx >= len(grid) or ny < 0 or ny >= len(grid[nx]):
                # print("out of bounds")
                continue

            if (nx, ny) in region or grid[nx][ny] != curr_value:
                # print("already seen or not value")
                continue

            queue.append((nx, ny))
            region.add((nx, ny))
            memo.add((nx, ny))

    return region

def calculate_fence_price(region: Set[Tuple[int, int]]) -> int:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    start = time.time()
    elapsed_time = start + 5
    perimeter = 0
    for r in region:
        if time.time() > elapsed_time:
            now = time.time()
            elapsed_time = now + 10
            print(f"Currently working on region {r}, size: {len(region)}. Total elapsed time {now - start}")

        val = 4
        for d in directions:
            if (r[0] + d[0], r[1] + d[1]) in region:
                val -= 1
        perimeter += val

    # print("perimeter", perimeter)
    return perimeter * len(region)

def count_sides(region: Set[Tuple[int, int]], direction: List[Tuple[int, int]]) -> int:
    sides = 0
    seen = set()
    for r in region:
        if r in seen:
            continue

        sides += 1
        seen.add(r)
        for d in direction:
            x, y = r[0] + d[0],  r[1] + d[1]
            while (x, y) in region:
                seen.add((x, y))
                x, y = x + d[0], y + d[1]

    return sides

def calculate_fence_price_2(start: Tuple[int, int], region: Set[Tuple[int, int]]) -> int:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    grouping = {}
    for d in directions:
        grouping[d] = set()

    for r in region:
        for d in directions:
            x, y = r[0] + d[0], r[1] + d[1]
            if (x, y) not in region:
                grouping[d].add(r)

    sides = 0
    verticals = [(1, 0), (-1, 0)]
    horizontal = [(0, 1), (0, -1)]

    right_side = grouping[(0, 1)]
    sides += count_sides(right_side, verticals)

    left_side = grouping[(0, -1)]
    sides += count_sides(left_side, verticals)

    top_side = grouping[(-1, 0)]
    sides += count_sides(top_side, horizontal)

    bottom_side = grouping[(1, 0)]
    sides += count_sides(bottom_side, horizontal)

    return sides * len(region)

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))

    memo = set()
    regions = {}
    print("Finding the regions...")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) not in memo:
                region = get_regions(grid, (i, j), memo)
                regions[(i, j)] = region

    # for corner in regions:
    #     print("|=======")
    #     print("|CORNER:", corner)
    #     print("|=======")
    #     print(regions[corner])

    print("Calculating price per region")
    total_price = 0
    for corner in regions:
        # print("corner", corner)
        price = calculate_fence_price(regions[corner])
        # print(f"corner {corner} has price {price}")
        total_price += price

    print("Total price:", total_price)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    grid = parse_lines_grid(options.get("filepath", args[0]))

    memo = set()
    regions = {}
    print("Finding the regions...")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) not in memo:
                region = get_regions(grid, (i, j), memo)
                regions[(i, j)] = region

    print("Calculating price per region")
    total_price = 0
    for corner in regions:
        price = calculate_fence_price_2(corner, regions[corner])
        # print(f"corner {corner} has price {price}")
        total_price += price
        # break

    print("Total price:", total_price)

