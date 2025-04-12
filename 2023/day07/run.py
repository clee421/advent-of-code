import itertools
from typing import Dict, List, Tuple

CARD_VALUE = {
    "A": "13",
    "K": "12",
    "Q": "11",
    "J": "10",
    "T": "09",
    "9": "08",
    "8": "07",
    "7": "06",
    "6": "05",
    "5": "04",
    "4": "03",
    "3": "02",
    "2": "01",
}

CARD_VALUE_2 = {
    "A": "13",
    "K": "12",
    "Q": "11",
    "J": "00",
    "T": "09",
    "9": "08",
    "8": "07",
    "7": "06",
    "6": "05",
    "5": "04",
    "4": "03",
    "3": "02",
    "2": "01",
}

TYPE_VALUE = {
    "five_kind": "7",
    "four_kind": "6",
    "full_house": "5",
    "three_kind": "4",
    "two_pair": "3",
    "one_pair": "2",
    "high_card": "1",
}

def parse_inputs(filepath: str) -> List[Tuple[str, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    hands = []
    for l in lines:
        res = l.split(" ")
        hands.append((res[0], int(res[1])))

    return hands

def to_type(hand: str) -> str:
    card_count = {}
    for c in hand:
        v = card_count.get(c, 0)
        card_count[c] = v + 1

    card_count_values = list(card_count.values())
    if len(card_count_values) == 1 and card_count_values[0] == 5:
        return "five_kind"
    elif len(card_count_values) == 2 and 4 in card_count_values:
        return "four_kind"
    elif len(card_count_values) == 2 and 3 in card_count_values and 2 in card_count_values:
        return "full_house"
    elif len(card_count_values) == 3 and 3 in card_count_values:
        return "three_kind"
    elif len(card_count_values) == 3 and card_count_values.count(2) == 2:
        return "two_pair"
    elif len(card_count_values) == 4 and card_count_values.count(2) == 1:
        return "one_pair"
    else:
        return "high_card"

def to_value(hand: str) -> int:
    """
    Converting a hand into a point value. The cards are worth double digit points
    as so:
    A - 13
    K - 12
    Q - 11
    J - 10
    T - 09
    9 - 08
    8 - 07
    7 - 06
    6 - 05
    5 - 04
    4 - 03
    3 - 02
    2 - 01

    With the left most card taking precedence in value. So the hand AQ962 valuing
    at => 1311080501

    The type will mark the 11th digit for points
    Five of a kind       - 70000000000
    Four of a kind       - 60000000000
    Full house of a kind - 50000000000
    Three of a kind      - 40000000000
    Two pair of a kind   - 30000000000
    One pair of a kind   - 20000000000
    High card of a kind  - 10000000000
    """

    value = ""
    for c in hand:
        value += CARD_VALUE[c]

    hand_type = to_type(hand)
    if hand_type not in TYPE_VALUE:
        raise Exception(f"I broke something {hand} {hand_type}")

    return int(f"{TYPE_VALUE[hand_type]}{value}")

def to_value_2(hand: str) -> int:
    # print(f"HAND ====== {hand} ======")
    card_count = {}
    for c in hand:
        v = card_count.get(c, 0)
        card_count[c] = v + 1

    # Nothing changes w/o jokers
    if "J" not in card_count:
        return to_value(hand)

    # print(f"j count {card_count["J"]}")
    cartesian_product_list = list(itertools.product(list(card_count.keys()), repeat=card_count["J"]))
    # print(cartesian_product_list)

    # Find the max value type, but joker is still trash
    max_value = 0
    for p in cartesian_product_list:
        new_hand = ""

        i = 0
        for c in hand:
            if c != "J":
                new_hand += c
            else:
                new_hand += p[i]
                i += 1

        # print(f"new hand {new_hand}")
        curr_value = int(TYPE_VALUE[to_type(new_hand)])
        max_value = max(max_value, curr_value)

    value = ""
    for c in hand:
        value += CARD_VALUE_2[c]

    return int(f"{max_value}{value}")


def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    hands = parse_inputs(options.get("filepath", args[0]))

    valued_hands = []
    for hand in hands:
        valued_hands.append((to_value(hand[0]), hand[0], hand[1]))

    valued_hands.sort(key=lambda e: e[0])

    total = 0
    for i, h in enumerate(valued_hands):
        total += ((i + 1) * h[2])

    print(f"Total: {total}")


def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    hands = parse_inputs(options.get("filepath", args[0]))

    # hands = [("T55J5", 684)]

    valued_hands = []
    for hand in hands:
        valued_hands.append((to_value_2(hand[0]), hand[0], hand[1]))

    valued_hands.sort(key=lambda e: e[0])

    # print(valued_hands)

    total = 0
    for i, h in enumerate(valued_hands):
        total += ((i + 1) * h[2])

    print(f"Total: {total}")