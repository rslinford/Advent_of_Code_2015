import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return data



def part_one(filename):
    rval = 0
    data = read_puzzle_input(filename)
    print(data)
    return rval


print(part_one('Day_13_input.txt'))


class Test(unittest.TestCase):
    def test(self):
        pass