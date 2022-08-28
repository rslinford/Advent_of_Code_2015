import math
import re


class Edge:
    def __init__(self, from_city, to_city, distance):
        self.from_city = from_city
        self.to_city = to_city
        self.distance = distance

    def __repr__(self):
        return f'{self.__class__.__name__} from_city({self.from_city}) to_city({self.to_city}) distance({self.distance})'

    def __hash__(self):
        return hash((self.from_city, self.to_city))

    def __eq__(self, other):
        return self.from_city == other.from_city and self.to_city == other.to_city

    def __lt__(self, other):
        return self.from_city < other.from_city


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_line(line):
    result = re.search(r'(\w+) to (\w+) = (\d+)', line)
    return result.group(1), result.group(2), int(result.group(3))


def distance(vertex_one, vertex_two, edges: dict[(str, str)]):
    if (vertex_one, vertex_two) in edges:
        return edges[vertex_one, vertex_two].distance
    if (vertex_two, vertex_one) in edges:
        return edges[vertex_two, vertex_one].distance
    raise ValueError(f'Edge for {vertex_one}, {vertex_two} not found.')


def build_edges(data):
    edges: dict[(str, str), Edge] = {}
    all_vertices = set()
    for line in data:
        edge = Edge(*parse_line(line))
        edges[(edge.from_city, edge.to_city)] = edge
        all_vertices.add(edge.from_city)
        all_vertices.add(edge.to_city)
    return edges, all_vertices


def calculate_cost_of(path, edges):
    cost = 0
    for i in range(len(path) - 1):
        cost += distance(path[i], path[i+1], edges)
    return cost


def permutate(k: int, A: list[str], results):
    if k == 1:
        results.append(A.copy())
        return
    permutate(k - 1, A, results)

    for i in range(0, k - 1):
        if k % 2 == 0:
            A[i], A[k - 1] = A[k - 1], A[i]
        else:
            A[0], A[k - 1] = A[k - 1], A[0]
        permutate(k-1, A, results)

def pick_shortest_path(permutations, edges):
    shortest_path = None
    shortest_distance = math.inf
    for path in permutations:
        distance = calculate_cost_of(path, edges)
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_path = path
    return shortest_path, shortest_distance

def pick_longest_path(permutations, edges):
    longest_path = None
    longest_distance = 0
    for path in permutations:
        distance = calculate_cost_of(path, edges)
        if distance > longest_distance:
            longest_distance = distance
            longest_path = path
    return longest_path, longest_distance


def part_one(filename):
    data = read_puzzle_input(filename)
    edges, all_vertices = build_edges(data)
    permutations = []
    permutate(len(all_vertices), list(all_vertices), permutations)
    shortest_path, shortest_distance = pick_shortest_path(permutations, edges)
    print(shortest_path, shortest_distance)

def part_two(filename):
    data = read_puzzle_input(filename)
    edges, all_vertices = build_edges(data)
    permutations = []
    permutate(len(all_vertices), list(all_vertices), permutations)
    longest_path, longest_distance = pick_longest_path(permutations, edges)
    print(longest_path, longest_distance)


part_two('Day_09_input.txt')
