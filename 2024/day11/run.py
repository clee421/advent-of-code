from typing import Dict, List, Tuple
import time

def parse_lines_stones(filepath: str) -> List[int]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    if len(lines) > 1:
        raise Exception("we should only have one line")

    return list(map(lambda x: int(x), lines[0].split(" ")))

def blink(stones: List[int]) -> List[int]:
    new_stones = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif len(f"{s}") % 2 == 0:
            s_str = f"{s}"
            mid = int(len(s_str) / 2)
            new_stones.append(int(s_str[:mid]))
            new_stones.append(int(s_str[mid:]))
        else:
            new_stones.append(s * 2024)

    return new_stones


def calculate_memo_blinks(stones: List[int], blink_num: int, memo: Dict[Tuple[int, int], int]) -> int:
    if blink_num == 1:
        return len(blink(stones))

    total_stones = 0
    for s in stones:
        if (s, blink_num) not in memo:
            new_stone_s = blink([s])

            sub_stone_count = calculate_memo_blinks(new_stone_s, blink_num-1, memo)
            memo[(s, blink_num)] = sub_stone_count
        # else:
            # print(f"Found {(s, blink_num)} in memo!")

        total_stones += memo[(s, blink_num)]

    return total_stones

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    stones = parse_lines_stones(options.get("filepath", args[0]))

    num_blinks = 25
    for _ in range(num_blinks):
        stones = blink(stones)

    print("Total stones:", len(stones))

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    stones = parse_lines_stones(options.get("filepath", args[0]))

    memo: Dict[Tuple[int, int], int] = {}
    total_stones = calculate_memo_blinks(stones, 75, memo)

    print("Total stones:", total_stones)
