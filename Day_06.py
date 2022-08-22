import re
import unittest
import numpy as np


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


class LightGrid:
    grid: np.chararray

    def __init__(self, width, height):
        self.grid = np.chararray((height, width))
        self.grid[:] = '.'
    def __repr__(self):
        rval = []
        for y in range(self.grid.shape[0]-1, 0, -1):
            for x in range(self.grid.shape[1]):
                match self.grid[y][x]:
                    case b'.':
                        rval.append('.')
                    case b'#':
                        rval.append('#')
                    case _:
                        raise ValueError
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


def parse_line(command_text):
    x = [0, 0]
    y = [0, 0]
    result = re.search(r'^([^\d]+)(\d+),(\d+) through (\d+),(\d+)$', command_text)
    command = result.group(1).strip()
    x[0] = int(result.group(2))
    y[0] = int(result.group(3))
    x[1] = int(result.group(4))
    y[1] = int(result.group(5))
    return command, x, y


def process_command(grid: LightGrid, command, x, y):
    if x[0] > x[1]:
        x[0], x[1] = x[1], x[0]
    if y[0] > y[1]:
        y[0], y[1] = y[1], y[0]
    for y_index in range(y[0], y[1] + 1):
        for x_index in range(x[0], x[1] + 1):
            match command:
                case 'turn on':
                    grid.turn_on(x_index, y_index)
                case 'turn off':
                    grid.turn_off(x_index, y_index)
                case 'toggle':
                    grid.toggle(x_index, y_index)

def light_show(command_input):
    grid = LightGrid(1000, 1000)
    for command in command_input:
        parsed_command = parse_line(command)
        process_command(grid, *parsed_command)
        print(grid)

def part_one(filename):
    command_input = read_puzzle_input(filename)
    light_show(command_input)

part_one('Day_06_input.txt')

class Test(unittest.TestCase):
    def test_parse_line(self):
        self.assertEqual(('turn on', [887, 959], [9, 629]), parse_line('turn on 887,9 through 959,629'))
        self.assertEqual(('toggle', [720, 897], [196, 994]), parse_line('toggle 720,196 through 897,994'))

class TestLightGrid(unittest.TestCase):
    command_input = read_puzzle_input('Day_06_short_input.txt')
    light_show(command_input)
