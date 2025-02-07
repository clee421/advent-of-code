import time
from typing import Dict, List, Tuple, Set

def parse_inputs(filepath: str) -> Tuple[List[str], List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    towels = lines[0].split(", ")
    if lines[1] != "":
        raise Exception("Input is not as expected")

    designs = lines[2:]

    return (towels, designs)

def is_design_possible(design: str, towels: List[str]) -> bool:
    # print("design", design)
    for t in towels:
        # print("design", design, "t", t, "design == t", design == t)
        if design == t:
            return True

    for t in towels:
        # print("design", design, "t", t, "design.startswith(t)", design.startswith(t))
        if design.startswith(t):
            if is_design_possible(design[len(t):], towels):
                return True

    return False

# This is correct but takes way too long
def num_possible_designs(design: str, towels: List[str], memo: Dict[str, List[Set[str]]] = {}) ->  List[List[str]]:
    # print(f"Design {design}")
    if design in memo:
        # print(f"Found {design} in memo")
        return memo[design]

    design_possibilities: List[List[str]] = []
    for t in towels:
        if design == t:
            design_possibilities.append([t])

    for t in towels:
        if design.startswith(t):
            # print(f"Design {design} starts with {t}")
            sub_design_possibilities = num_possible_designs(design[len(t):], towels, memo)
            # print(f"Found sub_design_possibilities {len(sub_design_possibilities)}")
            for sdp in sub_design_possibilities:
                design_possibilities.append([t, *sdp])

    memo[design] = design_possibilities
    return design_possibilities

def num_possible_designs_2(design: str, towels: List[str], memo: Dict[str, int] = {}) ->  int:
    if design in memo:
        return memo[design]

    design_possibilities = 0
    for t in towels:
        if design == t:
            design_possibilities += 1

    for t in towels:
        if design.startswith(t):
            design_possibilities += num_possible_designs_2(design[len(t):], towels, memo)

    memo[design] = design_possibilities
    return design_possibilities

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))
    towels, designs = inputs[0], inputs[1]

    # is_design_possible("bwurrg", towels)
    possible = 0
    for d in designs:
        if is_design_possible(d, towels):
            # print(f"{d} is possible")
            possible += 1
        # else:
        #     print(f"{d} is not possible")

    print("Possible designs:", possible)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))
    towels, designs = inputs[0], inputs[1]

    # start = time.time()
    possible = 0
    for d in designs:
        # print(f"==== Working on design {d} ====")
        # all_designs = num_possible_designs(d, towels)
        all_designs = num_possible_designs_2(d, towels)
        # possible += len(all_designs)
        possible += all_designs
        # print(f"Total elapsed time {time.time() - start}")

    print("Possible designs:", possible)