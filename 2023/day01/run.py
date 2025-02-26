from typing import Dict, List

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return lines

NUM_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def find_start_num(text: str) -> str:
    min_index = len(text)
    min_value = None
    for s in range(len(text)):
        if text[s].isdigit():
            min_index = s
            min_value = text[s]
            break

    for word_num in [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]:
        w_index = text.find(word_num)
        if w_index != -1 and w_index < min_index:
            min_index = w_index
            min_value = NUM_MAP[word_num]

    return min_value

def find_end_num(text: str) -> str:
    max_index = -1
    max_value = None
    for e in range(len(text)-1, -1, -1):
        if text[e].isdigit():
            max_index = e
            max_value = text[e]
            break

    for word_num in [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]:
        w_index = text.rfind(word_num)
        if w_index != -1 and w_index > max_index:
            max_index = w_index
            max_value = NUM_MAP[word_num]

    return max_value

def get_number(text: str) -> int:
    left = find_start_num(text)
    right = find_end_num(text)
    # print("line:", text, int(f"{left}{right}"))

    return int(f"{left}{right}")

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for line in inputs:
        l, r = None, None
        s, e = 0, len(line) - 1
        for s in range(len(line)):
            if line[s].isdigit():
                l = line[s]
                break

        for e in range(len(line)-1, -1, -1):
            if line[e].isdigit():
                r = line[e]
                break

        # print("line:", line, int(f"{l}{r}"))
        total += int(f"{l}{r}")

    print("Total", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for line in inputs:
        total += get_number(line)

    print("Total", total)