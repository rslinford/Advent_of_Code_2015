import re
from abc import abstractmethod


class Edge:
    def __init__(self, from_city, to_city, distance):
        self.from_city = from_city
        self.to_city = to_city
        self.distance = distance
        self.right_hand = None
        self.left_hand = None

    def __repr__(self):
        return f'{self.__class__.__name__} from_city({self.from_city}) to_city({self.to_city}) distance({self.distance})'

    def set_left(self, node):
        self.left_hand = node

    def set_right(self, node):
        self.right_hand = node


class Node:
    all_instances = {}

    def __init__(self, city_name):
        assert (city_name not in self.all_instances.keys())
        self.city_name = city_name
        self.adjacent_nodes = set()

    @classmethod
    def factory(cls, city_name):
        if city_name in cls.all_instances.keys():
            return cls.all_instances[city_name]
        cls.all_instances[city_name] = Node(city_name)
        return cls.all_instances[city_name]

    def connect(self, edge: Edge):
        self.adjacent_nodes.add(edge)


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_line(line):
    result = re.search(r'(\w+) to (\w+) = (\d+)', line)
    return result.group(1), result.group(2), int(result.group(3))


def connect(edge, from_city, to_city):
    from_city.connect(edge)
    to_city.connect(edge)
    edge.set_left(from_city)
    edge.set_right(to_city)


def build_graph(data):
    for line in data:
        edge = Edge(*parse_line(line))
        from_city = Node.factory(edge.from_city)
        to_city = Node.factory(edge.to_city)
        connect(edge, from_city, to_city)


def part_one(filename):
    data = read_puzzle_input(filename)
    build_graph(data)


part_one('Day_09_short_input.txt')
