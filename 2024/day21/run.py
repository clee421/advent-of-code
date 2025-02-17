from typing import Dict, List, Tuple

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

MOVEMENT_MAP = {
    ("A", "A"): ["A"],
    ("A", "0"): ["<A"],
    ("A", "1"): ["^<<A"], # <^<A exists but we omit directly changes midway for all iterations
    ("A", "2"): ["<^A", "^<A"],
    ("A", "3"): ["^A"],
    ("A", "4"): ["^^<<A"], # "<^<^A", "<^^<A", "^<<^A", "^<^<A"
    ("A", "5"): ["<^^A", "^^<A"],
    ("A", "6"): ["^^A"],
    ("A", "7"): ["^^^<<A"],
    ("A", "8"): ["<^^^A", "^^^<A"],
    ("A", "9"): ["^^^A"],
    ("A", "^"): ["<A"],
    ("A", ">"): ["vA"],
    ("A", "v"): ["v<A", "<vA"],
    ("A", "<"): ["v<<A"],

    ("0", "A"): [">A"],
    ("0", "0"): ["A"],
    ("0", "1"): ["^<A"],
    ("0", "2"): ["^A"],
    ("0", "3"): [">^A", "^>A"],
    ("0", "4"): ["^^<A"],
    ("0", "5"): ["^^A"],
    ("0", "6"): [">^^A", "^^>A"],
    ("0", "7"): ["^^^<A"],
    ("0", "8"): ["^^^A"],
    ("0", "9"): [">^^^A", "^^^>A"],

    ("1", "A"): [">>vA"],
    ("1", "0"): [">vA"],
    ("1", "1"): ["A"],
    ("1", "2"): [">A"],
    ("1", "3"): [">>A"],
    ("1", "4"): ["^A"],
    ("1", "5"): [">^A", "^>A"],
    ("1", "6"): [">>^A", "^>>A"],
    ("1", "7"): ["^^A"],
    ("1", "8"): [">^^A", "^^>A"],
    ("1", "9"): [">>^^A", "^^>>A"],

    ("2", "A"): [">vA", "v>A"],
    ("2", "0"): ["vA"],
    ("2", "1"): ["<A"],
    ("2", "2"): ["A"],
    ("2", "3"): [">A"],
    ("2", "4"): ["<^A", "^<A"],
    ("2", "5"): ["^A"],
    ("2", "6"): [">^A", "^>A"],
    ("2", "7"): ["<^^A", "^^<A"],
    ("2", "8"): ["^^A"],
    ("2", "9"): [">^^A", "^^>A"],

    ("3", "A"): ["vA"],
    ("3", "0"): ["v<A", "<vA"],
    ("3", "1"): ["<<A"],
    ("3", "2"): ["<A"],
    ("3", "3"): ["A"],
    ("3", "4"): ["<<^A", "^<<A"],
    ("3", "5"): ["<^A", "^<A"],
    ("3", "6"): ["^A"],
    ("3", "7"): ["<<^^A", "^^<<A"],
    ("3", "8"): ["<^^A", "^^<A"],
    ("3", "9"): ["^^A"],

    ("4", "A"): [">>vvA"],
    ("4", "0"): [">vvA"],
    ("4", "1"): ["vA"],
    ("4", "2"): [">vA", "v>A"],
    ("4", "3"): [">>vA", "v>>A"],
    ("4", "4"): ["A"],
    ("4", "5"): [">A"],
    ("4", "6"): [">>A"],
    ("4", "7"): ["^A"],
    ("4", "8"): [">^A", "^>A"],
    ("4", "9"): [">>^A", "^>>A"],

    ("5", "A"): [">vvA", "vv>A"],
    ("5", "0"): ["vvA"],
    ("5", "1"): ["v<A", "<vA"],
    ("5", "2"): ["vA"],
    ("5", "3"): [">vA", "v>A"],
    ("5", "4"): ["<A"],
    ("5", "5"): ["A"],
    ("5", "6"): [">A"],
    ("5", "7"): ["<^A", "^<A"],
    ("5", "8"): ["^A"],
    ("5", "9"): [">^A", "^>A"],

    ("6", "A"): ["vvA"],
    ("6", "0"): ["vv<A", "<vvA"],
    ("6", "1"): ["v<<A", "<<vA"],
    ("6", "2"): ["v<A", "<vA"],
    ("6", "3"): ["vA"],
    ("6", "4"): ["<<A"],
    ("6", "5"): ["<A"],
    ("6", "6"): ["A"],
    ("6", "7"): ["<<^A", "^<<A"],
    ("6", "8"): ["<^A", "^<A"],
    ("6", "9"): ["^A"],

    ("7", "A"): [">>vvvA"],
    ("7", "0"): [">vvvA"],
    ("7", "1"): ["vvA"],
    ("7", "2"): [">vvA", "vv>A"],
    ("7", "3"): [">>vvA", "vv>>A"],
    ("7", "4"): ["vA"],
    ("7", "5"): [">vA", "v>A"],
    ("7", "6"): [">>vA", "v>>A"],
    ("7", "7"): ["A"],
    ("7", "8"): [">A"],
    ("7", "9"): [">>A"],

    ("8", "A"): [">vvvA", "vvv>A"],
    ("8", "0"): ["vvvA"],
    ("8", "1"): ["vv<A", "<vvA"],
    ("8", "2"): ["vvA"],
    ("8", "3"): [">vvA", "vv>A"],
    ("8", "4"): ["v<A", "<vA"],
    ("8", "5"): ["vA"],
    ("8", "6"): [">vA", "v>A"],
    ("8", "7"): ["<A"],
    ("8", "8"): ["A"],
    ("8", "9"): [">A"],

    ("9", "A"): ["vvvA"],
    ("9", "0"): ["vvv<A", "<vvvA"],
    ("9", "1"): ["vv<<A", "<<vvA"],
    ("9", "2"): ["vv<A", "<vvA"],
    ("9", "3"): ["vvA"],
    ("9", "4"): ["v<<A", "<<vA"],
    ("9", "5"): ["v<A", "<vA"],
    ("9", "6"): ["vA"],
    ("9", "7"): ["<<A"],
    ("9", "8"): ["<A"],
    ("9", "9"): ["A"],

    ("^", "A"): [">A"],
    ("^", "^"): ["A"],
    ("^", ">"): [">vA", "v>A"],
    ("^", "v"): ["vA"],
    ("^", "<"): ["v<A"],

    (">", "A"): ["^A"],
    (">", "^"): ["<^A", "^<A"],
    (">", ">"): ["A"],
    (">", "v"): ["<A"],
    (">", "<"): ["<<A"],

    ("v", "A"): [">^A", "^>A"],
    ("v", "^"): ["^A"],
    ("v", ">"): [">A"],
    ("v", "v"): ["A"],
    ("v", "<"): ["<A"],

    ("<", "A"): [">>^A"],
    ("<", "^"): [">^A"],
    ("<", ">"): [">A"],
    ("<", "v"): [">A"],
    ("<", "<"): ["A"],
}

def parse_inputs(filepath: str) -> str:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return lines

def calculate_min_moves(code: str, n: int, memo: Dict[Tuple[str, int], int]) -> int:
    if (code, n) in memo:
        return memo[(code, n)]

    if n == 0:
        memo[(code, n)] = len(code)
        return memo[(code, n)]

    result = 0
    for i in range(len(code)):
        if i == 0:
            curr, going_to = "A", code[i]
        else:
            curr, going_to = code[i-1], code[i]

        instructs = MOVEMENT_MAP[(curr, going_to)]
        result += min(list(map(lambda p: calculate_min_moves(p, n - 1, memo), instructs)))

    memo[(code, n)] = result

    return result

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for code in inputs:
        count = calculate_min_moves(code, 3, {})

        instruct_sum = count * int(code[:-1])
        print(f"length: {count} x value: {int(code[:-1])} = sum: {instruct_sum}")
        total += instruct_sum

    print(f"Total: {total}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for code in inputs:
        count = calculate_min_moves(code, 26, {})

        instruct_sum = count * int(code[:-1])
        print(f"length: {count} x value: {int(code[:-1])} = sum: {instruct_sum}")
        total += instruct_sum

    print(f"Total: {total}")

