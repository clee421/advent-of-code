from typing import Dict, List

def parse_inputs(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    oasis_report_history = []
    for l in lines:
        oasis_report_history.append(
            [int(n) for n in l.split(" ")]
        )

    return oasis_report_history

def get_next_value(seq: List[int]) -> int:
    seq_history = [seq]
    while True:
        curr_seq = seq_history[-1]

        if len(set(curr_seq)) == 1:
            break

        new_seq = []
        for i in range(1, len(curr_seq)):
            new_seq.append(curr_seq[i] - curr_seq[i-1])

        seq_history.append(new_seq)

    # print(seq_history)

    for i in range(len(seq_history)-2, -1, -1):
        new_n = seq_history[i][-1] + seq_history[i+1][-1]
        seq_history[i].append(new_n)

    # print(seq_history)
    return seq_history[0][-1]

def get_prev_value(seq: List[int]) -> int:
    seq_history = [seq]
    while True:
        curr_seq = seq_history[-1]

        if len(set(curr_seq)) == 1:
            break

        new_seq = []
        for i in range(1, len(curr_seq)):
            new_seq.append(curr_seq[i] - curr_seq[i-1])

        seq_history.append(new_seq)

    for i in range(len(seq_history)-2, -1, -1):
        new_n = seq_history[i][0] - seq_history[i+1][0]
        seq_history[i].insert(0, new_n)

    # print(seq, seq_history[0][0])
    return seq_history[0][0]


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    oasis_report_history = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for orh in oasis_report_history:
        total += get_next_value(orh)

    print(f"Total: {total}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    oasis_report_history = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for orh in oasis_report_history:
        total += get_prev_value(orh)

    print(f"Total: {total}")