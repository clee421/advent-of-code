import time
from typing import Dict, List, Tuple

def parse_lines_disk_map(filepath: str) -> List[Tuple[int, int, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    if len(lines) > 1:
        raise Exception("we should only have one line")

    compact_disk = []
    id = 0
    for i in range(0, len(lines[0]), 2):
        files = int(lines[0][i])

        free_space = 0
        if i+1 < len(lines[0]):
            free_space = int(lines[0][i+1])

        compact_disk.append((files, free_space, id))
        id += 1

    return compact_disk

def parse_lines_disk_map_2(filepath: str) -> List[Tuple[int, int, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    if len(lines) > 1:
        raise Exception("we should only have one line")

    compact_disk = []
    id = 0
    for i in range(0, len(lines[0]), 2):
        files = int(lines[0][i])

        free_space = 0
        if i+1 < len(lines[0]):
            free_space = int(lines[0][i+1])

        compact_disk.append((id, files))
        compact_disk.append((-1, free_space))
        id += 1

    return compact_disk

def defrag_expanded_disk(original_sequence: List[int | str]) -> List[int | str]:
    sequence = original_sequence.copy()
    print("    The sequence length is", len(sequence))
    i, j = 0, len(sequence)-1
    start = time.time()
    elapsed_time = start + 5
    while i < j:
        if time.time() > elapsed_time:
            now = time.time()
            elapsed_time = now + 10
            print(f"Currently working on i: {i}, j: {j}. Total elapsed time {now - start}")

        i = sequence.index(".")

        while sequence[j] == "." or j < 0:
            j -= 1

        if i >= j:
            break

        sequence[i] = sequence[j]
        sequence[j] = "."
        i += 1
        j -= 1

    return sequence

# def defrag_expanded_disk_2(old_disk_map: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
#     disk_map = old_disk_map.copy()
#     i = 0
#     end = len(disk_map)
#     while i < end:
#         files = disk_map[i][0]
#         free_space = disk_map[i][1]
#         id = disk_map[i][2]

#         j = len(disk_map) - 1
#         while j > i:
#             if disk_map[j][0] <= free_space:
#                 print("SWAPPING", i, disk_map[i], j, disk_map[j])
#                 new_files = disk_map[j][0]
#                 new_free_space = free_space - disk_map[j][0]
#                 new_id = disk_map[j][2]

#                 disk_map[j-1] = (disk_map[j-1][0], disk_map[j-1][1] + disk_map[j][0], disk_map[j-1][2])

#                 disk_map.pop(j)
#                 disk_map.insert(i+1, (new_files, new_free_space, new_id))

#                 disk_map[i] = (files, 0, id)

#                 print("CURRENT STATE", disk_map)
#                 break

#             j -= 1
#         i += 1

#     return disk_map

# def defrag_expanded_disk_3(old_disk_map: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
#     disk_map = old_disk_map.copy()
#     current = len(disk_map) - 1
#     while current >= 0:
#         target_files = disk_map[current][0]
#         target_free_space = disk_map[current][1]
#         target_id = disk_map[current][2]

#         found = 0
#         while found < current:
#             found_files = disk_map[found][0]
#             found_free_space = disk_map[found][1]
#             found_id = disk_map[found][2]
#             if found_free_space >= target_files:
#                 print("SWAPPING", current, disk_map[current], found, disk_map[found])
#                 new_free_space = found_free_space - target_files

#                 disk_map[found] = (found_files, 0, found_id)
#                 prev = current - 1
#                 disk_map[prev] = (disk_map[prev][0], disk_map[prev][1] + target_files + target_free_space, disk_map[prev][2])

#                 disk_map.pop(current)
#                 disk_map.insert(found+1, (target_files, new_free_space, target_id))

#                 # print("CURRENT STATE", disk_map)
#                 break
#             found += 1
#         current -= 1
#     # print("current:", current)

#     return disk_map

def defrag_expanded_disk_4(old_disk_map: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    disk_map = old_disk_map.copy()

    start = time.time()
    elapsed_time = start + 5
    for file_i in range(len(disk_map)-1, 0, -1):
        for free_space_i in range(file_i):
            if time.time() > elapsed_time:
                now = time.time()
                elapsed_time = now + 10
                print(f"Currently working on file_i: {file_i}, free_space_i: {free_space_i}. Total elapsed time {now - start}")

            if (disk_map[file_i][0] != -1
                and disk_map[free_space_i][0] == -1
                and disk_map[file_i][1] <= disk_map[free_space_i][1]
            ):
                moving_file = (disk_map[file_i][0], disk_map[file_i][1])
                new_free_space = (disk_map[free_space_i][0], disk_map[free_space_i][1] - disk_map[file_i][1])

                disk_map[file_i] = (-1, disk_map[file_i][1])
                disk_map[free_space_i] = new_free_space
                disk_map.insert(free_space_i, moving_file)

    return disk_map

def expanded_disk_4_to_string(input: List[Tuple[int, int]]) -> str:
    result = ""
    for i in range(len(input)):
        for _ in range(input[i][1]):
            if input[i][0] == -1:
                result += "."
            else:
                result += f"{input[i][0]}"

    return result


def calculate_checksum(sequence: str) -> int:
    checksum = 0
    for i in range(len(sequence)):
        if sequence[i] == ".":
            continue

        checksum += (i * int(sequence[i]))

    return checksum

def calculate_checksum_2(sequence: List[Tuple[int, int, int]]) -> int:
    checksum = 0
    index = 0
    for i in range(len(sequence)):
        end = index
        while index < (end + sequence[i][0]):
            checksum += (index * sequence[i][2])
            index += 1
        index += sequence[i][1]

    return checksum

def calculate_checksum_3(sequence: List[int | str]) -> int:
    checksum = 0
    for i in range(len(sequence)):
        if sequence[i] == ".":
            continue

        checksum += (i * sequence[i])

    return checksum

def calculate_checksum_4(sequence: List[Tuple[int, int]]) -> int:
    checksum = 0
    index = 0
    for i in range(len(sequence)):
        for _ in range(sequence[i][1]):
            if sequence[i][0] != -1:
                checksum += (index * sequence[i][0])

            index += 1

    return checksum

def create_pad_char_list(char: str, num: int) -> List[int | str]:
    result = []
    for _ in range(num):
        if char != ".":
            result.append(int(char))
        else:
            result.append(char)

    return result

def expand_files(tuple: Tuple[int, int, int]) -> List[int]:
    files = tuple[0]
    free_space = tuple[1]
    id = tuple[2]
    result = []
    for _ in range(files):
        result.append(id)
    for _ in range(free_space):
        result.append(".")

    return result

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    disk_map = parse_lines_disk_map(options.get("filepath", args[0]))

    expanded_list = []
    print("Expanding the disk map...")
    for index, dm in enumerate(disk_map):
        expanded_list.extend(create_pad_char_list(str(index), dm[0]))
        expanded_list.extend(create_pad_char_list(".", dm[1]))

    # print(expanded_list)

    print("Defragging the disk map...")
    defragged = defrag_expanded_disk(expanded_list)

    print("Calculating the checksum...")
    checksum = calculate_checksum(defragged)

    # print("EXPANDED LIST =========")
    # print(expanded_list)
    # print("DEFRAGGED STRING =========")
    # print(defragged)
    print("Checksum:", checksum)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    disk_map = parse_lines_disk_map_2(options.get("filepath", args[0]))

    # print(disk_map)

    print("Expanding the disk map...")
    defragged = defrag_expanded_disk_4(disk_map)
    # print(expanded_disk_4_to_string(defragged))
    # OUTPUT: 00992111777.44.333....5555.6666.....8888..
    # SOLUTI: 00992111777.44.333....5555.6666.....8888..

    print("Calculating the checksum...")
    # checksum = calculate_checksum_2(defragged)
    checksum = calculate_checksum_4(defragged)

    print("Checksum:", checksum)
