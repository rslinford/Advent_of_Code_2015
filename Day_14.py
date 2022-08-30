import re
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


class Reindeer:
    def __init__(self, name, speed, speed_duration, rest_duration):
        self.name = name
        self.speed = speed
        self.speed_duration = speed_duration
        self.rest_duration = rest_duration

    def __repr__(self):
        return f'name({self.name}) speed({self.speed}) speed_duration({self.speed_duration}) rest_duration({self.rest_duration})'


def deserialize_reindeer(data):
    reindeer = []
    for line in data:
        result = re.search(r'^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.$',
                           line)
        name = result.group(1)
        speed = int(result.group(2))
        speed_duration = int(result.group(3))
        rest_duration = int(result.group(4))
        reindeer.append(Reindeer(name, speed, speed_duration, rest_duration))
    return reindeer


def part_one(filename):
    data = read_puzzle_input(filename)
    reindeer = deserialize_reindeer(data)
    for x in reindeer:
        print(x)


short = True

if short:
    print('Answer:', part_one('Day_14_short_input.txt'))
else:
    print('Answer:', part_one('Day_14_input.txt'))


class Test(unittest.TestCase):
    def test_parse_preference(self):
        pass
