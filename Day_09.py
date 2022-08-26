import re

class Edge:
    def __init__(self, from_city, to_city, distance):
        self.from_city = from_city
        self.to_city = to_city
        self.distance = distance

    def __repr__(self):
        return f'{self.__class__.__name__} from_city({self.from_city}) to_city({self.to_city}) distance({self.distance})'

def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_line(line):
    result = re.search(r'(\w+) to (\w+) = (\d+)', line)
    return result.group(1), result.group(2), int(result.group(3))


def build_graph(data):
    for line in data:
        edge = Edge(*parse_line(line))
        print(edge)

def part_one(filename):
    data = read_puzzle_input(filename)
    build_graph(data)

part_one('Day_09_short_input.txt')
