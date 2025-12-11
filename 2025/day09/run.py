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

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    points = parse_inputs(options.get("filepath", args[0]))

    area = find_largest_area(points)
    print(f"Area: {area}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    print("\n".join(inputs))
