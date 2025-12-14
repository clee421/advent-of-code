from typing import Dict, List, Tuple
from ortools.linear_solver import pywraplp

class Machine:
    def __init__(self, text: str):
        # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        parts = text.split(" ")

        text_lights = parts[0][1:-1]
        self.indicator_end_state = text_lights

        self.joltage_requirements = list(map(lambda e: int(e), parts[-1][1:-1].split(",")))

        self.buttons = []
        for text_button in parts[1:-1]:
            self.buttons.append(
                tuple(map(lambda e: int(e), text_button[1:-1].split(",")))
            )

    def __repr__(self) -> str:
        return f"{self.indicator_end_state} | {self.buttons} | {self.joltage_requirements}"

def parse_inputs(filepath: str) -> List[Machine]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    machines = [Machine(l) for l in lines]

    return machines

def get_new_state(state: str, toggle: Tuple[int]) -> str:
    new_state = list(state)
    for t in toggle:
        if new_state[t] == ".":
            new_state[t] = "#"
        else:
            new_state[t] = "."

    return "".join(new_state)

def calculate_min_button_press(machine: Machine) -> int:
    inital_state = "".join(["."] * len(machine.indicator_end_state))
    queue = [(inital_state, [], set())]

    while queue:
        curr = queue.pop(0)
        curr_state = curr[0]
        curr_path = curr[1]
        curr_seen = curr[2]

        for b in machine.buttons:
            if b in curr_seen:
                continue

            next_state = get_new_state(curr_state, b)
            if next_state == machine.indicator_end_state:
                return len(curr_path) + 1

            new_path = curr_path.copy()
            new_path.append(b)

            new_seen = curr_seen.copy()
            new_seen.add(b)

            queue.append((next_state, new_path, new_seen))

    return -1


def calculate_min_button_presses(machines: List[Machine]) -> int:
    count = 1
    total = 0
    for m in machines:
        # print(f"working on {count} / {len(machines)}; {m.indicator_end_state}")
        score = calculate_min_button_press(m)
        total += score

        count += 1

    return total

def _min_presses_for_machine(m: Machine) -> int:
    target = tuple(m.joltage_requirements)
    counters = len(target)
    buttons = m.buttons

    # Early infeasibility: any target counter with no button affecting it.
    affects = [0] * counters
    for b in buttons:
        for idx in b:
            affects[idx] += 1
    for i, t in enumerate(target):
        if t > 0 and affects[i] == 0:
            return -1

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        return -1

    x = [solver.IntVar(0, solver.infinity(), f"x_{i}") for i in range(len(buttons))]

    # Constraints: for each counter, sum of presses of buttons affecting it == target.
    for c in range(counters):
        solver.Add(
            sum(x[j] for j, b in enumerate(buttons) if c in b) == target[c]
        )

    # Objective: minimize total presses.
    solver.Minimize(solver.Sum(x))

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return -1

    return int(solver.Objective().Value())

def calculate_min_button_presses_voltage(machines: List[Machine]) -> int:
    count = 1
    total = 0
    for m in machines:
        # print(f"working on {count} / {len(machines)}; {m.joltage_requirements}")
        score = _min_presses_for_machine(m)
        total += score

        count += 1

    return total

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    machines = parse_inputs(options.get("filepath", args[0]))
    # print(machines)

    result = calculate_min_button_presses(machines)
    print(f"Result: {result}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    machines = parse_inputs(options.get("filepath", args[0]))

    result = calculate_min_button_presses_voltage(machines)
    print(f"Result: {result}")
