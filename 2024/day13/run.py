import re
import time
from typing import Dict, List, Tuple

class Button:
    def __init__(self, x: int, y: int, cost: int):
        self._x = x
        self._y = y
        self._cost = cost

    @staticmethod
    def from_string(text: str) -> "Button":
        result = re.search("^Button ([A|B]):\\sX\\+(\\d+),\\sY\\+(\\d+)$", text)
        # print(result)
        cost = 0
        match result[1]:
            case "A":
                cost = 3
            case "B":
                cost = 1

        return Button(int(result[2]), int(result[3]), cost)


class Prize:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @staticmethod
    def from_string(text: str) -> "Prize":
        result = re.search("^Prize:\\sX\\=(\\d+),\\sY\\=(\\d+)$", text)
        return Prize(int(result[1]), int(result[2]))

class Machine:
    def __init__(self, a: Button, b: Button, prize: Prize):
        self._a = a
        self._b = b
        self._prize = prize

def parse_button_prize(filepath: str) -> List[Machine]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    machines = []
    for i in range(0, len(lines), 4):
        a = Button.from_string(lines[i])
        b = Button.from_string(lines[i+1])
        p = Prize.from_string(lines[i+2])
        machines.append(Machine(a, b, p))

    return machines

# def dfs(a: Tuple[int, int, int], b: Tuple[int, int, int], target: Tuple[int, int], count: int = 1) -> int:
#     print("target", target, "count", count)
#     if count > 30:
#         return -1

#     # assume a costs less than b
#     if target[0] == a[0] and target[1] == a[1]:
#         return a[2]
#     elif target[0] == b[0] and target[1] == b[1]:
#         return b[2]
#     elif target[0] < 0 or target[1] < 0:
#         return -1

#     left_dfs = dfs(a, b, (target[0] - a[0], target[1] - a[1]), count + 1)
#     right_dfs = dfs(a, b, (target[0] - b[0], target[1] - b[1]), count + 1)

#     if left_dfs == -1 and right_dfs == -1:
#         print("can't reach prize")
#         return -1
#     elif left_dfs == -1:
#         print("a button failed")
#         return right_dfs + b[2]
#     elif right_dfs == -1:
#         print("b button failed")
#         return left_dfs + a[2]
#     else:
#         left_total = left_dfs + a[2]
#         right_total = right_dfs + b[2]
#         return min(left_total, right_total)

# def find_minimal_coins(m: Machine) -> int:
#     ordered_by_costs = sorted([m._a, m._b], key=lambda x: x._cost)
#     a, b = ordered_by_costs[0], ordered_by_costs[1]

#     print(f"Running calc on {(a._x, a._y, a._cost)}, {(b._x, b._y, b._cost)}, {(m._prize._x, m._prize._y)}")
#     return dfs((a._x, a._y, a._cost), (b._x, b._y, b._cost), (m._prize._x, m._prize._y))

# def find_minimal_coins(m: Machine) -> int:
#     delta = [(m._a._x, m._a._y, m._a._cost), (m._b._x, m._b._y, m._b._cost)]

#     seen = {}

#     start = time.time()
#     elapsed_time = start + 5
#     queue = [(m._a._x, m._a._y, m._a._cost), (m._b._x, m._b._y, m._b._cost)]
#     while len(queue) > 0:
#         if time.time() > elapsed_time:
#             now = time.time()
#             elapsed_time = now + 10
#             print(f"Queue is size: {len(queue)}. Total elapsed time {now - start}")
#             print(f"Top of queue is {queue[0]}")

#         # (curr_x, curr_y, curr_cost)
#         curr = queue.pop(0)

#         if curr[0] > m._prize._x or curr[1] > m._prize._y:
#             continue

#         # might have to do seen.get and use a min because you could have seen the leftover twice
#         # and you want to only keep the minimal seen
#         seen[(curr[0], curr[1])] = curr[2]

#         if curr[0] == m._prize._x and curr[1] == m._prize._y:
#             return curr[2]

#         target_difference = (m._prize._x - curr[0], m._prize._y - curr[1])
#         if target_difference in seen:
#             return curr[2] + seen[target_difference]

#         for d in delta:
#             queue.append((curr[0] + d[0], curr[1] + d[1], curr[2] + d[2]))

#     return 0

def find_combinations_for_target(a: int, b: int, target: int) -> List[Tuple[int, int]]:
    combinations = []

    end_range = 100
    for n in range(1, end_range + 1):
        y = (target - (a * n)) / b
        if int(y) == y:
            combinations.append((n, y))

    return combinations

def find_minimal_coins(m: Machine) -> int:
    x_combinations = find_combinations_for_target(m._a._x, m._b._x, m._prize._x)
    y_combinations = find_combinations_for_target(m._a._y, m._b._y, m._prize._y)

    overlaps = set()
    for x in x_combinations:
        for y in y_combinations:
            if x == y:
                overlaps.add(x)

    overlaps_list = list(overlaps)
    if len(overlaps) <= 0:
        # print("could not find possible combination")
        return 0

    minimal_cost = overlaps_list[0]
    for c in overlaps:
        # b is second in the tuple so we want to maximize it
        if c[1] > minimal_cost[1]:
            minimal_cost = c

    # print("minimal_cost", minimal_cost)
    return (minimal_cost[0] * m._a._cost) + (minimal_cost[1] * m._b._cost)

# wolfram alpha
# solve(a*x1 + b*x2 = x3, a*y1 + b*y2 = y3, [a,b])
def find_minimal_coins_2(m: Machine) -> int:
    x_1, x_2, x_3, y_1, y_2, y_3 = m._a._x, m._b._x, m._prize._x, m._a._y, m._b._y, m._prize._y
    a = ((x_3 * y_2) - (x_2 * y_3)) / ((x_1 * y_2) - (x_2 * y_1))
    b = ((x_3 * y_1) - (x_1 * y_3)) / ((x_2 * y_1) - (x_1 * y_2))

    cost = 0
    if int(a) == a and int(b) == b:
        cost = (a * m._a._cost) + (b * m._b._cost)

    return cost

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    machines = parse_button_prize(options.get("filepath", args[0]))

    # result = find_minimal_coins(machines[0])
    # print(result)

    total_coins = 0
    for m in machines:
        # s = find_minimal_coins(m)
        s = find_minimal_coins_2(m)
        # print(f"Score for prize X={m._prize._x}, Y={m._prize._y} is {s}")
        total_coins += s

    print(f"Total coins:", total_coins)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    machines = parse_button_prize(options.get("filepath", args[0]))

    # result = find_minimal_coins(machines[0])
    # print(result)

    error_add = 10000000000000
    total_coins = 0
    for m in machines:
        m._prize._x += error_add
        m._prize._y += error_add
        s = find_minimal_coins_2(m)
        # print(f"Score for prize X={m._prize._x}, Y={m._prize._y} is {s}")
        total_coins += s

    print(f"Total coins:", total_coins)