import math
from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    rules = lines[0]
    adj_map = {}
    for l in lines[2:]:
        res = l.split(" = ")
        k = res[0].strip()
        res = res[1].split(", ")
        left = res[0][1:]
        right = res[1][:-1]
        adj_map[k] = (left, right)

    return (rules, adj_map)

def count_steps(rules: str, adj_map: Dict[str, Tuple[str, str]]) -> int:
    steps = 0
    current = "AAA"
    while True:
        if current == "ZZZ":
            break

        next_tuple = adj_map[current]
        i = steps % len(rules)
        if rules[i] == "L":
            current = next_tuple[0]
        elif rules[i] == "R":
            current = next_tuple[1]
        else:
            raise Exception("wtf")

        steps += 1

    return steps

# Already expected this one to take a long time
def count_steps_2(rules: str, adj_map: Dict[str, Tuple[str, str]]) -> int:
    steps = 0

    current = []
    for k in adj_map.keys():
        if k[-1] == "A":
            current.append(k)

    while True:
        if all(map(lambda x: x[-1] == "Z", current)):
            break

        i = steps % len(rules)
        if rules[i] == "L":
            current = list(map(lambda x: adj_map[x][0], current))
        elif rules[i] == "R":
            current = list(map(lambda x: adj_map[x][1], current))
        else:
            raise Exception("wtf")

        steps += 1

    return steps

def lcm(a, b):
    gcd = math.gcd(a, b)
    lcm = (a * b) // gcd
    return lcm

def count_steps_3(rules: str, adj_map: Dict[str, Tuple[str, str]]) -> int:
    steps_list = []
    current = []
    for k in adj_map.keys():
        if k[-1] == "A":
            current.append(k)

    # print("starts", current)
    for c in current:
        # print(f"working on {c}")
        steps = 0
        curr = c
        while True:
            if curr[-1] == "Z":
                break

            next_tuple = adj_map[curr]
            i = steps % len(rules)
            if rules[i] == "L":
                curr = next_tuple[0]
            elif rules[i] == "R":
                curr = next_tuple[1]
            else:
                raise Exception("wtf")

            steps += 1

        steps_list.append(steps)

    # print(steps_list)

    lcm_val = 1
    for n in steps_list:
        lcm_val = lcm(lcm_val, n)

    return lcm_val

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))
    rules = inputs[0]
    adj_map = inputs[1]

    steps = count_steps(rules, adj_map)
    print(f"Steps: {steps}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))
    rules = inputs[0]
    adj_map = inputs[1]

    steps = count_steps_3(rules, adj_map)
    print(f"Steps: {steps}")



