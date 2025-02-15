from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    schematics = []
    _schem = []
    for l in lines:
        if l == "":
            schematics.append(_schem)
            _schem = []
            continue

        _schem.append(l)
    schematics.append(_schem)

    return schematics

def parse_schematic(schematic: List[str]) -> List[int]:
    key = [-1] * len(schematic[0])
    for r in schematic:
        for i in range(len(key)):
            if r[i] == "#":
                key[i] += 1

    return key

def parse_key_and_locks(schematics: List[List[str]]) -> Tuple[List[List[int]], List[List[int]]]:
    keys = []
    locks = []
    for s in schematics:
        if s[0] == "#####":
            locks.append(parse_schematic(s))
        else:
            keys.append(parse_schematic(s))

    return (keys, locks)

def does_key_and_lock_fit(key: List[int], lock: List[int]) -> bool:
    for i in range(len(key)):
        if key[i] + lock[i] > 5:
            return False

    return True

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    schematics = parse_inputs(options.get("filepath", args[0]))

    # for schematic in schematics:
    #     for row in schematic:
    #         print(row)
    #     print("=====")

    res = parse_key_and_locks(schematics)
    keys, locks = res[0], res[1]
    count = 0
    for k in keys:
        for l in locks:
            if does_key_and_lock_fit(k, l):
                count += 1

    print("Count:", count)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    print("\n".join(inputs))