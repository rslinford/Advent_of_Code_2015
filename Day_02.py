import re
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_dimensions(box_dimensions):
    result = re.search('^(\d+)x(\d+)x(\d+)', box_dimensions)
    length = int(result.group(1))
    width = int(result.group(2))
    height = int(result.group(3))
    return length, width, height


def calculate_area(length, width, height):
    area_a = length * width
    area_b = width * height
    area_c = height * length
    extra = 0
    if area_a <= area_b and area_a <= area_c:
        extra = area_a
    elif area_b <= area_a and area_b <= area_c:
        extra = area_b
    elif area_c <= area_a and area_c <= area_b:
        extra = area_c
    if extra == 0:
        raise ValueError('Should not execute')
    return 2 * (area_a + area_b + area_c) + extra


def part_one(filename):
    data = read_puzzle_input(filename)
    tally = 0
    for box_dimensions in data:
        area = calculate_area(*parse_dimensions(box_dimensions))
        tally += area
    print('Total area', tally)


part_one('Day_02_input.txt')


class Test(unittest.TestCase):
    def test_calculate_area(self):
        self.assertEqual(58, calculate_area(2, 3, 4))
        self.assertEqual(43, calculate_area(1, 1, 10))

    def test_parse_dimensions(self):
        self.assertEqual((2, 3, 4), parse_dimensions('2x3x4'))
        self.assertEqual((1, 1, 10), parse_dimensions('1x1x10'))
