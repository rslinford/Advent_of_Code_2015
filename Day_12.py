import json
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
    return data


def read_puzzle_input_as_json(filename):
    with open(filename) as f:
        return json.load(f)


def find_numbers(s: str):
    all_numbers = []
    current_number = []
    for c in s:
        if c.isdigit():
            current_number.append(c)
        elif c == '-':
            assert (len(current_number) == 0)
            current_number.append(c)
        else:
            if current_number:
                all_numbers.append(int(''.join(current_number)))
                current_number.clear()
    if current_number:
        all_numbers.append(int(''.join(current_number)))
    return all_numbers


def handle_list(data, rval):
    for x in data:
        if type(x) == int:
            rval.append(x)
        elif type(x) == dict:
            handle_dict(x, rval)
        elif type(x) == list:
            handle_list(x, rval)
        elif type(x) == str:
            pass
        else:
            raise ValueError(f'What to do with type {type(x)}')


def dict_is_red(data):
    for k,v in data.items():
        if v == 'red':
            return True
    return False


def handle_dict(data, rval):
    if dict_is_red(data):
        return
    for k,v in data.items():
        if type(v) == int:
            rval.append(v)
        elif type(v) == dict:
            handle_dict(v, rval)
        elif type(v) == list:
            handle_list(v, rval)
        elif type(v) == str:
            pass
        else:
            raise ValueError(f'What to do with type {type(v)}')


def find_numbers_in_json_element(data, rval):
    if type(data) == list:
        handle_list(data, rval)
    elif type(data) == dict:
        handle_dict(data, rval)
    else:
        raise ValueError(f'What to do with type {type(data)}')


def find_numbers_in_json(json_data):
    rval = []
    find_numbers_in_json_element(json_data, rval)
    return rval


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
    json_data = read_puzzle_input_as_json(filename)
    numbers = find_numbers_in_json(json_data)
    answer = add_numbers(numbers)
    return answer


print(part_two('Day_12_input.txt'))


class Test(unittest.TestCase):
    def test_find_numbers(self):
        self.assertEqual([1, 2, 3], find_numbers('[1,2,3]'))
        self.assertEqual([2, 4], find_numbers('{"a":2,"b":4}'))
        self.assertEqual([-1, 1], find_numbers('{"a":[-1,1]}'))
        self.assertEqual([-1, 1], find_numbers('[-1,{"a":1}]'))
        self.assertEqual([1], find_numbers('"a":1'))

    def test_find_numbers_in_json(self):
        self.assertEqual([1, 2, 3], find_numbers_in_json(json.loads('[1,2,3]')))
        self.assertEqual([1, 3], find_numbers_in_json(json.loads('[1,{"c":"red","b":2},3]')))
        self.assertEqual([1, 5], find_numbers_in_json(json.loads('[1,"red",5]')))

if __name__ == '__main__':
    unittest.main()