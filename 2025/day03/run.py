from typing import Dict, List

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return lines

def find_largest_joltage(rating: str) -> int:
    max_joltage = 0
    for i in range(len(rating)):
        for j in range(i+1, len(rating)):
            max_joltage = max(max_joltage, int(rating[i] + rating[j]))

    return max_joltage

def calculate_total_joltage(ratings: List[str]) -> int:
    total = 0
    for r in ratings:
        j = find_largest_joltage(r)
        # print(f"for {r} -> joltage {j}")
        total += j

    return total

def find_largest_joltage_2(rating: str, n: int) -> int:
    if len(rating) < n:
        raise Exception("error in the code")

    if len(rating) == n:
        return int(rating)

    chosen = []
    start = 0
    remaining = n
    while remaining > 0:
        window_end = len(rating) - (remaining - 1)
        window = rating[start:window_end]
        max_digit = max(window)
        max_index = window.index(max_digit) + start
        chosen.append(max_digit)
        start = max_index + 1
        remaining -= 1

    return int("".join(chosen))

def calculate_total_joltage_2(ratings: List[str]) -> int:
    total = 0
    for r in ratings:
        j = find_largest_joltage_2(r, 12)
        # print(f"for {r} -> joltage {j}")
        total += j

    return total


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    joltage_ratings = parse_inputs(options.get("filepath", args[0]))

    total = calculate_total_joltage(joltage_ratings)
    print(f"Total: {total}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    joltage_ratings = parse_inputs(options.get("filepath", args[0]))

    total = calculate_total_joltage_2(joltage_ratings)
    print(f"Total: {total}")
