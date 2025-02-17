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

def create_map(grid: List[List[str]], positions: List[Tuple[int, int]]) -> Dict[str, Dict[str, List[str]]]:
    position_map = {}
    for s_index in range(len(positions)):
        start = positions[s_index]
        s_val = grid[start[0]][start[1]]
        position_map[s_val] = {}

        for e_index in range(len(positions)):
            s_to_e_paths = []
            end = positions[e_index]
            paths = get_all_possible_paths(grid, start, end)

            min_path_length = 10000000000
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
def create_num_pad_map() -> Dict[str, Dict[str, List[str]]]:
    r = create_num_pad()
    num_pad, positions = r[0], r[1]
    return create_map(num_pad, positions)

def create_d_pad_map() -> Dict[str, Dict[str, List[str]]]:
    r = create_d_pad()
    d_pad, positions = r[0], r[1]
    return create_map(d_pad, positions)

def pad_instructions(input: str, pad_map: Dict[str, Dict[str, List[str]]]) -> List[str]:
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

def pad_instructions_2(input: str, pad_map: Dict[str, Dict[str, str]]) -> List[str]:
    result = ""
    for i in range(len(input)-1):
        curr, going_to = input[i], input[i+1]
        result += pad_map[curr][going_to]

    return result

def get_min_instructions(code: str, num_pad_map: Dict[str, Dict[str, List[str]]], d_pad_map: Dict[str, Dict[str, List[str]]]) -> str:
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

def get_min_from_list(a_list: List[str]) -> str:
    min_length = 1000000000000
    for a in a_list:
        min_length = min(min_length, len(a))

    for a in a_list:
        if len(a) == min_length:
            return a

    raise Exception("this should not happen")

def narrow_min_pad_maps(num_pad_map: Dict[str, Dict[str, List[str]]], d_pad_map: Dict[str, Dict[str, List[str]]]) -> Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, str]]]:
    new_d_pad_map = {}
    new_num_pad_map = {}

    for k_from in d_pad_map:
        new_d_pad_map[k_from] = {}
        for k_to in d_pad_map[k_from]:
            min_padded_instruct = get_min_from_list(pad_instructions(d_pad_map[k_from][k_to][0], d_pad_map))
            min_instruct = d_pad_map[k_from][k_to][0]
            for instruct in d_pad_map[k_from][k_to]:
                padded_instruct = get_min_from_list(pad_instructions(instruct, d_pad_map))
                if len(padded_instruct) < len(min_padded_instruct):
                    min_instruct = instruct

            new_d_pad_map[k_from][k_to] = min_instruct

    for k_from in num_pad_map:
        new_num_pad_map[k_from] = {}
        for k_to in num_pad_map[k_from]:
            min_padded_instruct = get_min_from_list(pad_instructions(num_pad_map[k_from][k_to][0], d_pad_map))
            min_instruct = num_pad_map[k_from][k_to][0]
            for instruct in num_pad_map[k_from][k_to]:
                padded_instruct = get_min_from_list(pad_instructions(instruct, d_pad_map))
                if len(padded_instruct) < len(min_padded_instruct):
                    min_instruct = instruct

            new_num_pad_map[k_from][k_to] = min_instruct

    return (new_num_pad_map, new_d_pad_map)

def get_min_instructions_2(code: str, n: int, num_pad_map: Dict[str, Dict[str, str]], d_pad_map: Dict[str, Dict[str, str]]) -> str:
    result = pad_instructions_2("A" + code, num_pad_map)
    for _ in range(n):
        result = pad_instructions_2("A" + result, d_pad_map)

    return result

def get_min_dpad_count(input: str, n: int, d_pad_map: Dict[str, Dict[str, str]], memo: Dict[Tuple[str, int], int]) -> int:
    if (input, n) in memo:
        # print("found memo", input, n)
        return memo[(input, n)]

    if n == 1:
        res = pad_instructions_2(input, d_pad_map)
        memo[(input, n)] = len(res)
        return memo[(input, n)]

    result = 0
    prev_instruct = None
    for i in range(len(input)-1):
        curr, going_to = input[i], input[i+1]
        instruct = d_pad_map[curr][going_to]
        if i == 0:
            instruct = "A" + instruct
        else:
            instruct = prev_instruct[-1] + instruct
        result += get_min_dpad_count(instruct, n-1, d_pad_map, memo)
        prev_instruct = instruct

    memo[(input, n)] = result

    return result

def get_min_dpad_count_2(input: str, n: int, d_pad_map: Dict[str, Dict[str, List[str]]], memo: Dict[Tuple[str, int], int], d_pad_map_2) -> int:
    if (input, n) in memo:
        # print("found memo", input, n)
        return memo[(input, n)]

    if n == 1:
        res = pad_instructions_2(input, d_pad_map_2)
        memo[(input, n)] = len(res)
        return memo[(input, n)]

    result = 0
    prev_instruct = None
    for i in range(len(input)-1):
        curr, going_to = input[i], input[i+1]
        instructs = d_pad_map[curr][going_to]
        local_min = None
        for instruct in instructs:
            if i == 0:
                instruct = "A" + instruct
            else:
                instruct = prev_instruct[-1] + instruct
            temp_min = get_min_dpad_count_2(instruct, n-1, d_pad_map, memo, d_pad_map_2)
            if local_min is None or temp_min < local_min:
                local_min = temp_min
                prev_instruct = instruct

        result += local_min

    memo[(input, n)] = result

    return result

def get_min_count(code: str, n: int, num_pad_map: Dict[str, Dict[str, str]], d_pad_map: Dict[str, Dict[str, str]]) -> int:
    memo = {}
    dpad_str = pad_instructions_2("A" + code, num_pad_map)
    result = get_min_dpad_count(dpad_str, n, d_pad_map, memo)
    # print(memo)

    return result

def get_min_count_2(code: str, n: int, num_pad_map: Dict[str, Dict[str, str]], d_pad_map: Dict[str, Dict[str, List[str]]], d_pad_map_2) -> int:
    memo = {}
    dpad_str = pad_instructions_2("A" + code, num_pad_map)
    result = get_min_dpad_count_2(dpad_str, n, d_pad_map, memo, d_pad_map_2)
    # print(memo)

    return result

def get_min_count_3(code: str, n: int, pad_map: Dict[str, Dict[str, List[str]]], memo: Dict[Tuple[str, int], int]) -> int:
    if (code, n) in memo:
        return memo[(code, n)]

    if n == 0:
        memo[(code, n)] = len(code)
        return memo[(code, n)]

    result = 0
    for i in range(len(code)-1):
        curr, going_to = code[i], code[i+1]
        instructs = pad_map[curr][going_to]
        local_min = []
        for instruct in instructs:
            if i == 0:
                instruct = "A" + instruct
            temp_min = get_min_count_3(instruct, n-1, pad_map, memo)
            local_min.append(temp_min)

        result += min(local_min)

    memo[(code, n)] = result

    return result

def get_min_dpad_count_2(input: str, n: int, d_pad_map: Dict[str, Dict[str, List[str]]], memo: Dict[Tuple[str, int], int], d_pad_map_2) -> int:
    if (input, n) in memo:
        # print("found memo", input, n)
        return memo[(input, n)]

    if n == 1:
        res = pad_instructions_2(input, d_pad_map_2)
        memo[(input, n)] = len(res)
        return memo[(input, n)]

    result = 0
    prev_instruct = None
    for i in range(len(input)-1):
        curr, going_to = input[i], input[i+1]
        instructs = d_pad_map[curr][going_to]
        local_min = None
        for instruct in instructs:
            if i == 0:
                instruct = "A" + instruct
            else:
                instruct = prev_instruct[-1] + instruct
            temp_min = get_min_dpad_count_2(instruct, n-1, d_pad_map, memo, d_pad_map_2)
            if local_min is None or temp_min < local_min:
                local_min = temp_min
                prev_instruct = instruct

        result += local_min

    memo[(input, n)] = result

    return result

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    num_pad_map = create_num_pad_map()
    d_pad_map = create_d_pad_map()

    res = narrow_min_pad_maps(num_pad_map, d_pad_map)
    num_pad_map_2, d_pad_map_2 = res[0], res[1]

    total = 0
    for input in inputs:
        o = get_min_instructions_2(input, 2, num_pad_map_2, d_pad_map_2)

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

    # keypad_dirs = create_dpad_map()
    # print(keypad_dirs)

    num_pad_map = create_num_pad_map()
    d_pad_map = create_d_pad_map()

    a_merged = num_pad_map["A"] | d_pad_map["A"]
    merged_pad_map = num_pad_map | d_pad_map
    merged_pad_map["A"] = a_merged

    total = 0
    for code in inputs:
        count = get_min_count_3("A" + code, 26, merged_pad_map, {})

        instruct_sum = count * int(code[:-1])
        print(f"length: {count} x value: {int(code[:-1])} = sum: {instruct_sum}")
        total += instruct_sum

    print(f"Total: {total}")

    # res = narrow_min_pad_maps(num_pad_map, d_pad_map)
    # num_pad_map_2, d_pad_map_2 = res[0], res[1]

    # # print("num_pad_map_2", num_pad_map_2)
    # # print("d_pad_map_2", d_pad_map_2)

    # layers = int(args[1]) if len(args) > 1 else 2
    # total = 0
    # for input in inputs:
    #     # count = get_min_count(input, layers, num_pad_map_2, d_pad_map_2)
    #     count = get_min_count_2(input, layers, num_pad_map_2, d_pad_map, d_pad_map_2)

    #     instruct_sum = count * int(input[:-1])
    #     print(f"length: {count} x value: {int(input[:-1])} = sum: {instruct_sum}")
    #     total += instruct_sum

    # print(f"Total: {total}")
    # # 335078733882526 is too high
    # # 297448271134066 not correct
    # # 294209504640384
    #   1294297196
    # # 260987462148488 also not correct but better?
    # # 133860691755948 is too low
"""

length: 84539018430 x value: 805 = sum: 68053909836150
length: 88153312358 x value: 682 = sum: 60120559028156
length: 93607514064 x value: 671 = sum: 62810641936944
length: 81651274032 x value: 973 = sum: 79446689633136
length: 84691130720 x value: 319 = sum: 27016470699680
Total: 297448271134066

69613005324660
58976484011456
60893633732822
78552411885318
26173969686128
294209504640384

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
