from typing import Dict, List, Tuple
from functools import lru_cache


def parse_inputs(filepath: str) -> List[Tuple[str, List[int]]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    condition_records = []
    for l in lines:
        res = l.split(" ")
        condition_records.append(
            # (conditions, broken_springs)
            (res[0], [int(x) for x in res[1].split(",")])
        )

    return condition_records

def expand_records(condition_records: List[Tuple[str, List[int]]]) -> List[Tuple[str, List[int]]]:
    expansion_num = 5
    expanded_records = []
    for r in condition_records:
        r_str, r_springs = r[0], r[1]
        r_str = "?".join([r_str] * expansion_num)
        r_springs = r_springs * expansion_num

        expanded_records.append((r_str, r_springs))

    return expanded_records

# NOTE: I'm not very good at these sort of problems so I used o3 to solve
# the problem. The o3 model had bugs also and needed refinement twice to
# guard and arrive at a solution. I'll study this style of problem a bit
# more and then attempt it again.
def get_arrangements(conditions: str, broken_springs: List[int]) -> int:
    conditions_len = len(conditions)

    @lru_cache(maxsize=None)
    def dfs(pos: int, gi: int) -> int:
        if gi == len(broken_springs):
            return 0 if '#' in conditions[pos:] else 1

        g_len = broken_springs[gi]
        ways  = 0

        for start in range(pos, conditions_len - g_len + 1):
            if any(conditions[k] == '#' for k in range(pos, start)):
                continue

            if start > 0 and conditions[start - 1] == '#':
                continue

            if any(conditions[k] == '.' for k in range(start, start + g_len)):
                continue

            end = start + g_len
            if end < conditions_len and conditions[end] == '#':
                continue

            next_pos = end + 1 if end < conditions_len else end
            ways += dfs(next_pos, gi + 1)

        return ways

    return dfs(0, 0)

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    condition_records = parse_inputs(options.get("filepath", args[0]))

    arrangement_count = 0
    for r in condition_records:
        c = get_arrangements(r[0], r[1])
        arrangement_count += c

    print(f"Total: {arrangement_count}")


def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    condition_records = parse_inputs(options.get("filepath", args[0]))
    condition_records = expand_records(condition_records)

    # records_length = len(condition_records)
    arrangement_count = 0
    for i, r in enumerate(condition_records):
        c = get_arrangements(r[0], r[1])
        # print(f"[{i + 1}/{records_length}] arrangements: {c}")
        arrangement_count += c

    print(f"Total: {arrangement_count}")