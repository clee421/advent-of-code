from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> Tuple[Dict[str, int], Tuple[str, str, str, str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    inputs = {}
    formulas = []
    is_2nd_part = False
    for l in lines:
        if l == "":
            is_2nd_part = True
            continue

        if not is_2nd_part:
            res = l.split(": ")
            inputs[res[0]] = int(res[1])
        else:
            res = l.split(" -> ")
            formula, output = res[0], res[1]
            res = formula.split(" ")
            left, logic, right = res[0], res[1], res[2]

            formulas.append((left, logic, right, output))

    return (inputs, formulas)

def calculate_final_output(inputs: Dict[str, int], formulas: List[Tuple[str, str, str, str]]) -> int:
    queue = formulas.copy()
    while len(queue) > 0:
        f = queue.pop(0)
        left, logic, right, output = f[0], f[1], f[2], f[3]

        if left not in inputs or right not in inputs:
            queue.append(f)
            continue

        match logic:
            case "AND":
                inputs[output] = inputs[left] & inputs[right]
            case "OR":
                inputs[output] = inputs[left] | inputs[right]
            case "XOR":
                inputs[output] = inputs[left] ^ inputs[right]
            case _:
                raise Exception("wtf")

    binary_str = ""
    i = 0
    while True:
        digit_str = f"{i}".zfill(2)
        if f"z{digit_str}" not in inputs:
            break

        binary_str = str(inputs[f"z{digit_str}"]) + binary_str
        i += 1

    print(binary_str)
    return int(binary_str, 2)

def parse_x_y(inputs: Dict[str, int]) -> Tuple[int, int]:
    x_binary_str = ""
    y_binary_str = ""
    i = 0
    while True:
        digit_str = f"{i}".zfill(2)
        if f"x{digit_str}" not in inputs or f"y{digit_str}" not in inputs:
            break

        x_binary_str = x_binary_str + str(inputs[f"x{digit_str}"])
        y_binary_str = y_binary_str + str(inputs[f"y{digit_str}"])
        i += 1

    # z goes fucking backwards so x and y string build gets swapped
    print(x_binary_str, y_binary_str)
    return (int(x_binary_str, 2), int(y_binary_str, 2))

def create_formula_dep_map(formulas: List[Tuple[str, str, str, str]]) -> Dict[str, List[str]]:
    dep_map = {}
    for f in formulas:
        left, logic, right, output = f[0], f[1], f[2], f[3]
        dep_map[output] = [left, right]

    return dep_map

def get_dep_graph_for_output(output: str, dep_map: Dict[str, List[str]], formulas: List[Tuple[str, str, str, str]]) -> List[Tuple[str, str, str, str]]:
    ordered_deps = []
    queue = [output]
    while len(queue) > 0:
        curr = queue.pop(0)
        ordered_deps.append(curr)
        if curr in dep_map:
            queue.extend(dep_map[curr])

    ordered_deps.reverse()
    required_formulas = []
    for od in ordered_deps:
        for f in formulas:
            left, logic, right, output = f[0], f[1], f[2], f[3]
            if od == output:
                required_formulas.append(f)

    return required_formulas

def get_dummy_inputs(n: int) -> Dict[str, int]:
    dummy = {}
    for i in range(n):
        digit_str = f"{i}".zfill(2)
        dummy[f"x{digit_str}"] = 0
        dummy[f"y{digit_str}"] = 0

    return dummy

def validate_x_y_z(i: int, z1_formula: List[Tuple[str, str, str, str]], z2_formula: List[Tuple[str, str, str, str]]) -> bool:
    truth_table = [
        # [x0, y0], [s0, s1]
        [[0, 0], [0, 0]],
        [[0, 1], [1, 0]],
        [[1, 0], [1, 0]],
        [[1, 1], [0, 1]],
    ]

    input_map = get_dummy_inputs(45)

    for row in truth_table:
        x_y, expect = row[0], row[1]

        digit_str = f"{i}".zfill(2)
        digit_str_1 = f"{i+1}".zfill(2)
        x, y = f"x{digit_str}", f"y{digit_str}"

        z0, z1 = f"z{digit_str}", f"z{digit_str_1}"

        input_map[x] = x_y[0]
        input_map[y] = x_y[1]

        both_formulas = [*z1_formula, *z2_formula]
        for f in both_formulas:
            left, logic, right, output = f[0], f[1], f[2], f[3]

            match logic:
                case "AND":
                    input_map[output] = input_map[left] & input_map[right]
                case "OR":
                    input_map[output] = input_map[left] | input_map[right]
                case "XOR":
                    input_map[output] = input_map[left] ^ input_map[right]
                case _:
                    raise Exception("wtf?")

        if input_map[z0] != expect[0] and input_map[z1] != expect[1]:
            print(f"x{i}: {x_y[0]}, y{i}: {x_y[1]}, expect: {(expect[1], expect[0])} got: {(input_map[z1], input_map[z0])}")
            return False

    return True

# wasn't really needed, i was trying stuff
def formula_tiers(inputs: Dict[str, int], formulas: List[Tuple[str, str, str, str]]) -> List[List[str]]:
    formula_tiers = []

    while len(formulas) > 0:
        possible_formulas = []
        formulas_waiting = []
        for f in formulas:
            left, logic, right, output = f[0], f[1], f[2], f[3]
            if left in inputs and right in inputs:
                possible_formulas.append(f)
            else:
                formulas_waiting.append(f)

        current_tier = []
        for f in possible_formulas:
            left, logic, right, output = f[0], f[1], f[2], f[3]
            match logic:
                case "AND":
                    inputs[output] = inputs[left] & inputs[right]
                case "OR":
                    inputs[output] = inputs[left] | inputs[right]
                case "XOR":
                    inputs[output] = inputs[left] ^ inputs[right]
                case _:
                    raise Exception("wtf")

            current_tier.append(f"{left} {logic} {right} -> {output}")

        formula_tiers.append(current_tier)
        formulas = formulas_waiting

    return formula_tiers

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    r = parse_inputs(options.get("filepath", args[0]))
    inputs, formulas = r[0], r[1]

    output = calculate_final_output(inputs, formulas)

    print("Output:", output)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    r = parse_inputs(options.get("filepath", args[0]))
    inputs, formulas = r[0], r[1]

    dep_map = create_formula_dep_map(formulas)

    # I graphed it out and now 46 is limit
    for i in range(45):
        digit_str = f"{i}".zfill(2)
        zx0_formulas = get_dep_graph_for_output(f"z{digit_str}", dep_map, formulas)

        digit_str_1 = f"{i+1}".zfill(2)
        zx1_formulas = get_dep_graph_for_output(f"z{digit_str_1}", dep_map, formulas)

        res = validate_x_y_z(i, zx0_formulas, zx1_formulas)
        if not res:
            print(f"z{digit_str} result for adder", res)

    # changed = ["kbk", "tgj", "z13", "hsw", "qjc", "z18", "nvr", "wkr"]
    changed = ["bjm", "hsw", "nvr", "skf", "wkr", "z07", "z13", "z18"]
    changed.sort()
    text = ",".join(changed)
    print(f"Manual work on this: {text}")

    """
    these both worked for z07
    y07 AND x07 -> kbk
    y07 XOR x07 -> tgj
          and
    tgj XOR mkm -> bjm
    njc OR kbk -> z07

    z13
    pmv AND rbk -> z13
    pmv XOR rbk -> hsw

    y18 XOR x18 -> qjc
    y18 AND x18 -> z18
          and
    bgt XOR qjc -> skf
    y18 AND x18 -> z18

    x26 XOR y26 -> nvr
    y26 AND x26 -> wkr

    bjm,hsw,nvr,skf,wkr,z07,z13,z18
    """


    # output = calculate_final_output(inputs, formulas)
    # r = parse_x_y(inputs)
    # x, y = r[0], r[1]

    # print(f"x: {x} + y: {y} = {x + y}, output: {output}, {x + y == output}")

    # tiers = formula_tiers(inputs, formulas)
    # for tier in tiers:
    #     print("\n".join(tier))
    #     print("==================")

"""
https://www.geeksforgeeks.org/full-adder-in-digital-logic/
truth table for full adder

aaa,aoc,bbb,ccc,eee,ooo,z24,z99

i don't get it, the example looks wrong

x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1

y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x05 AND y05 -> z00
1 & 1 -> 1

x02 AND y02 -> z01
0 & 1 -> 0

x01 AND y01 -> z02
1 & 0 -> 0

x03 AND y03 -> z03
1 & 1 -> 1

x04 AND y04 -> z04
0 & 0 -> 0

x00 AND y00 -> z05
0 & 0 -> 0

z: 001001

x00 AND y00 -> z00
0 & 0 -> 0

x01 AND y01 -> z01
1 & 0 -> 0

x02 AND y02 -> z02
0 & 1 -> 0

x03 AND y03 -> z03
1 & 1 -> 1

x04 AND y04 -> z04
0 & 0 -> 0

x05 AND y05 -> z05
1 & 1 -> 1

z: 101000
"""