from typing import Dict, List

def parse_inputs(filepath: str) -> Dict[str, List[str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    adj_list = {}
    for l in lines:
        res = l.split(": ")
        adj_list[res[0]] = res[1].split(" ")

    return adj_list

def count_outs(adj_list: Dict[str, List[str]]) -> int:
    out_count = 0
    queue = ["you"]
    while queue:
        curr = queue.pop(0)

        if curr == "out":
            out_count += 1
            continue

        if curr not in adj_list:
            raise Exception(f"{curr} not found in adj_list")

        for k in adj_list[curr]:
            queue.append(k)

    return out_count

def count_outs_2(adj_list: Dict[str, List[str]]) -> int:
    out_count = 0
    queue = [("svr", False, False)]
    while queue:
        curr = queue.pop(0)
        curr_k = curr[0]
        curr_fft = curr[1]
        curr_dac = curr[2]

        if curr_k == "out":
            if curr_fft and curr_dac:
                out_count += 1
            continue

        if curr_k not in adj_list:
            raise Exception(f"{curr_k} not found in adj_list")

        for k in adj_list[curr_k]:
            if k == "fft":
                queue.append((k, True, curr_dac))
            elif k == "dac":
                queue.append((k, curr_fft, True))
            else:
                queue.append((k, curr_fft, curr_dac))

    return out_count

def count_outs_3(adj_list: Dict[str, List[str]]) -> int:
    memo = {}

    def dfs(device: str, seen_fft: bool, seen_dac: bool) -> int:
        key = (device, seen_fft, seen_dac)
        if key in memo:
            return memo[key]

        if device == "out":
            return 1 if seen_fft and seen_dac else 0

        if device not in adj_list:
            raise Exception(f"{device} not found in adj_list")

        total = 0
        for next in adj_list[device]:
            total += dfs(
                next,
                seen_fft or next == "fft",
                seen_dac or next == "dac",
            )

        memo[key] = total
        return total

    return dfs("svr", False, False)


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    adj_list = parse_inputs(options.get("filepath", args[0]))

    result = count_outs(adj_list)
    print(f"Result: {result}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    adj_list = parse_inputs(options.get("filepath", args[0]))

    result = count_outs_3(adj_list)
    print(f"Result: {result}")
