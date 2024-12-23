from typing import Dict, List, Tuple

def clean(line: str) -> Tuple[int, int]:
    parts = line.split(" ")
    return (int(parts[0]), int(parts[-1]))

def parse_lines_to_lists(filepath: str) -> Tuple[List[int], List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    left, right = [], []
    for line in lines:
        pair = clean(line)
        left.append(pair[0])
        right.append(pair[1])

    return (left, right)

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    left, right = parse_lines_to_lists(args[0])

    left.sort()
    right.sort()

    total = 0
    for i in range(len(left)):
        total += abs(right[i] - left[i])

    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    left, right = parse_lines_to_lists(args[0])

    count = {}
    for n in right:
        c = count.get(n, 0)
        count[n] = c+1

    similarity = 0
    for n in left:
        c = count.get(n, 0)
        similarity += (n * c)

    print("Similarity:", similarity)