from typing import Dict, List, Tuple
import heapq

def parse_inputs(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return [[int(i) for i in list(line)] for line in lines]

def find_min_heat_loss(heat_map: List[List[int]]) -> int:
    directions_map = {
        (0, 1): [(-1, 0), (1, 0)],
        (0, -1): [(-1, 0), (1, 0)],
        (-1, 0): [(0, -1), (0, 1)],
        (1, 0): [(0, -1), (0, 1)],
    }

    heat_map_len = len(heat_map) - 1
    end = (heat_map_len, len(heat_map[heat_map_len]))

    start = (0, 0)
    direction = (0, 1)
    # tuple: heat loss, position, direction, seen, straight count
    min_heap = [(0, start, direction, set(), 0)]
    while min_heap:
        print(min_heap)
        curr_heat_loss, curr_pos, curr_dir, seen, straight_count = heapq.heappop(min_heap)
        next_directions = directions_map[curr_dir]
        if straight_count < 3:
            next_directions.append(curr_dir)

        for dx, dy in next_directions:
            nx, ny = curr_pos[0] + dx, curr_pos[1] + dy

            if (nx, ny) == end:
                return curr_heat_loss

            if nx < 0 or nx >= len(heat_map) or ny < 0 or ny >= len(heat_map[nx]):
                continue

            if (nx, ny) in seen:
                continue

            new_heat_loss = curr_heat_loss + heat_map[nx][ny]
            new_pos = (nx, ny)
            new_dir = (dx, dy)
            new_seen = seen.copy()
            new_seen.add(new_pos)
            new_straight_count = 1
            if new_dir == curr_dir:
                new_straight_count = straight_count + 1

            heapq.heappush(min_heap, (new_heat_loss, new_pos, new_dir, new_seen, new_straight_count))

    return -1

def find_min_heat_loss_2(heat_map: List[List[int]]) -> int:
    ROWS, COLS = len(heat_map), len(heat_map[0])
    end = (ROWS - 1, COLS - 1)

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # (heat_loss, x, y, direction_index, steps_in_direction)
    heap = [(0, 0, 0, d, 0) for d in range(4)]
    visited = dict()

    while heap:
        heat, x, y, d, steps = heapq.heappop(heap)
        key = (x, y, d, steps)
        if key in visited and visited[key] <= heat:
            continue
        visited[key] = heat

        if (x, y) == end:
            return heat

        if steps < 3:
            dx, dy = dirs[d]
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                heapq.heappush(heap, (heat + heat_map[nx][ny], nx, ny, d, steps + 1))

        for turn in [-1, 1]:
            nd = (d + turn) % 4
            dx, dy = dirs[nd]
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                heapq.heappush(heap, (heat + heat_map[nx][ny], nx, ny, nd, 1))

    return -1

def find_min_heat_loss_3(heat_map: List[List[int]]) -> int:
    ROWS, COLS = len(heat_map), len(heat_map[0])
    end = (ROWS - 1, COLS - 1)

    # note: right, down, left, right must alternate because we use it to calculate turns
    next_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # (heat_loss, x, y, direction_index, steps_in_direction)
    heap = [(0, 0, 0, d, 0) for d in range(4)]
    visited = dict()

    while heap:
        heat, x, y, direct, steps = heapq.heappop(heap)
        key = (x, y, direct, steps)
        if key in visited and visited[key] <= heat:
            continue
        visited[key] = heat

        # > it needs to move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end)
        # i should read better -_-
        if (x, y) == end and steps >= 4:
            return heat

        if steps < 10:
            dx, dy = next_directions[direct]
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                heapq.heappush(heap, (heat + heat_map[nx][ny], nx, ny, direct, steps + 1))

        if steps > 3:
            for turn in [-1, 1]:
                nd = (direct + turn) % 4
                dx, dy = next_directions[nd]
                nx, ny = x + dx, y + dy
                if 0 <= nx < ROWS and 0 <= ny < COLS:
                    heapq.heappush(heap, (heat + heat_map[nx][ny], nx, ny, nd, 1))

    return -1


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    heat_map = parse_inputs(options.get("filepath", args[0]))

    # heat_path = find_min_heat_loss(heat_map)
    # heat_loss = 0
    # for hp in heat_path:
    #     heat_loss += heat_map[hp[0]][hp[1]]

    heat_loss = find_min_heat_loss_2(heat_map)
    print(f"Loss: {heat_loss}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    heat_map = parse_inputs(options.get("filepath", args[0]))

    heat_loss = find_min_heat_loss_3(heat_map)
    print(f"Loss: {heat_loss}")