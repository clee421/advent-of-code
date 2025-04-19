from typing import Dict, List, Tuple

COL_A = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}

COL_B = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

POINT_MAP = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

RESULT_POINT = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

HAND_MAP = {
    "rock": {
        "X": POINT_MAP["scissors"],
        "Y": POINT_MAP["rock"],
        "Z": POINT_MAP["paper"],
    },
    "paper": {
        "X": POINT_MAP["rock"],
        "Y": POINT_MAP["paper"],
        "Z": POINT_MAP["scissors"],
    },
    "scissors": {
        "X": POINT_MAP["paper"],
        "Y": POINT_MAP["scissors"],
        "Z": POINT_MAP["rock"],
    },
}

def parse_inputs(filepath: str) -> List[Tuple[str, str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    games = []
    for l in lines:
        res = l.split(" ")
        games.append((res[0], res[1]))

    return games

def calculate_RSP(left: str, right: str) -> Tuple[int, int]:
    if left == right:
        return (3, 3)

    if left == "rock" and right == "paper":
        return (0, 6)
    if left == "rock" and right == "scissors":
        return (6, 0)

    if left == "paper" and right == "scissors":
        return (0, 6)
    if left == "paper" and right == "rock":
        return (6, 0)

    if left == "scissors" and right == "rock":
        return (0, 6)
    if left == "scissors" and right == "paper":
        return (6, 0)

    raise Exception("this should to happen")


def calculate_game(game: Tuple[str]) -> Tuple[int, int]:
    left_points = 0
    right_points = 0

    left_hand = COL_A[game[0]]
    right_hand = COL_B[game[1]]

    # The score for a single round is the score for the
    # shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
    left_points += POINT_MAP[left_hand]
    right_points += POINT_MAP[right_hand]

    match_res = calculate_RSP(left_hand, right_hand)
    left_points += match_res[0]
    right_points += match_res[1]

    return (left_points, right_points)

def calculate_game_2(game: Tuple[str]) -> int:
    # points = 0
    # points += RESULT_POINT[game[1]]
    # points += HAND_MAP[COL_A[game[0]]][game[1]]

    return RESULT_POINT[game[1]] + HAND_MAP[COL_A[game[0]]][game[1]]

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    games = parse_inputs(options.get("filepath", args[0]))

    opponent = 0
    me = 0
    for g in games:
        result = calculate_game(g)
        opponent += result[0]
        me += result[1]

    print(f"My score: {me}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    games = parse_inputs(options.get("filepath", args[0]))

    me = 0
    for g in games:
        me += calculate_game_2(g)

    print(f"My score: {me}")