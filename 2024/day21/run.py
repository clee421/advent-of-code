from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> str:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return lines

def create_num_pad() -> Tuple[List[List[str]], List[Tuple[int, int]]]:
    grid = [
        list("#####"),
        list("#789#"),
        list("#456#"),
        list("#123#"),
        list("##0A#"),
        list("#####"),
    ]
    pos = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != "#":
                pos.append((i, j))

    return (grid, pos)

def create_d_pad() ->Tuple[List[List[str]], List[Tuple[int, int]]]:
    grid = [
        list("#####"),
        list("##^A#"),
        list("#<v>#"),
        list("#####"),
    ]

    pos = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != "#":
                pos.append((i, j))

    return (grid, pos)

def get_all_possible_paths(grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> List[str]:
    paths = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = [(start, [])]
    while len(queue) > 0:
        curr = queue.pop(0)
        curr_pos, curr_path = curr[0], curr[1]

        if curr_pos == end:
            paths.append(curr_path)
            continue

        for d in directions:
            x, y = curr_pos[0] + d[0], curr_pos[1] + d[1]
            if grid[x][y] == "#" or (x, y) in curr_path:
                continue

            cp_path = curr_path.copy()
            cp_path.append((x, y))
            queue.append(((x, y), cp_path))

    # print(f"start: {grid[start[0]][start[1]]}, end: {grid[end[0]][end[1]]}, paths: {paths}")
    return paths

def map_to_direction(start: Tuple[int, int], paths: List[Tuple[int, int]]) -> str:
    res = []
    for p in paths:
        d = ""
        t = [start, *p]
        for i in range(1, len(t)):
            curr, next = t[i-1], t[i]
            # print("curr", curr, "next", next)
            x, y = next[0] - curr[0], next[1] - curr[1]
            match (x, y):
                case (0, 1):
                    d += ">"
                case (1, 0):
                    d += "v"
                case (0, -1):
                    d += "<"
                case (-1, 0):
                    d += "^"
                case _:
                    raise Exception("wtf")
        res.append(d + "A")
    return res

def create_map(grid: List[List[str]], positions: List[Tuple[int, int]]) -> Dict[str, Dict[str, str]]:
    position_map = {}
    for s_index in range(len(positions)):
        start = positions[s_index]
        s_val = grid[start[0]][start[1]]
        position_map[s_val] = {}

        for e_index in range(len(positions)):
            s_to_e_paths = []
            end = positions[e_index]
            paths = get_all_possible_paths(grid, start, end)

            min_path_length = 1000000
            for p in paths:
                min_path_length = min(min_path_length, len(p))
            for p in paths:
                if len(p) == min_path_length:
                    s_to_e_paths.append(p)

            e_val = grid[end[0]][end[1]]
            position_map[s_val][e_val] = map_to_direction(start, s_to_e_paths)

    return position_map

# returns the shortest path from one num to another
# {
#   "A": {"A": ["A"], "9": ["^^^A"]}
# }
def create_num_pad_map() -> Dict[str, Dict[str, str]]:
    r = create_num_pad()
    num_pad, positions = r[0], r[1]
    return create_map(num_pad, positions)

def create_d_pad_map() -> Dict[str, Dict[str, str]]:
    r = create_d_pad()
    d_pad, positions = r[0], r[1]
    return create_map(d_pad, positions)

def pad_instructions(input: List[str], pad_map:  Dict[str, Dict[str, str]]) -> List[str]:
    result_list = [""]

    for i in range(len(input)-1):
        curr, going_to = input[i], input[i+1]
        temp_result = []
        for instruct in pad_map[curr][going_to]:
            for r in result_list:
                temp_result.append(r + instruct)

        result_list = temp_result

    min_len = 10000000000
    for r in result_list:
        min_len = min(min_len, len(r))

    final_result = []
    for r in result_list:
        if len(r) == min_len:
            final_result.append(r)

    return final_result

def get_min_instructions(code: str,  num_pad_map:  Dict[str, Dict[str, str]],  d_pad_map:  Dict[str, Dict[str, str]]) -> str:
    all_results = []
    keypad_instruct_list = pad_instructions("A" + code, num_pad_map)
    for kil in keypad_instruct_list:
        dpad_instruct_list_1 = pad_instructions("A" + kil, d_pad_map)
        for dil1 in dpad_instruct_list_1:
            dpad_instruct_list_1 = pad_instructions("A" + dil1, d_pad_map)
            all_results.extend(dpad_instruct_list_1)

    min_length = 1000000000
    for r in all_results:
        min_length = min(min_length, len(r))

    final_results = []
    for r in all_results:
        if len(r) == min_length:
            final_results.append(r)

    # print("final_results", final_results)
    return final_results[0]


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    num_pad_map = create_num_pad_map()
    d_pad_map = create_d_pad_map()

    total = 0
    for input in inputs:
        o = get_min_instructions(input, num_pad_map, d_pad_map)

        instruct_sum = len(o) * int(input[:-1])
        print(f"length: {len(o)} + value: {int(input[:-1])} = sum: {instruct_sum}")
        total += instruct_sum

    print(f"Total: {total}")

    # input = inputs[2]
    # o = get_min_instructions(input, num_pad_map, d_pad_map)

    # instruct_sum = len(o) * int(input[:-1])
    # print(f"length: {len(o)} + value: {int(input[:-1])} = sum: {instruct_sum}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    print("\n".join(inputs))

"""
<    ^   <   A    ^  ^ A  >  > A  v   v v A
v<<A >^A v<A >>^A <A A >A vA A ^A v<A A A >^A

+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

^<<A ^^A >>A vvvA

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

<A v<A A >>^A <A A >A vA A ^A <vA A A >^A
^  <   < A    ^  ^ A  >  > A  v   v v A

<Av<AA>>^A<AA>AvAA^A<vAAA>^A

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

<v<A >>^A <vA <A >>^A A vA A <^A >A <v<A >>^A A vA ^A <vA >^A A <A >A <v<A >A >^A A A vA <^A >A
<    A    v   <  A    A >  > ^   A  <    A    A >  A  v   A   A ^  A  <    v  A   A A >  ^   A
"""
