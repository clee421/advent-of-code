from typing import Dict, List, Tuple

def get_input_sequence(filepath: str) -> str:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    if len(lines) != 1:
        # for line in lines:
        #     print(line)
        print("WARNING: The input is longer than 1 line")

    return lines

def parse_input(text: str) -> List[Tuple[int, int]]:
    inputs = []
    current = 0
    while current != -1:
        # print("current", current, text[current:current+5])
        next_index = text[current:].find("mul(")
        # print("finding mul( - next_index", next_index)
        if next_index == -1:
            return inputs

        current += (next_index + 4)
        next_dig_index = text[current:].find(",")
        # print("finding , - next_dig_index", next_dig_index)
        if next_dig_index > 3 or next_dig_index < 1:
            continue

        maybe_digit = text[current:current+next_dig_index]
        if not maybe_digit.isdigit():
            continue

        left = int(maybe_digit)

        current += (next_dig_index + 1)
        next_dig_index = text[current:].find(")")
        # print("finding ) - next_dig_index", next_dig_index)
        if next_dig_index > 3 or next_dig_index < 1:
            continue

        maybe_digit = text[current:current+next_dig_index]
        if not maybe_digit.isdigit():
            continue

        right = int(maybe_digit)

        # print("appending", (left, right))
        inputs.append((left, right))

    return inputs

def parse_input_2(text: str) -> List[Tuple[int, int] | str]:
    inputs = []
    current = 0
    while current != -1:
        # print("looking at", text[current:])
        do_index = text[current:].find("do()")
        # print("finding do() - do_index", do_index)
        if do_index == -1:
            do_index = len(text) + 1
        dont_index = text[current:].find("don't()")
        # print("finding don't() - dont_index", dont_index)
        if dont_index == -1:
            dont_index = len(text) + 1
        # print("current", current, text[current:current+5])
        next_index = text[current:].find("mul(")
        # print("finding mul( - next_index", next_index)

        if do_index < next_index or dont_index < next_index:
            if do_index < dont_index:
                inputs.append("do")
                current += (do_index + 4)
            elif dont_index < do_index:
                inputs.append("dont")
                current += (dont_index + 7)

            continue

        if next_index == -1:
            return inputs

        current += (next_index + 4)
        next_dig_index = text[current:].find(",")
        # print("finding , - next_dig_index", next_dig_index)
        if next_dig_index > 3 or next_dig_index < 1:
            continue

        maybe_digit = text[current:current+next_dig_index]
        if not maybe_digit.isdigit():
            continue

        left = int(maybe_digit)

        current += (next_dig_index + 1)
        next_dig_index = text[current:].find(")")
        # print("finding ) - next_dig_index", next_dig_index)
        if next_dig_index > 3 or next_dig_index < 1:
            continue

        maybe_digit = text[current:current+next_dig_index]
        if not maybe_digit.isdigit():
            continue

        right = int(maybe_digit)

        # print("appending", (left, right))
        inputs.append((left, right))

    return inputs



def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = get_input_sequence(options.get("filepath", args[0]))
    total = 0
    for input in inputs:
        muls = parse_input(input)
        # print(muls)

        sum = 0
        for m in muls:
            sum += (m[0] * m[1])

        print("Sum:", sum)
        total += sum
    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = get_input_sequence(options.get("filepath", args[0]))
    total = 0
    enabled = True
    for input in inputs:
        muls = parse_input_2(input)
        # print(muls)

        sum = 0
        for m in muls:
            if isinstance(m, str):
                if m == "dont":
                    enabled = False
                else:
                    enabled = True
                continue
            if enabled:
                sum += (m[0] * m[1])
            # else:
                # print("skipping:", m)

        print("Sum:", sum)
        total += sum
    print("Total:", total)