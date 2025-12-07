from functools import reduce
from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> Tuple[List[List[int]], List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    temp_results = []
    for l in lines:
        temp_results.append(l.split(" "))

    nums = []
    for i in range(len(temp_results) - 1):
        filtered = filter(lambda x: x, temp_results[i])
        nums.append(list(map(lambda x: int(x), filtered)))

    return (nums, list(filter(lambda x: x, temp_results[-1])))

def parse_inputs_2(filepath: str) -> Tuple[List[List[str]], List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip("\n") for line in file]

    ops_line = lines[-1]
    # Find the column starts by looking at where the operators sit.
    col_starts = [i for i, c in enumerate(ops_line) if c.strip()]
    if not col_starts:
        raise Exception("No operators found in the last line")

    # Columns appear to be evenly spaced; use the smallest gap as the width.
    if len(col_starts) > 1:
        widths = [b - a for a, b in zip(col_starts, col_starts[1:])]
        col_width = min(widths)
    else:
        # Single column – width is the remaining length.
        col_width = len(ops_line) - col_starts[0]

    nums: List[List[str]] = []
    for line in lines[:-1]:
        row = []
        for idx, start in enumerate(col_starts):
            end = col_starts[idx + 1] if idx + 1 < len(col_starts) else len(line)
            cell = line[start:end].rstrip(" ")
            row.append(cell)
        nums.append(row)

    ops = [ops_line[start] for start in col_starts]

    # Normalize column widths so original spacing is preserved (leading spaces kept,
    # trailing spaces padded out to the widest cell in each column).
    col_widths = [0] * len(col_starts)
    for row in nums:
        for idx, cell in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(cell))

    for row in nums:
        for idx, cell in enumerate(row):
            row[idx] = cell.ljust(col_widths[idx], " ")

    return (nums, ops)

def compute_total(nums: List[List[int]], ops: List[str]) -> int:
    # print(nums)
    total = 0
    for c_i in range(len(nums[0])):
        add_sub_total = 0
        mul_sub_total = 1
        for r_i in range(len(nums)):
            op = ops[c_i]
            # print(f"{nums[r_i][c_i]} | {op}")
            if op == "+":
                add_sub_total += nums[r_i][c_i]
            elif op =="*":
                mul_sub_total *= nums[r_i][c_i]
            else:
                raise Exception(f"operation {op} unsupported!")

        if add_sub_total > 0:
            # print("add_sub_total", add_sub_total)
            total += add_sub_total

        if mul_sub_total > 1:
            # print("mul_sub_total", mul_sub_total)
            total += mul_sub_total

    return total

def transform_numbers(nums: List[str]) -> List[int]:
    # str_nums = list(map(lambda x: str(x), nums))
    # print("str_nums", str_nums)
    # max_len = len(max(str_nums, key=lambda x: len(x)))
    max_len = len(max(nums, key=lambda x: len(x)))
    # print("max_len", max_len)
    # padded_nums = list(map(lambda x: x.rjust(max_len, "*"), str_nums))
    # print(padded_nums)

    t_nums = []
    for c_i in range(max_len):
        n_str = ""
        for r_i in range(len(nums)):
            if nums[r_i][c_i] != " ":
                n_str += nums[r_i][c_i]

        t_nums.append(int(n_str))

    # print("t_nums", t_nums)

    return t_nums

def compute_total_2(nums: List[List[str]], ops: List[str]) -> int:
    total = 0
    for c_i in range(len(nums[0])):

        op = ops[c_i]
        sub_num = []
        for r_i in range(len(nums)):
            sub_num.append(nums[r_i][c_i])

        t_nums = transform_numbers(sub_num)

        if op == "+":
            total += reduce(lambda x, y: x + y, t_nums)
        elif op =="*":
            total += reduce(lambda x, y: x * y, t_nums)
        else:
            raise Exception(f"operation {op} unsupported!")

    return total

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    n_and_ops = parse_inputs(options.get("filepath", args[0]))

    total = compute_total(nums=n_and_ops[0], ops=n_and_ops[1])
    print(f"Total: {total}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    n_and_ops = parse_inputs_2(options.get("filepath", args[0]))
    # print(n_and_ops)

    total = compute_total_2(nums=n_and_ops[0], ops=n_and_ops[1])
    print(f"Total: {total}")
