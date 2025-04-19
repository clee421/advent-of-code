from typing import Dict, List

def parse_inputs(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    elves = []
    elf = []
    for l in lines:
        if l == "":
            elves.append(elf)
            elf = []
        else:
            elf.append(int(l))

    elves.append(elf)

    return elves

def get_elf_calories(elf: List[int]) -> int:
    total = 0
    for c in elf:
        total += c

    return total

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    elves = parse_inputs(options.get("filepath", args[0]))

    max_cal = 0
    for e in elves:
        max_cal = max(max_cal, get_elf_calories(e))

    print(f"Max: {max_cal}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    elves = parse_inputs(options.get("filepath", args[0]))

    calories = [get_elf_calories(e) for e in elves]
    calories.sort()
    total = calories[-3] + calories[-2] + calories[-1]

    print(f"Total: {total}")