from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[Tuple[int, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    result = []
    for l in lines:
        for pair in l.split(","):
            # print(pair)
            p = pair.split("-")

            # data quality issue?
            if len(p) == 1:
                continue

            # print(p[0], p[1])
            result.append((int(p[0]), int(p[1])))

    return result

def is_invalid_id(n: int) -> bool:
    s_n = str(n)
    if len(s_n) % 2 != 0:
        return False

    start = 0
    mid = int(len(s_n) / 2)
    while mid < len(s_n):
        if s_n[start] != s_n[mid]:
            return False
        start += 1
        mid += 1

    return True


def calculate_invalid_ids(ranges: List[Tuple[int, int]]):
    scores = 0
    for r in ranges:
        for n in range(r[0], r[1] + 1):
            if is_invalid_id(n):
                scores += n

    return scores

def is_invalid_id_2(n: int, split: int) -> bool:
    s_n = str(n)
    if len(s_n) % split != 0:
        return False

    chunk_size = int(len(s_n) / split)
    chunk = s_n[:chunk_size]

    return chunk * split == s_n


def calculate_invalid_ids_2(ranges: List[Tuple[int, int]]):
    scores = 0
    for r in ranges:
        for n in range(r[0], r[1] + 1):
            for s in range(2, len(str(n)) + 1):
                if is_invalid_id_2(n, s):
                    scores += n
                    break

    return scores

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    ranges = parse_inputs(options.get("filepath", args[0]))

    scores = calculate_invalid_ids(ranges)

    print(f"Invalid IDs total: {scores}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    ranges = parse_inputs(options.get("filepath", args[0]))

    scores = calculate_invalid_ids_2(ranges)

    print(f"Invalid IDs total: {scores}")
