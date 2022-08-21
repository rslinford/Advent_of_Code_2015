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

def follow_directions_two(directions):
    x = [0, 0]
    y = [0, 0]
    history = set()
    history.add((0, 0))
    for i, direction in enumerate(directions):
        index = i % 2
        match direction:
            case '^':
                y[index] += 1
            case '>':
                x[index] += 1
            case 'v':
                y[index] -= 1
            case '<':
                x[index] -= 1
        point = (x[index], y[index])
        history.add(point)
    return len(history)

def part_one(filename):
    directions = read_puzzle_data(filename)
    return follow_directions(directions)

def part_two(filename):
    directions = read_puzzle_data(filename)
    return follow_directions_two(directions)


print('Houses that receive at least one present:', part_two('Day_03_input.txt'))

class Test(unittest.TestCase):
    def test_follow_directions_two(self):
        self.assertEqual(3, follow_directions_two('^>v<'))
        self.assertEqual(3, follow_directions_two('^v'))
        self.assertEqual(11, follow_directions_two('^v^v^v^v^v'))


    def test_follow_directions(self):
        self.assertEqual(4, follow_directions('^>v<'))
        self.assertEqual(2, follow_directions('<'))
        self.assertEqual(2, follow_directions('^v^v^v^v^v'))