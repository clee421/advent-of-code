from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    points = []
    for l in lines:
        x, y = list(map(lambda x: int(x), l.split(",")))
        points.append((x, y))

    return points

def calculate_rectangle_area(x1, y1, x2, y2) -> int:
    length = abs(x2 - x1) + 1
    width = abs(y2 - y1) + 1
    return length * width

def find_largest_area(points: List[Tuple[int, int]]) -> int:
    max_area = 0
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            area = calculate_rectangle_area(points[i][0], points[i][1], points[j][0], points[j][1])
            # print(f"{points[i]} / {points[j]} has area of {area}")
            max_area = max(max_area, area)

    return max_area

def calculate_bounds(points: List[Tuple[int, int]]) -> Tuple[str, int, int, int]:
    segments = []
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        if x1 == x2:
            y_min, y_max = sorted((y1, y2))
            segments.append(("v", x1, y_min, y_max))
        elif y1 == y2:
            x_min, x_max = sorted((x1, x2))
            segments.append(("h", y1, x_min, x_max))
        else:
            raise Exception("Non axis-aligned segment detected")
    return segments

def build_row_intervals(points: List[Tuple[int, int]], bounds: Tuple[str, int, int, int]):
    ys = sorted(set(p[1] for p in points))
    verticals = [seg for seg in bounds if seg[0] == "v"]
    horizontals = [seg for seg in bounds if seg[0] == "h"]

    slabs = []

    for i in range(len(ys) - 1):
        y0, y1 = ys[i], ys[i + 1]
        xs = []
        for _, x, y_min, y_max in verticals:
            if y_min <= y0 < y_max:
                xs.append(x)
        xs.sort()
        intervals = []
        for k in range(0, len(xs), 2):
            if k + 1 < len(xs):
                intervals.append((xs[k], xs[k + 1]))
        if intervals:
            slabs.append((y0, y1 - 1, intervals))

    for _, y, x1, x2 in horizontals:
        if x1 > x2:
            x1, x2 = x2, x1
        slabs.append((y, y, [(x1, x2)]))

    points = set()
    for s_start, s_end, _ in slabs:
        points.add(s_start)
        points.add(s_end + 1)
    ys_events = sorted(points)

    merged_slabs = []
    for i in range(len(ys_events) - 1):
        y0 = ys_events[i]
        y1 = ys_events[i + 1] - 1
        active = []
        for s_start, s_end, intervals in slabs:
            if s_start <= y0 <= s_end:
                active.extend(intervals)
        if not active:
            continue
        active.sort()
        merged = []
        for a, b in active:
            if not merged or a > merged[-1][1] + 1:
                merged.append([a, b])
            else:
                merged[-1][1] = max(merged[-1][1], b)
        merged_slabs.append((y0, y1, [(a, b) for a, b in merged]))

    merged_slabs.sort(key=lambda s: s[0])
    return merged_slabs

def find_largest_area_in_bounds(points: List[Tuple[int, int]]) -> int:
    bounds = calculate_bounds(points)
    row_intervals = build_row_intervals(points, bounds)

    red_points = points

    def row_covers(y_start: int, y_end: int, x1: int, x2: int) -> bool:
        curr = y_start
        for s_start, s_end, intervals in row_intervals:
            if s_end < curr:
                continue
            if s_start > curr:
                return False  # gap
            covered = any(a <= x1 and b >= x2 for a, b in intervals)
            if not covered:
                return False
            curr = min(s_end, y_end) + 1
            if curr > y_end:
                return True
        return curr > y_end

    max_area = 0
    for i in range(len(red_points)):
        for j in range(i + 1, len(red_points)):
            x1, y1 = red_points[i]
            x2, y2 = red_points[j]
            min_x, max_x = sorted((x1, x2))
            min_y, max_y = sorted((y1, y2))

            if row_covers(min_y, max_y, min_x, max_x):
                area = calculate_rectangle_area(x1, y1, x2, y2)
                max_area = max(max_area, area)

    return max_area

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    points = parse_inputs(options.get("filepath", args[0]))

    area = find_largest_area(points)
    print(f"Area: {area}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    points = parse_inputs(options.get("filepath", args[0]))

    area = find_largest_area_in_bounds(points)
    print(f"Area: {area}")
