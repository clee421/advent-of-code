from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    init_seq_steps = []
    for l in lines:
        for step in l.split(","):
            init_seq_steps.append(step)

    return init_seq_steps

def _hash(step: str, curr: int) -> int:
    if len(step) > 1:
        raise f"{step} should be only 1 charactor"

    curr = ((curr + ord(step)) * 17) % 256
    return curr

def hash_step(step: str) -> int:
    curr = 0
    for c in step:
        curr = _hash(c, curr)

    return curr

def parse_step(step: str) -> Tuple[str, str, int]:
    res = step.split("=")
    if len(res) == 2:
        return (res[0], "=", int(res[1]))

    if len(res) == 1:
        res = step.split("-")
        return (res[0], "-", -1)

    raise f"Invalid step {step}"

def create_hashmap(steps: List[str]) -> Dict[str, List[Tuple[str, int]]]:
    hashmap: Dict[str, List[str]] = {}
    label_values = {}
    for s in steps:
        parsed_step = parse_step(s)
        box_id = hash_step(parsed_step[0])
        action = parsed_step[1]
        if action == "=":
            box = hashmap.get(box_id, [])
            if parsed_step[0] not in box:
                box.append(parsed_step[0])
                hashmap[box_id] = box

            label_values[parsed_step[0]] = parsed_step[2]
        elif action == "-":
            box = hashmap.get(box_id, [])
            if parsed_step[0] in box:
                box.remove(parsed_step[0])
                del label_values[parsed_step[0]]
        else:
            raise f"Invalid action {action}"

    populated_hashmap = {}
    for k, v in hashmap.items():
        if len(v) > 0:
            populated_hashmap[k] = [(l, label_values[l]) for l in v]

    return populated_hashmap

def calc_focal_power(hashmap: Dict) -> int:
    total = 0

    for box, focals in hashmap.items():
        for i in range(len(focals)):
            slot = i + 1
            label, length = focals[i]
            power = ((int(box) + 1) * slot * length)
            total += power

    return total

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    sequence = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for r in sequence:
        v = hash_step(r)
        total += v
        # print(r, hash_step(r))

    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    sequence = parse_inputs(options.get("filepath", args[0]))

    hashmap = create_hashmap(sequence)
    power = calc_focal_power(hashmap)

    print("Power:", power)