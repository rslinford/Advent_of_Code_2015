import unittest


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        directions = f.read()
    return directions

def follow_directions(directions):
    x, y = 0, 0
    history = set()
    history.add((0, 0))
    for direction in directions:
        match direction:
            case '^':
                y += 1
            case '>':
                x += 1
            case 'v':
                y -= 1
            case '<':
                x -= 1
        point = (x, y)
        history.add(point)
    return len(history)

def part_one(filename):
    directions = read_puzzle_data(filename)
    return follow_directions(directions)


print('Houses that receive at least one present', part_one('Day_03_input.txt'))

class Test(unittest.TestCase):
    def test_follow_directions(self):
        self.assertEqual(4, follow_directions('^>v<'))
        self.assertEqual(2, follow_directions('<'))
        self.assertEqual(2, follow_directions('^v^v^v^v^v'))