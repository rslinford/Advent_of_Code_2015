import re
import unittest
from typing import Dict, Any


class Preference:
    def __init__(self, subject, happiness_units, object):
        self.subject = subject
        self.happiness_units = happiness_units
        self.object = object

    def __repr__(self):
        return f'{self.__class__.__name__} subject({self.subject}) happiness_units({self.happiness_units}) object({self.object})'


class Person:
    all_instances = {}

    def __init__(self, name):
        self.name = name
        self.preferences = {}

    def __repr__(self):
        return f'{self.__class__.__name__} name({self.name} preferences({self.preferences}))'

    @classmethod
    def factory(cls, name: str):
        if name in cls.all_instances.keys():
            return cls.all_instances[name]
        else:
            cls.all_instances[name] = Person(name)
            return cls.all_instances[name]

    def add_preference(self, preference: Preference):
        self.preferences[preference.object] = preference

def calculate_happiness_for_one(subject, left_object, right_object):
    s = Person.factory(subject)
    left_preference = s.preferences[left_object]
    right_preference = s.preferences[right_object]
    happiness = left_preference.happiness_units + right_preference.happiness_units
    return happiness


class Table:
    def __init__(self, keys):
        self.arrangement = list(keys)
        self.arrangement.sort()

    def calculate_happiness(self):
        tally = 0
        for i in range(len(self.arrangement)):
            if i == 0:
                left_hand = self.arrangement[-1]
            else:
                left_hand = self.arrangement[i-1]
            if i == len(self.arrangement) - 1:
                right_hand = self.arrangement[0]
            else:
                right_hand = self.arrangement[i+1]
            tally += calculate_happiness_for_one(self.arrangement[i], left_hand, right_hand)

        return tally

    def render(self):
        return str(self.arrangement)


def parse_preference(text_preference):
    result = re.search('^(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).$', text_preference)
    subject = result.group(1)
    sign = result.group(2)
    happiness_units = int(result.group(3))
    object = result.group(4)
    if sign == 'lose':
        happiness_units = happiness_units * -1
    return Preference(subject, happiness_units, object)


def parse_preferences_into_people(data):
    for preference in data:
        preference = parse_preference(preference)
        person = Person.factory(preference.subject)
        person.add_preference(preference)


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def pretty_print_all_people():
    for x in Person.all_instances.values():
        print(x.name)
        for y in x.preferences.values():
            print('  ', y)


def part_one(filename):
    rval = 0
    data = read_puzzle_input(filename)
    parse_preferences_into_people(data)
    print(Person.all_instances)
    return rval


# print(part_one('Day_13_input.txt'))


class Test(unittest.TestCase):
    def test_parse_preference(self):
        data = read_puzzle_input('Day_13_short_input.txt')
        preference = parse_preference(data[0])
        self.assertEqual('Alice', preference.subject)
        self.assertEqual(54, preference.happiness_units)
        self.assertEqual('Bob', preference.object)
        preference = parse_preference(data[1])
        self.assertEqual('Alice', preference.subject)
        self.assertEqual(-79, preference.happiness_units)
        self.assertEqual('Carol', preference.object)

    def test_parse_preferences_into_people(self):
        data = read_puzzle_input('Day_13_short_input.txt')
        parse_preferences_into_people(data)
        person = Person.all_instances['Carol']
        self.assertEqual('Carol', person.name)
        self.assertEqual(3, len(person.preferences))
        self.assertEqual('Carol', person.preferences['Bob'].subject)
        for k,v in person.preferences.items():
            match k:
                case 'Alice':
                    self.assertEqual(-62, v.happiness_units)
                case 'Bob':
                    self.assertEqual(60, v.happiness_units)
                case 'David':
                    self.assertEqual(55, v.happiness_units)
                case _:
                    raise ValueError

    def test_calculate_happiness_for_one(self):
        data = read_puzzle_input('Day_13_short_input.txt')
        parse_preferences_into_people(data)
        self.assertEqual(-25, calculate_happiness_for_one('Alice', 'Bob', 'Carol'))
        self.assertEqual(76, calculate_happiness_for_one('Bob', 'Alice', 'Carol'))

    def test_calculate_happiness(self):
        data = read_puzzle_input('Day_13_short_input.txt')
        parse_preferences_into_people(data)
        table = Table(Person.all_instances.keys())
        self.assertEqual(330, table.calculate_happiness())
