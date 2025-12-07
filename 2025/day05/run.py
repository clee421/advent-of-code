from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Inventory:
    ranges: List[Tuple[int, int]]
    ingredient_ids: List[int]

    def count_fresh_ingredients(self) -> int:
        fresh_count = 0
        for ii in self.ingredient_ids:
            for r in self.ranges:
                if r[0] <= ii <= r[1]:
                    fresh_count += 1
                    break

        return fresh_count

    def combine_ranges(self) -> List[List[int]]:
        combined_ranges_list: List[List[int]] = []
        sorted_ranges = sorted(self.ranges, key=lambda e: e[0])

        for sr in sorted_ranges:
            did_combine = False
            for crl in combined_ranges_list:
                if crl[0] <= sr[0] <= crl[1]:
                    crl[1] = max(sr[1], crl[1])
                    did_combine = True
                    break

            if not did_combine:
                combined_ranges_list.append([sr[0], sr[1]])

        return combined_ranges_list

    def total_fresh_ingredients(self) -> int:
        combined_ranges = self.combine_ranges()
        # print("combined ranges", combined_ranges)
        fresh_count = 0
        for r in combined_ranges:
            count = r[1] - r[0] + 1
            fresh_count += count

        return fresh_count

def parse_inputs(filepath: str) -> Inventory:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    ranges: List[Tuple[int, int]] = []
    ingredient_ids: List[int] = []
    part_1 = True
    for l in lines:
        if l == "":
            part_1 = False
            continue

        if part_1:
            r = l.split("-")
            ranges.append((int(r[0]), int(r[1])))
        else:
            ingredient_ids.append(int(l))

    return Inventory(ranges=ranges, ingredient_ids=ingredient_ids)

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inventory = parse_inputs(options.get("filepath", args[0]))

    print(f"Total: {inventory.count_fresh_ingredients()}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inventory = parse_inputs(options.get("filepath", args[0]))

    print(f"Total: {inventory.total_fresh_ingredients()}")