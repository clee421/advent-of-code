from typing import Dict, List

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return lines

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    print("\n".join(inputs))

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    print("\n".join(inputs))