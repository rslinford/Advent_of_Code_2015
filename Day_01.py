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

def find_basement(data):
    depth = 0
    for i, c in enumerate(data):
        match c:
            case '(':
                depth += 1
            case ')':
                depth -= 1
        if depth < 0:
            return i + 1
    return depth


def part_one(filename):
    data = read_puzzle_input(filename)
    print('Depth', find_depth(data))

def part_two(filename):
    data = read_puzzle_input(filename)
    print('Enters basement at position', find_basement(data))


part_two('Day_01_input.txt')

class Test(unittest.TestCase):
    def test_find_depth(self):
        self.assertEqual(0, find_depth('(())'))
        self.assertEqual(0, find_depth('()()'))
        self.assertEqual(3, find_depth('((('))
        self.assertEqual(3, find_depth('(()(()('))
        self.assertEqual(-1, find_depth('())'))
        self.assertEqual(-3, find_depth(')())())'))

    def test_find_basement(self):
        self.assertEqual(1, find_basement(')'))
        self.assertEqual(5, find_basement('()()))'))