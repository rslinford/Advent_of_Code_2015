import re
import unittest
from abc import abstractmethod
from enum import Enum
from typing import List, Any


class Handedness(Enum):
    LEFT = 1
    RIGHT = 2

class Edge:
    def __init__(self, from_city, to_city, distance):
        self.from_city = from_city
        self.to_city = to_city
        self.distance = distance
        self.right_hand = None
        self.left_hand = None

    def __repr__(self):
        return f'{self.__class__.__name__} from_city({self.from_city}) to_city({self.to_city}) distance({self.distance})'

    def __hash__(self):
        return hash((self.from_city, self.to_city))

    def __eq__(self, other):
        return self.from_city == other.from_city and self.to_city == other.to_city

    def __lt__(self, other):
        return self.from_city < other.from_city

    def set_left(self, node):
        self.left_hand = node

    def set_right(self, node):
        self.right_hand = node


class Node:
    all_instances = {}

    def __init__(self, city_name, handedness: Handedness):
        assert (city_name not in self.all_instances.keys())
        self.city_name = city_name
        self.adjacent_nodes = []
        self.handedness = handedness

    def __repr__(self):
        return f'{self.__class__.__name__} city_name({self.city_name}) ' + \
               f'{self.handedness} adjacent_nodes({[x.city_name for x in self.adjacent_nodes]})'

    @classmethod
    def factory(cls, city_name, handedness: Handedness):
        if city_name in cls.all_instances.keys():
            return cls.all_instances[city_name]
        cls.all_instances[city_name] = Node(city_name, handedness)
        return cls.all_instances[city_name]


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_line(line):
    result = re.search(r'(\w+) to (\w+) = (\d+)', line)
    return result.group(1), result.group(2), int(result.group(3))



def build_edges(data):
    graph = []
    for line in data:
        graph.append(Edge(*parse_line(line)))
    return graph


def create_nodes(edges: List[Edge]):
    for edge in edges:
        left: Node = Node.factory(edge.from_city, Handedness.LEFT)
        right: Node = Node.factory(edge.to_city, Handedness.RIGHT)
        left.adjacent_nodes.append(right)
        right.adjacent_nodes.append(left)


def part_one(filename):
    data = read_puzzle_input(filename)
    edges = build_edges(data)
    create_nodes(edges)
    [print(x) for x in edges]
    print()
    [print(x) for x in Node.all_instances.values()]

# part_one('Day_09_short_input.txt')

class Test(unittest.TestCase):
    def test_node(self):
        data = read_puzzle_input('Day_09_short_input.txt')
        edges = build_edges(data)
        create_nodes(edges)
        dublin: Node = Node.all_instances['Dublin']
        self.assertIsNotNone(dublin)
        self.assertEqual('Dublin', dublin.city_name)
        self.assertEqual(2, len(dublin.adjacent_nodes))
        self.assertEqual('London', dublin.adjacent_nodes[0].city_name)
        self.assertEqual('Belfast', dublin.adjacent_nodes[1].city_name)
        self.assertEqual('Dublin', dublin.adjacent_nodes[0].adjacent_nodes[0].city_name)
        self.assertEqual('Belfast', dublin.adjacent_nodes[0].adjacent_nodes[1].city_name)

