import math
import re
import unittest
from abc import abstractmethod
from enum import Enum
from typing import List, Any, Dict


"""
Let distance of start vertex from start vertex = 0
Let distance of all other vertices from start = (inf)

WHILE vertices remain unvisited
    Visit unvisited vertex with smallest known distance from start vertex (call this the 'current vertex')
    FOR each unvisited neighbour of the current vertex
        Calculate the distance from start vertex
        If the calculated distance of this vertex is less than the known distance
            Update shortest distance to this vertex
            Update the previous vertex with the current vertex
        end if
    NEXT unvisited neighbour
    Add the current vertex to the list of visited vertices
END WHILE
"""

# class Handedness(Enum):
#     LEFT = 1
#     RIGHT = 2

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



class Node:
    all_instances = {}

    def __init__(self, city_name):
        assert (city_name not in self.all_instances.keys())
        self.city_name = city_name
        self.adjacent_nodes = []

    def __repr__(self):
        return f'{self.__class__.__name__} city_name({self.city_name}) ' + \
               f'adjacent_nodes({[x.city_name for x in self.adjacent_nodes]})'

    @classmethod
    def factory(cls, city_name):
        if city_name in cls.all_instances.keys():
            return cls.all_instances[city_name]
        cls.all_instances[city_name] = Node(city_name)
        return cls.all_instances[city_name]


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_line(line):
    result = re.search(r'(\w+) to (\w+) = (\d+)', line)
    return result.group(1), result.group(2), int(result.group(3))



def build_edges(data):
    edges: dict[(str, str), Edge] = {}
    for line in data:
        edge = Edge(*parse_line(line))
        edges[(edge.from_city, edge.to_city)] = edge
        # edges[(edge.to_city, edge.from_city)] = edge
    return edges


def create_nodes(edges: dict[(str, str), Edge]):
    for edge in edges.values():
        left: Node = Node.factory(edge.from_city)
        right: Node = Node.factory(edge.to_city)
        left.adjacent_nodes.append(right)
        right.adjacent_nodes.append(left)


def distance(node_one, node_two, edges: dict[(str, str)]):
    if (node_one.city_name, node_two.city_name) in edges:
        return edges[node_one.city_name, node_two.city_name]
    if (node_two.city_name, node_one.city_name) in edges:
        return edges[node_two.city_name, node_one.city_name]
    raise ValueError(f'Edge for {node_one.city_name}, {node_two.city_name} not found.')



def traverse(node: Node, edges, path: list[str]):
    print(node, path)
    #  Guard against cycles
    if node.city_name in path:
        return
    for adjacent_node in node.adjacent_nodes:
        print(f'Distance between {node.city_name} and {adjacent_node.city_name}:', distance(node, adjacent_node, edges))
        path.append(adjacent_node.city_name)
        traverse(adjacent_node, edges, path)


def initialize_shortest_distances(start_city_name):
    rval = {}
    assert(Node.all_instances[start_city_name])
    for city_name in Node.all_instances.keys():
        if  city_name == start_city_name:
            rval[city_name] = 0
        else:
            rval[city_name] = math.inf
    return rval


def initialize_unvisited_cities():
    return set(Node.all_instances.keys())


def pick_closest_unvisited_vertex(shortest_distances, unvisited_cities):
    closest_city_name = None
    closest_city_distance = math.inf
    for city_name in unvisited_cities:
        if shortest_distances[city_name] < closest_city_distance:
            closest_city_distance = shortest_distances[city_name]
            closest_city_name = city_name
    return closest_city_name


def unvisited_neighbors_of(current_vertex, unvisited_cities):
    node = Node.factory(current_vertex)


def dijkstra(start_city_name, edges):
    shortest_distances = initialize_shortest_distances(start_city_name)
    unvisited_cities = initialize_unvisited_cities()
    while unvisited_cities:
        current_vertex = pick_closest_unvisited_vertex(shortest_distances, unvisited_cities)
        print(current_vertex)
        unvisited_neighbors = unvisited_neighbors_of(current_vertex, unvisited_cities)




def part_one(filename):
    data = read_puzzle_input(filename)
    edges = build_edges(data)
    create_nodes(edges)
    [print(x) for x in edges]
    print()
    [print(x) for x in Node.all_instances.values()]

# part_one('Day_09_short_input.txt')



class Test(unittest.TestCase):
    def setUp(self) -> None:
        data = read_puzzle_input('Day_09_short_input.txt')
        edges = build_edges(data)
        create_nodes(edges)

    def test_node(self):
        # [print(x) for x in edges.values()]
        # print()
        # [print(x) for x in Node.all_instances.values()]

        dublin: Node = Node.all_instances['Dublin']
        self.assertIsNotNone(dublin)
        self.assertEqual('Dublin', dublin.city_name)
        self.assertEqual(2, len(dublin.adjacent_nodes))
        self.assertEqual('London', dublin.adjacent_nodes[0].city_name)
        self.assertEqual('Belfast', dublin.adjacent_nodes[1].city_name)
        self.assertEqual('Dublin', dublin.adjacent_nodes[0].adjacent_nodes[0].city_name)
        self.assertEqual('Belfast', dublin.adjacent_nodes[0].adjacent_nodes[1].city_name)

    def test_traverse(self):
        data = read_puzzle_input('Day_09_short_input.txt')
        edges = build_edges(data)
        traverse(Node.factory('London'), edges, [])
        dijkstra('London', edges)
