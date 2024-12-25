from typing import Dict, List

class Equation:
    def __init__(self, result: int, values: List[int]):
        self.result = result
        self.values =  values

    def __str__(self):
        return f"{self.result}: {", ".join(str(x) for x in self.values)}"

    def __repr__(self):
        return f"[{self.result}: {", ".join(str(x) for x in self.values)}]"

    def is_possible(self) -> bool:
        # print("Is possible?", self.result, self.values)
        _reversed = self.values.copy()
        _reversed.reverse()
        return dfs(self.result, _reversed)

    def is_possible2(self) -> bool:
        return dfs2(self.result, self.values)

def dfs(target: int, values: List[int]) -> bool:
    # print("Target:", target, "Values:", values)
    if len(values) < 2:
        # print("Values:", values)
        raise Exception("someting went wrong")

    if len(values) == 2:
        return values[0] + values[1] == target or values[0] * values[1] == target

    if dfs(target - values[0], values[1:]):
        # print("Add new target:", target - values[0])
        return True

    if target % values[0] != 0:
        # print("target % values[0]", target % values[0])
        return False

    # print("Multiply new target:", int(target / values[0]))
    return dfs(int(target / values[0]), values[1:])

def dfs2(target: int, values: List[int]) -> bool:
    if len(values) < 1:
        raise Exception("someting went wrong")

    if len(values) == 1:
        return target == values[0]

    if len(values) == 2:
        return (
            values[0] + values[1] == target or
            values[0] * values[1] == target or
            int(f"{values[0]}{values[1]}") == target
        )

    add_list = values[1:]
    add_list[0] = values[0] + values[1]

    mul_list = values[1:]
    mul_list[0] = values[0] * values[1]

    cat_list = values[1:]
    cat_list[0] = int(f"{values[0]}{values[1]}")

    return dfs2(target, add_list) or dfs2(target, mul_list) or dfs2(target, cat_list)

def parse_lines_equations(filepath: str) -> List[Equation]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    equations = []
    for line in lines:
        parts = line.split(":")
        result = int(parts[0].strip())
        values = list(map(lambda x: int(x), parts[1].strip().split(" ")))
        equations.append(Equation(result, values))

    return equations

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    equations = parse_lines_equations(options.get("filepath", args[0]))

    total = 0
    for e in equations:
        if e.is_possible():
            # print(e)
            total += e.result

    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    equations = parse_lines_equations(options.get("filepath", args[0]))

    total = 0
    for e in equations:
        if e.is_possible2():
            # print(e)
            total += e.result

    print("Total:", total)