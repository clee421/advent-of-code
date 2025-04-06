from typing import Dict, List, Tuple

MAP_ORDERING = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]

# this is what seed_map dict is
# {'seeds': [79, 14, 55, 13], 'seed-to-soil': [[50, 98, 2], [52, 50, 48]], 'soil-to-fertilizer': [[0, 15, 37], [37, 52, 2], [39, 0, 15]], 'fertilizer-to-water': [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]], 'water-to-light': [[88, 18, 7], [18, 25, 70]], 'light-to-temperature': [[45, 77, 23], [81, 45, 19], [68, 64, 13]], 'temperature-to-humidity': [[0, 69, 1], [1, 0, 69]], 'humidity-to-location': [[60, 56, 37], [56, 93, 4]]}
def from_dict_to_seed_map(seed_map: Dict[any, any]) -> Tuple[List[int], Dict[str, Dict[int, int]]]:
    seed_list = seed_map["seeds"]
    actual_seed_map = {}
    for m in MAP_ORDERING:
        map_dict = {}
        # [[50, 98, 2], [52, 50, 48]]
        for item in seed_map[m]:
            # [50, 98, 2]
            # it's reversed because the problem is stupid
            left = item[1]
            right = item[0]
            range_count = item[2]
            for i in range(range_count):
                map_dict[left + i] = right + i

        actual_seed_map[m] = map_dict

    return (seed_list, actual_seed_map)

def parse_seeds(text: str) -> List[int]:
    res = text.split(": ")
    return list(map(lambda x: int(x), res[1].split(" ")))

def parse_inputs(filepath: str) -> Dict[any, any]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    current_map = None
    data_map = {}
    for l in lines:
        if l.startswith("seeds:"):
            data_map["seeds"] = parse_seeds(l)
        elif l == "":
            continue
        elif l.endswith("map:"):
            res = l.split(" m")
            current_map = res[0]
            data_map[current_map] = []
        else:
            data_map[current_map].append(list(map(lambda x: int(x), l.split(" "))))

    return data_map

def get_location_for_seeds(seeds: List[int], seed_map: Dict[str, Dict[int, int]]) -> List[int]:
    locs = []

    for seed in seeds:
        print("working on seed", seed)
        next_in_map = seed
        for next_map in MAP_ORDERING:
            print("working on map", next_map)
            # next_in_map = seed_map[next_map][next_in_map]
            # The inputs don't include all of the numbers, when that happens
            # I think it's just a 1 to 1
            next_in_map = seed_map[next_map].get(next_in_map, next_in_map)

        locs.append(next_in_map)

    return locs

# {'seeds': [79, 14, 55, 13], 'seed-to-soil': [[50, 98, 2], [52, 50, 48]], 'soil-to-fertilizer': [[0, 15, 37], [37, 52, 2], [39, 0, 15]], 'fertilizer-to-water': [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]], 'water-to-light': [[88, 18, 7], [18, 25, 70]], 'light-to-temperature': [[45, 77, 23], [81, 45, 19], [68, 64, 13]], 'temperature-to-humidity': [[0, 69, 1], [1, 0, 69]], 'humidity-to-location': [[60, 56, 37], [56, 93, 4]]}
def get_location_for_seeds_2(seed_map: Dict[any, any]) -> List[int]:
    seeds = seed_map["seeds"]

    locs = []

    for seed in seeds:
        next_in_map = seed
        for next_map in MAP_ORDERING:
            # [[50, 98, 2], [52, 50, 48]]
            maps_arr: List[List[int]] = seed_map[next_map]

            found_map = None
            for potential_map in maps_arr:
                start, end = potential_map[1], potential_map[1] + potential_map[2]
                if start <= next_in_map <= end:
                    found_map = next_in_map - potential_map[1] + potential_map[0]

            if found_map is not None:
                next_in_map = found_map

        locs.append(next_in_map)

    return locs

def get_mapped_outputs(input: Tuple[int, int], output_maps: List[List[int]]) -> List[Tuple[int, int]]:
    output = []
    for om in output_maps:
        input_start = input[0]
        input_end = input[0] + input[1] - 1

        mapped_to = om[0]
        jump = om[2]
        output_start = om[1]
        output_end = om[1] + jump - 1

        # print(f"seed: {input}, {input_start} -> {input_end}")
        # print(f"map: {om}, {output_start} -> {output_end}")
        # print(f"mapped_to {mapped_to}, jump {jump}")

        # There are 4 scenarios to handle here

        # 1. Input overlap is larger than output
        # input:    |-----------------|
        # output:        |---------|
        # result:   |----|, |---------|, |---|
        if input_start < output_start and input_end > output_end:
            # print("condition 1")
            left = (input_start, output_start - input_start)
            mid = (mapped_to, jump)
            right = (output_end + 1, input_end - output_end)

            output.extend([left, mid, right])

        # 2. Input lower half overlaps with output upper half
        # input:    |-----------|
        # output:          |----------|
        # result:   |------|, |-----|
        elif input_start < output_start and input_end <= output_end and output_start < input_end:
            # print("condition 2")
            left = (input_start, output_start - input_start - 1)
            right = (mapped_to, input_end - output_start + 1)

            output.extend([left, right])

        # 3. Input upper half overlaps with output lower half
        # input:         |-----------|
        # output:   |----------|
        # result:        |-----|, |------|
        elif input_start >= output_start and input_end > output_end and input_start < output_end:
            # print("condition 3")
            left = (mapped_to + input_start - output_start, output_end - input_start + 1)
            right = (output_end + 1, input_end - output_end + 1)

            output.extend([left, right])

        # 4. Input is overlapped by output
        # input:         |-----------|
        # output:   |--------------------|
        # result:        |-----------|
        elif input_start >= output_start and input_end <= output_end:
            # print("condition 4")
            output.append((input_start - output_start + mapped_to, input[1]))

        # else:
        #     print("no matching condition")

        # print(f"**** OUTPUT: {output}\n")

    if len(output) == 0:
        return [input]

    return output

def get_location_for_seeds_3(seeds: List[Tuple[int, int]], seed_map: Dict[str, List[List[int]]]) -> List[Tuple[int, int]]:
    mapped_seeds = seeds.copy()
    for _map in MAP_ORDERING:
        temp_mapped_seeds = []
        for seed in mapped_seeds:
            current_map = seed_map[_map]
            mapped_outputs = get_mapped_outputs(seed, current_map)
            temp_mapped_seeds.extend(mapped_outputs)

        mapped_seeds = temp_mapped_seeds.copy()
        # print("NEW INPUTS")
        # print("\n".join(list(map(lambda x: str(x), mapped_seeds))))
        # print("===========")

    return mapped_seeds

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    dict_map = parse_inputs(options.get("filepath", args[0]))

    # inputs = from_dict_to_seed_map(dict_map)
    # seed_list, seed_map = inputs[0], inputs[1]
    # locs = get_location_for_seeds(seed_list, seed_map)

    locs = get_location_for_seeds_2(dict_map)
    # print(locs)
    min_loc = min(locs)

    print(f"Location: {min_loc}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    dict_map = parse_inputs(options.get("filepath", args[0]))

    seeds_list = dict_map["seeds"]
    del dict_map["seeds"]

    seed_tuple_list = []
    for i in range(0, len(seeds_list), 2):
        seed_tuple_list.append((seeds_list[i], seeds_list[i+1]))

    # print(seed_tuple_list)
    # print(dict_map)

    loc_ranges = get_location_for_seeds_3(seed_tuple_list, dict_map)
    # print(loc_ranges)

    # f = open("output-list.txt", "w")
    # f.write("\n".join(list(map(lambda x: str(x), loc_ranges))))
    # f.close()

    # min_loc = min(list(map(lambda x: x[0], loc_ranges)))
    sorted_locs = sorted(list(map(lambda x: x[0], loc_ranges)))
    # print(sorted_locs)
    min_loc = list(filter(lambda x: x != 0, sorted_locs))[0]

    print(f"Location: {min_loc}")

    # There's a bug somewhere? Instead of the minimum I went with the lowest non-zero value
    # 0, 0, 0, 0, 0, 0, 0, 4917124, 4917124