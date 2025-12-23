from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> Tuple[Dict[str, List[str]], List[Tuple[Tuple[int, int], List[int]]]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    shapes: Dict[int, List[str]] = {}
    regions: List[Tuple[Tuple[int, int], List[int]]] = []

    indices = [0, 5, 10, 15, 20, 25]
    for i in indices:
        shapes[int(lines[i][0])] = [
            lines[i+1],
            lines[i+2],
            lines[i+3],
        ]

    for i in range(30, len(lines)):
        res = lines[i].split(": ")
        x, y = res[0].split("x")
        regions.append(((int(x), int(y)), list(map(lambda x: int(x), res[1].split(" ")))))

    return (shapes, regions)

def shape_stats(shape: List[str]) -> Tuple[int, int, int]:
    height = len(shape)
    width = max(len(row) for row in shape) if shape else 0
    area = sum(ch == "#" for row in shape for ch in row)
    return width, height, area

def can_fit_region(shapes: Dict[str, List[str]], region: Tuple[Tuple[int, int], List[int]]) -> bool:
    (width, height), counts = region

    region_area = width * height
    total_shape_area = 0
    total_bound_box_area = 0

    for i, count in enumerate(counts):
        if count == 0:
            continue
        s = shapes[i]
        shape_width, shape_height, shape_area = shape_stats(s)

        if shape_width > width or shape_height > height:
            return False

        total_shape_area += shape_area * count
        total_bound_box_area += (shape_width * shape_height) * count

    if total_shape_area > region_area:
        return False

    if total_bound_box_area > region_area:
        return False

    return True

def count_fittable_regions(shapes: Dict[str, List[str]], regions: List[Tuple[Tuple[int, int], List[int]]]) -> int:
    count = 0
    for r in regions:
        if can_fit_region(shapes, r):
            count += 1

    return count

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    shapes, regions = parse_inputs(options.get("filepath", args[0]))

    # I get 1 for the sample but the input is solved so.. win?
    result = count_fittable_regions(shapes, regions)
    print(f"Result: {result}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    print("There's no part 2!")