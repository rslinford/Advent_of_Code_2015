import numpy as np


class LightGrid:
    grid: np.chararray

    def __init__(self, width, height, initial_state):
        self.grid = np.chararray(initial_state)
        for y in range(height):
            for x in range(width):
                self.grid[y][x] = initial_state[y][x]

    def __repr__(self):
        rval = []
        for y in range(self.grid.shape[0] - 1, -1, -1):
            for x in range(self.grid.shape[1]):
                match self.grid[y][x]:
                    case b'.':
                        rval.append('.')
                    case b'#':
                        rval.append('#')
                    case _:
                        raise ValueError
            if y > 0:
                rval.append('\n')
        return ''.join(rval)

    def turn_on(self, x_index, y_index):
        self.grid[y_index][x_index] = '#'

    def turn_off(self, x_index, y_index):
        self.grid[y_index][x_index] = '.'

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


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def part_one(filename):
    data = read_puzzle_input(filename)
    print(data)
    lg = LightGrid(100, 100, data)
    print(lg)


part_one('Day_18_input.txt')
