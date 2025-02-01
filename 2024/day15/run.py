from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> Tuple[List[List[str]], List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    grid = []
    moves = []
    is_parse_second_section = False
    for l in lines:
        if l == "":
            is_parse_second_section = True
            continue

        if not is_parse_second_section:
            grid.append(list(l))
        else:
            moves.extend(list(l))

    return (grid, moves)

def find_robot_pos(grid: List[List[str]], target: str) -> Tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == target:
                return (i, j)

    raise Exception("wtf")

def move_direction(grid: List[List[str]], pos: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[int, int]:
    x, y = pos[0] + direction[0], pos[1] + direction[1]
    if grid[x][y] == ".":
        grid[x][y] = "@"
        grid[pos[0]][pos[1]] = "."
        return (x, y)
    elif grid[x][y] == "#":
        return pos
    elif grid[x][y] != "O":
        raise Exception(f"What is this {grid[x][y]}, {(x, y)}")

    empty_space = None
    potential_space = (x, y)
    x, y = x + direction[0], y + direction[1]
    while True:
        curr = grid[x][y]
        if curr == ".":
            empty_space = (x, y)
            break
        elif curr == "#":
            break
        elif curr != "O":
            raise Exception(f"What is thisss {grid[x][y]}, {(x, y)}")
        x, y = x + direction[0], y + direction[1]

    if empty_space is None:
        return pos

    grid[empty_space[0]][empty_space[1]] = "O"
    grid[potential_space[0]][potential_space[1]] = "@"
    grid[pos[0]][pos[1]] = "."

    return potential_space

def move_direction_horizontal(grid: List[List[str]], pos: Tuple[int, int], direction: int) -> Tuple[int, int]:
    # print("pos", pos)
    x, y = pos[0], pos[1] + direction
    # print("pos", pos, "x, y", (x, y))
    if grid[x][y] == ".":
        grid[x][y] = "@"
        grid[pos[0]][pos[1]] = "."
        return (x, y)
    elif grid[x][y] == "#":
        return pos
    elif grid[x][y] != "[" and grid[x][y] != "]":
        raise Exception(f"What is this {grid[x][y]}, {(x, y)}")

    empty_space = None
    potential_space = (x, y)
    x, y = x, y + direction
    while True:
        curr = grid[x][y]
        if curr == ".":
            empty_space = (x, y)
            break
        elif curr == "#":
            break
        elif grid[x][y] != "[" and grid[x][y] != "]":
            raise Exception(f"What is thisss {grid[x][y]}, {(x, y)}")
        x, y = x, y + direction

    if empty_space is None:
        return pos

    # print("direction", direction)
    # print("empty_space", empty_space)
    # print("potential_space", potential_space)
    for i in range(empty_space[1], potential_space[1], -direction):
        grid[x][i] = grid[x][i + (-direction)]


    grid[potential_space[0]][potential_space[1]] = "@"
    grid[pos[0]][pos[1]] = "."

    return potential_space

def move_direction_vertical(grid: List[List[str]], pos: Tuple[int, int], direction: int) -> Tuple[int, int]:
    x, y = pos[0] + direction, pos[1]
    # print("pos", pos, "x, y", (x, y))
    if grid[x][y] == ".":
        grid[x][y] = "@"
        grid[pos[0]][pos[1]] = "."
        return (x, y)
    elif grid[x][y] == "#":
        return pos
    elif grid[x][y] != "[" and grid[x][y] != "]":
        raise Exception(f"What is this {grid[x][y]}, {(x, y)}")

    things_to_be_moved: List[List[Tuple[int, int]]] = [[(pos[0], pos[1])]]
    while True:
        next_row_to_check = list(map(lambda val: val[1], things_to_be_moved[-1]))
        left = min(next_row_to_check)
        right = max(next_row_to_check)
        current_row = things_to_be_moved[-1][0][0] + direction
        next_row_to_move = []
        # print("left / right", (left, right))
        for i in range(left, right + 1):
            if grid[current_row][i] == "#":
                return pos

            if grid[current_row][i] == "]":
                next_row_to_move.append((current_row, i-1))
                next_row_to_move.append((current_row, i))
            elif grid[current_row][i] != "." and grid[current_row][i] != "[":
                raise Exception(f"What is this {grid[current_row][i]}, {(current_row, i)}")
        # print("grid[current_row][right]", (current_row, right), grid[current_row][right])
        if grid[current_row][right] == "[":
            # annoying edge case and i don't want to go back and change things anymore
            next_row_to_move.append((current_row, right))
            next_row_to_move.append((current_row, right+1))

        # print("next_row_to_move", next_row_to_move)
        if len(next_row_to_move) < 1:
            break
        else:
            things_to_be_moved.append(next_row_to_move)

    for row in things_to_be_moved[::-1]:
        for box in row:
            # print("box", box)
            grid[box[0] + direction][box[1]] = grid[box[0]][box[1]]
            grid[box[0]][box[1]] = "."

    return (x, y)

def update_warehouse(grid: List[List[str]], start: Tuple[int, int], moves: List[str]) -> List[List[str]]:
    warehouse = list(map(lambda x: x.copy(), grid))
    pos = start
    for m in moves:
        match m:
            case "^":
                # print("move up")
                pos = move_direction(warehouse, pos, (-1, 0))
            case "v":
                # print("move down")
                pos = move_direction(warehouse, pos, (1, 0))
            case "<":
                # print("move left")
                pos = move_direction(warehouse, pos, (0, -1))
            case ">":
                # print("move right")
                pos = move_direction(warehouse, pos, (0, 1))

    return warehouse

def update_warehouse_2(grid: List[List[str]], start: Tuple[int, int], moves: List[str]) -> List[List[str]]:
    warehouse = list(map(lambda x: x.copy(), grid))
    pos = start
    for m in moves:
        match m:
            case "^":
                # print("move up")
                pos = move_direction_vertical(warehouse, pos, -1)
            case "v":
                # print("move down")
                pos = move_direction_vertical(warehouse, pos, 1)
            case "<":
                # print("move left")
                pos = move_direction_horizontal(warehouse, pos, -1)
            case ">":
                # print("move right")
                pos = move_direction_horizontal(warehouse, pos, 1)

        # print("!! =====")
        # print("current", pos, "move", m)
        # for r in warehouse:
        #     print("".join(r))

    return warehouse

def calculate_score(grid: List[List[str]], target: str) -> int:
    score = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == target:
                score += (i * 100 + j)

    return score

def widen_warehouse(grid: List[List[str]]) -> List[List[str]]:
    warehouse = []
    for r in grid:
        row = []
        for i in range(len(r)):
            if r[i] == "#":
                row.extend(["#", "#"])
            if r[i] == ".":
                row.extend([".", "."])
            if r[i] == "O":
                row.extend(["[", "]"])
            if r[i] == "@":
                row.extend(["@", "."])

        warehouse.append(row)

    return warehouse


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    grid, moves = parse_inputs(options.get("filepath", args[0]))

    start = find_robot_pos(grid, "@")
    warehouse = update_warehouse(grid, start, moves)

    # for r in warehouse:
    #     print("".join(r))

    score = calculate_score(warehouse, "O")

    print(f"Score: {score}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)

    grid, moves = parse_inputs(options.get("filepath", args[0]))

    if args[0] == "debug":
        warehouse = grid
    else:
        warehouse = widen_warehouse(grid)

    # for r in warehouse:
    #     print("".join(r))
    start = find_robot_pos(warehouse, "@")
    warehouse = update_warehouse_2(warehouse, start, moves)

    # print("======")
    # for r in warehouse:
    #     print("".join(r))

    score = calculate_score(warehouse, "[")

    print(f"Score: {score}")