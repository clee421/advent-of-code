from typing import Dict, List

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    return list(map(lambda x: int(x), lines))

def mix_number(secret: int, n: int) -> int:
    return secret ^ n

def prune_number(secret: int) -> int:
    return secret % 16777216

def evolve_secret(secret: int) -> int:
    secret = mix_number(secret, secret * 64)
    secret = prune_number(secret)
    secret = mix_number(secret, int(secret / 32))
    secret = prune_number(secret)
    secret = mix_number(secret, secret * 2048)
    secret = prune_number(secret)

    return secret

def evolve_secret_by_n(secret: int, n: int) -> int:
    for _ in range(n):
        secret = evolve_secret(secret)

    return secret

def get_prices(secret: int, n: int) -> List[int]:
    prices = []
    for _ in range(n):
        secret = evolve_secret(secret)
        prices.append(secret % 10)

    return prices

def calculate_most_bananas(all_prices: List[List[int]]) -> int:
    seen = set()
    list_of_prices_map = []
    # print("calculating all the prices...")
    for i in range(len(all_prices)):
        price = all_prices[i]
        # if i % 10 == 0:
            # print("working on", i, "of", len(all_prices) - 1)
        price_map = {}
        change_list = []
        for p_index in range(1, len(price)):
            diff = price[p_index] - price[p_index-1]
            change_list.append(diff)
            if len(change_list) >= 4:
                change_set = (change_list[-4], change_list[-3], change_list[-2], change_list[-1])
                if change_set not in price_map:
                    price_map[change_set] = price[p_index]
                    seen.add(change_set)
        list_of_prices_map.append(price_map)

    # print("checking for max bananas...")
    max_bananas = 0
    for change_set in seen:
        local_total = 0
        for pm in list_of_prices_map:
            local_total += pm.get(change_set, 0)

        max_bananas = max(max_bananas, local_total)

    return max_bananas

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    total = 0
    for n in inputs:
        secret = evolve_secret_by_n(n, 2000)
        total += secret
        # print(f"{n}: {secret}")

    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    all_prices = []
    for n in inputs:
        prices = get_prices(n, 2000)
        all_prices.append(prices)

    # takes about 15 seconds
    bananas = calculate_most_bananas(all_prices)
    print("Bananas", bananas)

