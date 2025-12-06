from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[Tuple[str, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    results = []
    for l in lines:
        d = l[0]
        n = int(l[1:])
        results.append((d, n))

    return results

def calculate_end_number(rotations: List[Tuple[str, int]], start: int = 50) -> int:
    password = 0
    curr = start
    # print(f"start: {curr}")
    for r in rotations:
        if r[0] == "R":
            curr += r[1]
        else:
            curr -= r[1]

        curr = curr % 100
        # print(f"rotate {r[0]}; point to {curr}")
        if curr == 0:
            password += 1

    return password

def calculate_end_number_2(rotations: List[Tuple[str, int]], start: int = 50) -> int:
    password = 0
    prev_zero = False
    curr = start
    # print(f"start: {curr}")
    for r in rotations:
        over_rotations = int(r[1] / 100)
        # print(f"over_rotations {over_rotations}")
        password += over_rotations

        remainder = r[1] % 100
        if r[0] == "R":
            curr += remainder
        else:
            curr -= remainder

        if not prev_zero and (curr < 0 or curr > 100 or curr == 0 or curr == 100):
            # print(f"password increased: {curr}")
            password += 1

        curr = curr % 100
        if curr == 0:
            prev_zero = True
        else:
            prev_zero = False

        # print(f"rotate {r[0]} {r[1]}; point to {curr}; password {password}")

    return password


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    rotations = parse_inputs(options.get("filepath", args[0]))

    num = calculate_end_number(rotations=rotations)
    print(f"Password is: {num}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    rotations = parse_inputs(options.get("filepath", args[0]))

    num = calculate_end_number_2(rotations=rotations)
    print(f"Password is: {num}")