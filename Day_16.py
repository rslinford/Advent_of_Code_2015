import re
import unittest


class Sue:
    def __init__(self, id):
        self.id = id
        self.attr = {}

    def render(self):
        rval = []
        rval.append(self.__class__.__name__)
        rval.append(f' id ({self.id})')
        for k, v in self.attr.items():
            rval.append(f' {k}: {v}')
        return ''.join(rval)

    def __repr__(self):
        return self.render()

    def set_attribute(self, attr_name, amount):
        self.attr[attr_name] = amount

    def is_match(self, target_attrs):
        for k, v in target_attrs.items():
            if k not in self.attr.keys():
                continue
            if target_attrs[k] != self.attr[k]:
                return False
        return True

    def is_match_two(self, target_attrs):
        for k, v in target_attrs.items():
            if k not in self.attr.keys():
                continue
            if k in {'cats', 'trees'}:
                if target_attrs[k] >= self.attr[k]:
                    return False
            elif k in {'pomeranians', 'goldfish'}:
                if target_attrs[k] <= self.attr[k]:
                    return False
            elif target_attrs[k] != self.attr[k]:
                return False
        return True


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


target_attrs = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}


def part_one(filename):
    sues = read_puzzle_input(filename)
    the_sue = None
    for sue in sues:
        if sue.is_match(target_attrs):
            the_sue = sue
            print('Match!: ', sue)
    return the_sue


def part_two(filename):
    sues = read_puzzle_input(filename)
    the_sue = None
    for sue in sues:
        if sue.is_match_two(target_attrs):
            the_sue = sue
            print('Match!: ', sue)
    return the_sue


print('Answer:', part_two('Day_16_input.txt'))


class Test(unittest.TestCase):
    def test_sue(self):
        sues = read_puzzle_input('Day_16_input.txt')
        self.assertEqual(1, sues[0].id)
        self.assertEqual(6, sues[0].attr['goldfish'])
        self.assertEqual(9, sues[0].attr['trees'])
        self.assertEqual(0, sues[0].attr['akitas'])
        self.assertEqual(3, sues[2].id)
        self.assertEqual(10, sues[2].attr['cars'])
        self.assertEqual(6, sues[2].attr['akitas'])
        self.assertEqual(7, sues[2].attr['perfumes'])
