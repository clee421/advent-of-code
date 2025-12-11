from typing import Dict, List, Tuple
from math import dist
import heapq

def parse_inputs(filepath: str) -> List[Tuple[int, int, int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    junction_boxes = []
    for l in lines:
        x, y, z = list(map(lambda e: int(e), l.split(",")))
        junction_boxes.append((x, y, z))

    return junction_boxes

class DSU:
    def __init__(self, nodes: List[Tuple[int, int, int]]):
        self.parent = {n: n for n in nodes}
        self.size = {n: 1 for n in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def join_circuits(junction_boxes: List[Tuple[int, int, int]], connections: int) -> int:
    dsu = DSU(junction_boxes)

    heap = []
    n = len(junction_boxes)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = junction_boxes[i], junction_boxes[j]
            heapq.heappush(heap, (dist(a, b), a, b))

    added = 0
    while heap and added < connections:
        _, a, b = heapq.heappop(heap)
        dsu.union(a, b)
        added += 1

    comp_sizes: Dict[Tuple[int, int, int], int] = {}
    for node in junction_boxes:
        root = dsu.find(node)
        comp_sizes[root] = dsu.size[root]

    top3 = sorted(comp_sizes.values(), reverse=True)[:3]
    product = 1
    for s in top3:
        product *= s
    return product

def calculate_last_two_circuits(junction_boxes: List[Tuple[int, int, int]]) -> int:
    dsu = DSU(junction_boxes)

    heap = []
    n = len(junction_boxes)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = junction_boxes[i], junction_boxes[j]
            heapq.heappush(heap, (dist(a, b), a, b))

    components = n
    last_edge: Tuple[Tuple[int, int, int], Tuple[int, int, int]] | None = None

    while heap and components > 1:
        _, a, b = heapq.heappop(heap)
        if dsu.union(a, b):
            components -= 1
            last_edge = (a, b)

    if last_edge:
        return last_edge[0][0] * last_edge[1][0]

    return -1

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    junction_boxes = parse_inputs(options.get("filepath", args[0]))

    connections = 1000
    if args[0] == "sample":
        connections = 10

    product = join_circuits(junction_boxes, connections=connections)
    print(f"Result: {product}")


def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    junction_boxes = parse_inputs(options.get("filepath", args[0]))

    result = calculate_last_two_circuits(junction_boxes)
    print(f"Result: {result}")
