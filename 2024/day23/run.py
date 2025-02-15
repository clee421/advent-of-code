import time
from typing import Dict, List, Tuple, Set

def parse_inputs(filepath: str) -> List[Tuple[str, str]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    connections = []
    for l in lines:
        res = l.split("-")
        connections.append((res[0], res[1]))

    return connections

def create_connection_map(connection_list: List[Tuple[str, str]]) -> Dict[str, Set[str]]:
    connection_map = {}
    for c in connection_list:
        l, r = c[0], c[1]

        l_set = connection_map.get(l, set())
        l_set.add(r)
        connection_map[l] = l_set

        r_set = connection_map.get(r, set())
        r_set.add(l)
        connection_map[r] = r_set

    return connection_map

def find_triples(connections: List[Tuple[str, str]], connection_map: Dict[str, Set[str]]) -> Set[str]:
    triple_set = set()
    for c in connections:
        first, second = c[0], c[1]
        for key, c_set in connection_map.items():
            if key != first and key != second:
                if first in c_set and second in c_set:
                    triple = [first, second, key]
                    triple.sort()
                    triple_set.add("-".join(triple))

    return triple_set

# def is_pc_connected_to_all(connection_map: Dict[str, Set[str]], cm_set: Set[str]) -> bool:
#     cm_set_list = list(cm_set)
#     for i in range(len(cm_set_list)):
#         a = cm_set_list[i]
#         for j in range(len(cm_set_list)):
#             if i == j:
#                 continue

#             if cm_set_list[j] not in connection_map[a]:
#                 return False

#     return True

# def find_largest_connection(connections: List[Tuple[str, str]], connection_map: Dict[str, Set[str]]) -> List[str]:
#     mapped_to_each_other = []
#     cm = create_connection_map(connections)
#     for cm_key, cm_set in cm.items():
#         if is_pc_connected_to_all(connection_map, cm_set):
#             cm_set_list = list(cm_set)
#             cm_set_list.sort()
#             mapped_to_each_other.append(",".join(cm_set_list))

#     return mapped_to_each_other

def all_node_match(connection_map: Dict[str, Set[str]], nodes: Set[str]) -> bool:
    nodes_list = list(nodes)
    for i_n in nodes_list:
        for j_n in nodes_list:
            if i_n != j_n:
                if j_n not in connection_map[i_n]:
                    return False
    return True

# def find_largest_connection(connections: List[Tuple[str, str]], connection_map: Dict[str, Set[str]]) -> Set[str]:
#     all_nodes = set(connection_map.keys())

#     start = time.time()
#     elapsed_time = start + 5
#     queue = [all_nodes]
#     while len(queue) > 0:
#         if time.time() > elapsed_time:
#             now = time.time()
#             elapsed_time = now + 10
#             print(f"Size of queue: {len(queue)}. Total elapsed time {now - start}")
#             print(f"Working on {nodes_to_check}")

#         nodes_to_check = queue.pop(0)
#         if all_node_match(connection_map, nodes_to_check):
#             return nodes_to_check

#         for node_to_remove in nodes_to_check:
#             sub_set_of_nodes_to_check = nodes_to_check.copy()
#             sub_set_of_nodes_to_check.remove(node_to_remove)

#             queue.append(sub_set_of_nodes_to_check)

#     raise Exception("did not find anything")

# Bron-Kerbosch algorithm
# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
# I just asked chatgpt for the algorithm
def find_all_cliques(connection_map: Dict[str, Set[str]]) -> List[Set[str]]:
    all_vertices = list(connection_map.keys())
    cliques = []

    def bron_kerbosch_recursive(R, P, X):
        # If both P and X are empty, we found a maximal clique
        if not P and not X:
            cliques.append(R)
            return

        # We copy the list of vertices in P, because we'll modify P in the loop
        for v in list(P):
            # Recurse with v added to R, and P and X restricted to neighbors of v
            neighbors_v = connection_map[v]
            bron_kerbosch_recursive(
                R.union({v}),
                P.intersection(neighbors_v),
                X.intersection(neighbors_v)
            )
            # Move v from P to X
            P.remove(v)
            X.add(v)

    bron_kerbosch_recursive(set(), set(all_vertices), set())

    return cliques

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    connections = parse_inputs(options.get("filepath", args[0]))

    cm = create_connection_map(connections)
    triple_set = find_triples(connections, cm)

    count = 0
    for trips in triple_set:
        trips_list = trips.split("-")
        for t in trips_list:
            if t.startswith("t"):
                count += 1
                break

    print("Count:", count)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    connections = parse_inputs(options.get("filepath", args[0]))

    cm = create_connection_map(connections)
    # for cm_key, cm_set in cm.items():
    #     print(len(cm_set))

    cliques = find_all_cliques(cm)
    max_size = 0
    for c in cliques:
        max_size = max(max_size, len(c))

    for c in cliques:
        if len(c) == max_size:
            password_list = list(c)
            password_list.sort()
            print("Pass:", ",".join(password_list))

