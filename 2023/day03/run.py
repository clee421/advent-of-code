from typing import Dict, List, Tuple, Set

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return lines

def valid_pos(pos: Tuple[int, int], schem: List[str]) -> bool:
    return pos[0] >= 0 and pos[0] < len(schem) and pos[1] >= 0 and pos[1] < len(schem[pos[0]])

def parse_number(pos: Tuple[int, int], schem: List[str], seen: Set[Tuple[int, int]]) -> int:
    res = ""
    x, y = pos[0], pos[1]
    while valid_pos((x, y), schem) and schem[x][y].isdigit():
        res = schem[x][y] + res
        seen.add((x, y))
        y -= 1

    x, y = pos[0], pos[1] + 1
    while valid_pos((x, y), schem) and schem[x][y].isdigit():
        res = res + schem[x][y]
        seen.add((x, y))
        y += 1

    return int(res)

def calculate_parts(schem: List[str]) -> int:
    side_and_below = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    seen = set()
    total = 0
    for i in range(len(schem)):
        for j in range(len(schem[i])):
            if (i, j) in seen:
                continue

            if schem[i][j].isdigit() or schem[i][j] == ".":
                continue

            for d in side_and_below:
                x, y = i + d[0], j + d[1]

                if x < 0 or x >= len(schem) or y < 0 or y >= len(schem[x]):
                    continue

                if (x, y) in seen or not schem[x][y].isdigit():
                    continue

                n = parse_number((x, y), schem, seen)
                # print(n)
                total += n

    return total

def calculate_gear_ratios(schem: List[str]) -> int:
    side_and_below = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    total = 0
    for i in range(len(schem)):
        for j in range(len(schem[i])):
            if schem[i][j].isdigit() or schem[i][j] == ".":
                continue

            seen = set()
            numbers = []
            for d in side_and_below:
                x, y = i + d[0], j + d[1]

                if x < 0 or x >= len(schem) or y < 0 or y >= len(schem[x]):
                    continue

                if (x, y) in seen or not schem[x][y].isdigit():
                    continue

                n = parse_number((x, y), schem, seen)
                numbers.append(n)
                if len(numbers) == 2:
                    # print(numbers, (numbers[0] * numbers[1]))
                    total += (numbers[0] * numbers[1])

    return total


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    schematics = parse_inputs(options.get("filepath", args[0]))

    total = calculate_parts(schematics)
    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    schematics = parse_inputs(options.get("filepath", args[0]))

    total = calculate_gear_ratios(schematics)
    print("Total:", total)