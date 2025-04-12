import math
from typing import Dict, List, Tuple

def parse_inputs(filepath: str) -> List[str]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]
        times = [int(e) for e in filter(lambda v: v and v != "Time:", lines[0].split(" "))]
        distances = [int(e) for e in filter(lambda v: v and v != "Distance:", lines[1].split(" "))]

    return list(zip(times, distances))

def range_time_for_velo(time: int, dist: int) -> Tuple[float, float]:
    """
    Given the following:
    a - hold time => velocity
    y - total time
    b - time left
    x - total distance

    # The time left is the difference between the velocity and total time
    y - a = b

    # The velocity with the time left has to be greater than or equal to whole distance
    a * b >= x

    # This means the minimum velocity(a) needed is
    a = (y +/- sqrt(y^2 - 4x)) / 2
    """

    # Adding extra 1 because we have to beat the distance
    dist += 1
    discriminant = time**2 - (4 * dist)
    if discriminant < 0:
        raise Exception(f"time: {time}, dist: {dist} is not valid!")

    sqrt_term = math.sqrt(discriminant)

    a1 = (time + sqrt_term) / 2
    a2 = (time - sqrt_term) / 2

    return a1, a2

# keyword is BEAT the distance
def get_diff_ways_beat_dist(time: int, dist: int) -> int:
    result = range_time_for_velo(time, dist)
    # print(result)

    # floor the upper limit because you can't go over the time
    upper = math.floor(result[0])

    # ceil the lower because you can only travel at whole numbers
    lower = math.ceil(result[1])

    # print(upper - lower + 1)

    # Add 1 to include the lower / upper number
    return upper - lower + 1

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    total = 1
    for i in inputs:
        total *= get_diff_ways_beat_dist(i[0], i[1])

    print(f"Total: {total}")

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    inputs = parse_inputs(options.get("filepath", args[0]))

    time = ""
    dist = ""
    for i in inputs:
        time += str(i[0])
        dist += str(i[1])

    # print(time, dist)
    total = get_diff_ways_beat_dist(int(time), int(dist))

    print(f"Total: {total}")