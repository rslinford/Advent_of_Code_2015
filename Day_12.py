import json
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return data


def read_puzzle_input_as_json(filename):
    return json.load(filename)


def find_numbers(s: str):
    all_numbers = []
    current_number = []
    for c in s:
        if c.isdigit():
            current_number.append(c)
        elif c == '-':
            assert(len(current_number) == 0)
            current_number.append(c)
        else:
            if current_number:
                all_numbers.append(int(''.join(current_number)))
                current_number.clear()
    if current_number:
        all_numbers.append(int(''.join(current_number)))
    return all_numbers


def find_numbers_in_json(data):
    pass


def add_numbers(numbers):
    tally = 0
    for n in numbers:
        tally += n
    return tally

def part_one(filename):
    rval = 0
    data = read_puzzle_input(filename)
    numbers = find_numbers(data)
    answer = add_numbers(numbers)
    return answer



def part_two(filename):
    rval = 0
    data = read_puzzle_input_as_json(filename)
    numbers = find_numbers_in_json(data)
    answer = add_numbers(numbers)
    return answer


def part_two(param):
    pass


print(part_two('Day_12_input.txt'))


class Test(unittest.TestCase):
    def test_find_numbers(self):
        self.assertEqual([1, 2, 3], find_numbers('[1,2,3]'))
        self.assertEqual([2, 4], find_numbers('{"a":2,"b":4}'))
        self.assertEqual([-1, 1], find_numbers('{"a":[-1,1]}'))
        self.assertEqual([-1, 1], find_numbers('[-1,{"a":1}]'))
        self.assertEqual([1], find_numbers('"a":1'))