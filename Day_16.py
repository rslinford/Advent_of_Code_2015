import re
import unittest


class Sue:
    def __init__(self, id):
        self.id = id
        self.attr = {'children': 0, 'cats': 0, 'samoyeds': 0, 'pomeranians': 0, 'akitas': 0, 'vizslas': 0,
                     'goldfish': 0, 'trees': 0, 'perfumes': 0, 'cars': 0}

    def render(self):
        pass

    def set_attribute(self, attr_name, amount):
        if attr_name not in self.attr.keys():
            raise ValueError(f'"{attr_name}" is unknown.')
        self.attr[attr_name] = amount


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
        rval = []
        for line in data:
            result = re.search(r'^Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)$', line)
            id = int(result.group(1))
            attr_name1 = result.group(2)
            attr_amount1 = int(result.group(3))
            attr_name2 = result.group(4)
            attr_amount2 = int(result.group(5))
            attr_name3 = result.group(6)
            attr_amount3 = int(result.group(7))
            aunt = Sue(id)
            aunt.set_attribute(attr_name1, attr_amount1)
            aunt.set_attribute(attr_name2, attr_amount2)
            aunt.set_attribute(attr_name3, attr_amount3)
            rval.append(aunt)
    return rval


short = False


def part_one(filename):
    data = read_puzzle_input(filename)
    print(data)


if short:
    print('Answer:', part_one('Day_15_short_input.txt'))
else:
    print('Answer:', part_one('Day_16_input.txt'))


class Test(unittest.TestCase):
    def test_name(self):
        pass
