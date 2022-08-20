import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data

def find_depth(data):
    depth = 0
    for c in data:
        match c:
            case '(':
                depth += 1
            case ')':
                depth -= 1
    return depth


def part_one(filename):
    data = read_puzzle_input(filename)
    print('Depth', find_depth(data))


part_one('Day_01_input.txt')

class Test(unittest.TestCase):
    def test_find_depth(self):
        self.assertEqual(0, find_depth('(())'))
        self.assertEqual(0, find_depth('()()'))
        self.assertEqual(3, find_depth('((('))
        self.assertEqual(3, find_depth('(()(()('))
        self.assertEqual(-1, find_depth('())'))
        self.assertEqual(-3, find_depth(')())())'))
