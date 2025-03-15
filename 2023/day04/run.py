from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    def clean(arr: List[str]) -> List[int]:
        return list(map(lambda x: int(x), filter(lambda y: y != "", arr)))

    cards = []
    for l in lines:
        res = l.split(": ")
        card = res[1].strip().split("|")
        scratch_card, draws = card[0].strip().split(" "), card[1].strip().split(" ")


        cards.append((clean(scratch_card), clean(draws)))

    return cards

def calculate_scratch_card_match(card: List[int], draws: List[int]) -> int:
    card_set = set(card)
    count = 0
    for d in draws:
        if d in card_set:
            count += 1

    if count == 0:
        return count

    return count

def calculate_scratch_card(card: List[int], draws: List[int]) -> int:
    count = calculate_scratch_card_match(card, draws)

    if count == 0:
        return count

    return 2 ** (count - 1)

def calculate_total_scratch_card(cards: Tuple[List[int], List[int]]) -> int:
    total_cards = [1] * len(cards)

    points = []
    for c in cards:
        points.append(calculate_scratch_card_match(c[0], c[1]))

    sum_of_cards = 0
    for i in range(len(total_cards)):
        sum_of_cards += total_cards[i]

        card_points = points[i]
        # populate the next series of cards
        for j in range(card_points):
            next_card = i + j + 1
            total_cards[next_card] += total_cards[i]

    return sum_of_cards

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    cards = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for c in cards:
        total += calculate_scratch_card(c[0], c[1])

    print(f"Total: {total}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    cards = parse_inputs(options.get("filepath", args[0]))

    total = calculate_total_scratch_card(cards)
    print(f"Total: {total}")