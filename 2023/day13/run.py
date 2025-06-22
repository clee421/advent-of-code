from typing import Dict, List, Tuple, Set

def parse_inputs(filepath: str) -> List[List[List[str]]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    patterns = []
    pattern = []
    for l in lines:
        if l == "":
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(l)

    patterns.append(pattern)

    return patterns

def validate_vertical_split(entry: Tuple[int], pattern: List[str]) -> bool:
    if abs(entry[0] - entry[1]) > 1:
        return False

    # row_len = len(pattern[0])
    # sighs... i didn"t need to wrap around
    # required_matches = int(row_len / 2)
    # for i in range(required_matches):

    j1, j2 = entry[0], entry[1]
    while j1 >= 0 and j2 < len(pattern[0]):
        for row in range(len(pattern)):
            if pattern[row][j1] != pattern[row][j2]:
                return False
        j1 -= 1
        j2 += 1

    return True

def validate_horizontal_split(entry: Tuple[int], pattern: List[str]) -> bool:
    if abs(entry[0] - entry[1]) > 1:
        return False

    # same BS as above
    # pattern_len = len(pattern)
    # required_matches = int(pattern_len / 2)
    # for i in range(required_matches):
    #     j1, j2 = entry[0] - i, (entry[1] + i) % pattern_len
    #     if pattern[j1] != pattern[j2]:
    #         return False

    j1, j2 = entry[0], entry[1]
    while j1 >= 0 and j2 < len(pattern):
        if pattern[j1] != pattern[j2]:
            return False
        j1 -= 1
        j2 += 1

    return True

def get_vertical_split(pattern: List[str]) -> int:
    pairs = []
    row_len = len(pattern[0])
    for col_i in range(row_len):
        for col_j in range(col_i + 1, row_len):
            same_col = True
            for row in range(len(pattern)):
                if pattern[row][col_i] != pattern[row][col_j]:
                    same_col = False
                    break

            if same_col:
                pairs.append((col_i, col_j))
                break

    for pair in pairs:
        if validate_vertical_split(pair, pattern):
            return pair[1]

    return -1

def get_horizontal_split(pattern: List[str]) -> int:
    pairs = []
    pattern_len = len(pattern)
    for row_i in range(pattern_len):
        for row_j in range(row_i + 1, pattern_len):
            if pattern[row_i] == pattern[row_j]:
                pairs.append((row_i, row_j))
                break

    for pair in pairs:
        if validate_horizontal_split(pair, pattern):
            return pair[1]

    return -1

def summarize(pattern: List[str]) -> int:
    v = get_vertical_split(pattern)
    if v == -1:
        v = get_horizontal_split(pattern)
        if v == -1:
            return -1
        v *= 100

    return v

def is_v_mirror(pat: List[str], split: int) -> bool:
    h, w = len(pat), len(pat[0])
    offset = 0
    while split - offset >= 0 and split + 1 + offset < w:
        for r in range(h):
            if pat[r][split - offset] != pat[r][split + 1 + offset]:
                return False
        offset += 1
    return offset > 0


def is_h_mirror(pat: List[str], split: int) -> bool:
    h = len(pat)
    offset = 0
    while split - offset >= 0 and split + 1 + offset < h:
        if pat[split - offset] != pat[split + 1 + offset]:
            return False
        offset += 1
    return offset > 0

def find_mirrors(pat: List[str]) -> Tuple[Set[int], Set[int]]:
    h, w = len(pat), len(pat[0])
    vs: Set[int] = set()
    hs: Set[int] = set()

    for c in range(w - 1):
        if is_v_mirror(pat, c):
            vs.add(c + 1)

    for r in range(h - 1):
        if is_h_mirror(pat, r):
            hs.add(100 * (r + 1))

    return vs, hs

def summarize_2(pat: List[str]) -> int:
    vs, hs = find_mirrors(pat)
    if vs:
        return next(iter(vs))
    if hs:
        return next(iter(hs))
    raise ValueError("pattern has no mirror line (should not happen)")

def summarize_with_smudge(pat: List[str]) -> int:
    OPP = str.maketrans(".#", "#.")
    base_score = summarize_2(pat)
    used = {base_score}

    h, w = len(pat), len(pat[0])

    for r in range(h):
        for c in range(w):
            flipped_row = pat[r][:c] + pat[r][c].translate(OPP) + pat[r][c + 1:]
            cand = pat[:r] + [flipped_row] + pat[r + 1:]

            vs, hs = find_mirrors(cand)
            for s in vs | hs:
                if s not in used:
                    return s

    raise RuntimeError("pattern seems to need more than one smudge")

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    patterns = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for p in patterns:
        s = summarize(p)
        total += s

    print(f"Total: {total}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    patterns = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for p in patterns:
        s = summarize_with_smudge(p)
        total += s

    print(f"Total: {total}")