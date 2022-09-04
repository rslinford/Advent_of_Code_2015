import unittest

import numpy as np


class LightGrid:
    grid: np.chararray

    def __init__(self, dim, initial_state=None):
        self.grid = np.chararray((dim, dim))
        self.grid[:] = '.'
        if initial_state:
            for y in range(dim):
                for x in range(dim):
                    self.grid[y][x] = initial_state[y][x]

    def __repr__(self):
        rval = []
        for y in range(self.grid.shape[0]):
            if y > 0:
                rval.append('\n')
            for x in range(self.grid.shape[1]):
                match self.grid[y][x]:
                    case b'.':
                        rval.append('.')
                    case b'#':
                        rval.append('#')
                    case _:
                        raise ValueError
        return ''.join(rval)

    def turn_on(self, x_index, y_index):
        self.grid[y_index][x_index] = '#'

    def turn_off(self, x_index, y_index):
        self.grid[y_index][x_index] = '.'

    def is_on(self, x_index, y_index):
        return self.grid[y_index][x_index] == b'#'

    def toggle(self, x_index, y_index):
        match self.grid[y_index][x_index]:
            case b'.':
                self.grid[y_index][x_index] = '#'
            case b'#':
                self.grid[y_index][x_index] = '.'
            case _:
                raise ValueError

    def tally_lit(self):
        tally = 0
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                if self.grid[y][x] == b'#':
                    tally += 1
        return tally

    def count_lit_neighbors(self, x_index, y_index):
        tally = 0
        if y_index > 0:
            if self.is_on(x_index, y_index - 1):
                tally += 1
        if y_index < self.grid.shape[0] - 1:
            if self.is_on(x_index, y_index + 1):
                tally += 1
        if x_index > 0 and y_index > 0:
            if self.is_on(x_index - 1, y_index - 1):
                tally += 1
        if x_index > 0:
            if self.is_on(x_index - 1, y_index):
                tally += 1
        if x_index > 0 and y_index < self.grid.shape[0] - 1:
            if self.is_on(x_index - 1, y_index + 1):
                tally += 1
        if x_index < self.grid.shape[1] - 1 and y_index > 0:
            if self.is_on(x_index + 1, y_index - 1):
                tally += 1
        if x_index < self.grid.shape[1] - 1:
            if self.is_on(x_index + 1, y_index):
                tally += 1
        if x_index < self.grid.shape[1] - 1 and y_index < self.grid.shape[0] - 1:
            if self.is_on(x_index + 1, y_index + 1):
                tally += 1
        return tally

    def one_day(self):
        next_lg = LightGrid(self.grid.shape[0])
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                count = self.count_lit_neighbors(x, y)
                if (self.is_on(x, y)):
                    if count == 2 or count == 3:
                        next_lg.turn_on(x, y)
                    else:
                        next_lg.turn_off(x, y)
                else:
                    if count == 3:
                        next_lg.turn_on(x, y)
                    else:
                        next_lg.turn_off(x, y)

        self.grid = next_lg.grid


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def part_one(filename):
    data = read_puzzle_input(filename)
    lg = LightGrid(len(data), data)
    print(f'Initial state\n{lg}')
    for i in range(1, 101):
        lg.one_day()
        print(f'\nDay {i} lit({lg.tally_lit()})\n{lg}')


part_one('Day_18_input.txt')


class Test(unittest.TestCase):
    def test_count_lit_neighbors(self):
        data = read_puzzle_input('Day_18_short_input.txt')
        lg = LightGrid(len(data), data)
        self.assertEqual(1, lg.count_lit_neighbors(0, 0))
        self.assertEqual(0, lg.count_lit_neighbors(1, 0))
        self.assertEqual(4, lg.count_lit_neighbors(4, 0))
        self.assertEqual(1, lg.count_lit_neighbors(5, 0))
        self.assertEqual(2, lg.count_lit_neighbors(0, 5))
        self.assertEqual(1, lg.count_lit_neighbors(5, 5))
        self.assertEqual(6, lg.count_lit_neighbors(1, 4))
        self.assertEqual(4, lg.count_lit_neighbors(1, 3))

    def test_is_on(self):
        data = read_puzzle_input('Day_18_short_input.txt')
        lg = LightGrid(len(data), data)
        self.assertFalse(lg.is_on(0, 0))
        self.assertTrue(lg.is_on(1, 0))
        self.assertFalse(lg.is_on(5, 5))
        self.assertTrue(lg.is_on(0, 5))

    def test_one_day(self):
        data = read_puzzle_input('Day_18_short_input_2.txt')
        lg = LightGrid(len(data), data)
        lg.one_day()
        self.assertEqual(".#.\n"
                         ".#.\n"
                         "...", str(lg))
