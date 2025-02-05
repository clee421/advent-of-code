import re
import time
from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> Tuple[Dict[str, int], List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    registers = {}
    program = []
    is_parse_second_section = False
    for l in lines:
        if l == "":
            is_parse_second_section = True
            continue

        if not is_parse_second_section:
            result = re.search("^Register ([A|B|C])\\: (\\d+)$", l)
            registers[result[1]] = int(result[2])
        else:
            program = list(map(lambda x: int(x), l.split(":")[1].strip().split(",")))

    return (registers, program)

def combo_operand(registers: Dict[str, int], op: int) -> int:
    if op < 4:
        return op
    elif op == 4:
        return registers["A"]
    elif op == 5:
        return registers["B"]
    elif op == 6:
        return registers["C"]
    elif op == 7:
        raise Exception("reserved and will not appear in valid programs")

    raise Exception("something broke")

def execute_program(registers: Dict[str, int], program:  List[int]) -> List[int]:
    result = []
    i = 0
    opcode_override = None
    while i < len(program):
        opcode, operand = program[i], program[i+1]

        # print(f"Iteration {i} / opcode_override {opcode_override}, running opcode: {opcode} / operand: {operand}")
        match opcode:
            case 0:
                # adv
                numerator = registers["A"]
                denominator = 2**combo_operand(registers, operand)
                registers["A"] = int(numerator / denominator)
            case 1:
                # bxl
                registers["B"] = registers["B"] ^ operand
            case 2:
                # bst
                registers["B"] = combo_operand(registers, operand) % 8
            case 3:
                # jnz
                if registers["A"] != 0:
                    opcode_override = operand
            case 4:
                # bxc
                registers["B"] = registers["B"] ^ registers["C"]
            case 5:
                # out
                o = combo_operand(registers, operand) % 8
                result.append(o)
            case 6:
                # bdv
                numerator = registers["A"]
                denominator = 2**combo_operand(registers, operand)
                registers["B"] = int(numerator / denominator)
            case 7:
                # cdv
                numerator = registers["A"]
                denominator = 2**combo_operand(registers, operand)
                registers["C"] = int(numerator / denominator)

        if opcode_override is None:
            i += 2
        else:
            i = opcode_override
            opcode_override = None


    # print(registers)

    return result

def find_program_brute_force(registers: Dict[str, int], target_program:  List[int]) -> int:
    start = time.time()
    elapsed_time = start + 5

    # MATCH = 12
    # START = 220_141_272_079
    # END = 3_000_000_000_000
    # JUMP = 262144

    MATCH = 12
    START = 220_141_272_079
    END = 3_000_000_000_000
    JUMP = 262144

    prev = 0
    for i in range(END, START, -JUMP):
        if time.time() > elapsed_time:
            now = time.time()
            elapsed_time = now + 10
            print(f"Current value: {i}. Total elapsed time {now - start}")

        cp = registers.copy()
        cp["A"] = i
        o = execute_program(cp, target_program)
        if o == target_program:
            return i

        if o[:MATCH] == target_program[:MATCH]:
            print(f"i {i} matched {MATCH} elements. i - {prev} = {i - prev}")
            prev = i

    return -1

def test_octals(program):
    registers = {"A": 0, "B": 0, "C": 0}

    def run_oct_test(n):
        cp = registers.copy()
        cp["A"] = n
        o = execute_program(cp, program)

        # print(f"A: {n}, oct(A): {oct(n)}, output: {o} | {len(o)}")
        if o == [2,4,1,2,7,5,0,3,4,7,1,7,5,5,3,0]:
            print(f"A: {n}, oct(A): {oct(n)}, output: {o} | {len(o)}")

    # for i in range(1, 11):
    #     run_oct_test(i)

    # for i in range(101, 111):
    #     run_oct_test(i)

    # for i in range(1001, 1011):
    #     run_oct_test(i)

    # for i in range(10001, 10011):
    #     run_oct_test(i)

    # for i in range(190_385_000_000_000, 190_386_000_000_000, 100_000_000):
    for i in range(190384113100000, 190384113800000, 1):
        run_oct_test(i)

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))
    registers, program = inputs[0], inputs[1]

    output = execute_program(registers, program)
    print("Output", ",".join(list(map(lambda x: str(x), output))))

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))
    registers, program = inputs[0], inputs[1]

    test_octals(program)

    # a_value = find_program_brute_force(registers.copy(), program)
    # print("Register A", a_value)