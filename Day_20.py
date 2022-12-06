import unittest

short_input = 150
long_input = 29000000


def add_up_divisors(n: int):
    tally = 0
    for i in range(1, n + 1):
        if n % i == 0:
            tally += i
    return tally


def part_one(puzzle_input):
    house = 0
    while True:
        house += 1
        presents = add_up_divisors(house) * 10
        print(house, presents)
        if presents >= puzzle_input:
            break

    return house


def part_two(puzzle_input):
    return -1


print(f'Answer part one: {part_one(short_input)}')
print(f'Answer part two: {part_two(short_input)}')


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(8, part_one(short_input))

    def test_part_two(self):
        self.assertEqual(-1, part_two())

    def test_add_up_divisor(self):
        self.assertEqual(1, add_up_divisors(1))
        self.assertEqual(3, add_up_divisors(2))
        self.assertEqual(4, add_up_divisors(3))
        self.assertEqual(7, add_up_divisors(4))
        self.assertEqual(6, add_up_divisors(5))
        self.assertEqual(12, add_up_divisors(6))
        self.assertEqual(8, add_up_divisors(7))
        self.assertEqual(15, add_up_divisors(8))
        self.assertEqual(13, add_up_divisors(9))
