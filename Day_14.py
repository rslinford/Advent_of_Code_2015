import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data



def part_one(filename):
    data = read_puzzle_input(filename)


short = False

if short:
    print('Answer:', part_one('Day_13_short_input.txt'))
else:
    print('Answer:', part_one('Day_13_input_with_me.txt'))


class Test(unittest.TestCase):
    def test_parse_preference(self):
        pass