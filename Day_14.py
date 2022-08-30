import re
import unittest
from enum import Enum


class State(Enum):
    FLYING = 1
    RESTING = 2


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
        self.distance_traveled = 0
        self.state = State.FLYING
        self.count_down = self.speed_duration
        self.points = 0

    def __repr__(self):
        return f'name({self.name}) speed({self.speed}) speed_duration({self.speed_duration}) rest_duration({self.rest_duration}) ' \
               f'distance_traveled({self.distance_traveled}) state({self.state}) count_down({self.count_down}) points({self.points})'

    def one_second_passing(self):
        self.count_down -= 1
        match self.state:
            case State.FLYING:
                self.distance_traveled += self.speed
                if self.count_down == 0:
                    self.state = State.RESTING
                    self.count_down = self.rest_duration
            case State.RESTING:
                if self.count_down == 0:
                    self.state = State.FLYING
                    self.count_down = self.speed_duration


def deserialize_reindeer(data: list[str]) -> list[Reindeer]:
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


def award_point_to_first_place(reindeer):
    reindeer.sort(key=lambda x: x.distance_traveled, reverse=True)
    winner = reindeer[0]
    for rd in reindeer:
        if rd.distance_traveled == winner.distance_traveled:
            rd.points += 1
        else:
            break


def race(reindeer: list[Reindeer], time_limit):
    for elapsed_seconds in range(1, time_limit + 1):
        for rd in reindeer:
            rd.one_second_passing()
            print(f'After {elapsed_seconds}: {rd}')
        award_point_to_first_place(reindeer)


def determine_winner_part_one(reindeer):
    reindeer.sort(key=lambda x: x.distance_traveled, reverse=True)
    return reindeer[0]


def determine_winner_part_two(reindeer):
    reindeer.sort(key=lambda x: x.points, reverse=True)
    return reindeer[0]


short = False


def part_one(filename):
    data = read_puzzle_input(filename)
    reindeer = deserialize_reindeer(data)
    if short:
        race(reindeer, 1000)
    else:
        race(reindeer, 2503)
    return determine_winner_part_one(reindeer)


def part_two(filename):
    data = read_puzzle_input(filename)
    reindeer = deserialize_reindeer(data)
    if short:
        race(reindeer, 1000)
    else:
        race(reindeer, 2503)
    return determine_winner_part_two(reindeer)


if short:
    print('Answer:', part_two('Day_14_short_input.txt'))
else:
    print('Answer:', part_two('Day_14_input.txt'))


class Test(unittest.TestCase):
    def test_deserialize_reindeer(self):
        data = read_puzzle_input('Day_14_short_input.txt')
        reindeer = deserialize_reindeer(data)
        self.assertEqual('Comet', reindeer[0].name)
        self.assertEqual(14, reindeer[0].speed)
        self.assertEqual(10, reindeer[0].speed_duration)
        self.assertEqual(127, reindeer[0].rest_duration)
