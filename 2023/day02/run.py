from typing import Dict, List

MAX_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    games = []
    for line in lines:
        result = line.split(": ")
        left, right = result[0], result[1]
        left_result = left.split(" ")
        game_num = int(left_result[1])
        cube_sets = right.split("; ")
        cube_groups = []
        for cs in cube_sets:
            cube_map = {}
            cubes_str = cs.split(", ")
            for cube_str in cubes_str:
                cube_str_split = cube_str.split(" ")
                cube_map[cube_str_split[1]] = int(cube_str_split[0])

            cube_groups.append(cube_map)

        games.append({
            "game": game_num,
            "cube_groups": cube_groups,
        })

    return games

def game_possible(game: Dict["game": int, "cube_groups": List[Dict[str, int]]]) -> bool:
    for cube_group in game["cube_groups"]:
        for color, count in cube_group.items():
            if count > MAX_CUBES[color]:
                return False

    return True

def calculate_game_power(game: Dict["game": int, "cube_groups": List[Dict[str, int]]]) -> int:
    max_counter = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for cube_group in game["cube_groups"]:
        for color, count in cube_group.items():
            max_color_count = max_counter.get(color, 0)
            max_counter[color] = max(max_color_count, count)

    product = 1
    for v in max_counter.values():
        product *= v

    return product

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    games = parse_inputs(options.get("filepath", args[0]))

    score = 0
    for game in games:
        if game_possible(game):
            score += game["game"]

    print("Score:", score)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    games = parse_inputs(options.get("filepath", args[0]))

    power = 0
    for game in games:
        power += calculate_game_power(game)

    print("Power:", power)
