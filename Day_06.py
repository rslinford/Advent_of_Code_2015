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
        for y in range(self.grid.shape[0]-1, -1, -1):
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

class LightGridMarkTwo:
    grid: np.array

    def __init__(self, width, height):
        self.grid = np.zeros((height, width), dtype=np.uint)
    def __repr__(self):
        rval = []
        for y in range(self.grid.shape[0]-1, -1, -1):
            for x in range(self.grid.shape[1]):
                if x > 0:
                    rval.append(', ')
                rval.append(str(self.grid[y][x]))
            if y > 0:
                rval.append('\n')
        return ''.join(rval)

    def turn_on(self, x_index, y_index):
        self.grid[y_index][x_index] += 1

    def turn_off(self, x_index, y_index):
        if self.grid[y_index][x_index] > 0:
            self.grid[y_index][x_index] -= 1

    def toggle(self, x_index, y_index):
        self.grid[y_index][x_index] += 2

    def tally_lit(self):
        tally = 0
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
               tally += self.grid[y][x]
        return tally


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

def process_command_mark_two(grid: LightGridMarkTwo, command, x, y):
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
    return grid.tally_lit()

def light_show_mark_two(command_input):
    grid = LightGridMarkTwo(1000, 1000)
    for command in command_input:
        parsed_command = parse_line(command)
        process_command_mark_two(grid, *parsed_command)
    return grid.tally_lit()

def part_one(filename):
    command_input = read_puzzle_input(filename)
    return light_show(command_input)

def part_two(filename):
    command_input = read_puzzle_input(filename)
    return light_show_mark_two(command_input)

print('Lights lit:', part_two('Day_06_input.txt'))


class Test(unittest.TestCase):
    def test_parse_line(self):
        self.assertEqual(('turn on', [887, 959], [9, 629]), parse_line('turn on 887,9 through 959,629'))
        self.assertEqual(('toggle', [720, 897], [196, 994]), parse_line('toggle 720,196 through 897,994'))

class TestLightGridMarkTwo(unittest.TestCase):
    def test_light_grid_mark_two(self):
        grid = LightGridMarkTwo(4, 4)
        self.assertEqual("0, 0, 0, 0\n"
                         "0, 0, 0, 0\n"
                         "0, 0, 0, 0\n"
                         "0, 0, 0, 0", str(grid))
        self.assertEqual(0, grid.tally_lit())
        process_command_mark_two(grid, *parse_line('turn on 0,0 through 3,3'))
        self.assertEqual("1, 1, 1, 1\n"
                         "1, 1, 1, 1\n"
                         "1, 1, 1, 1\n"
                         "1, 1, 1, 1", str(grid))
        self.assertEqual(16, grid.tally_lit())
        process_command_mark_two(grid, *parse_line('turn off 0,0 through 3,3'))
        self.assertEqual("0, 0, 0, 0\n"
                         "0, 0, 0, 0\n"
                         "0, 0, 0, 0\n"
                         "0, 0, 0, 0", str(grid))
        self.assertEqual(0, grid.tally_lit())
        process_command_mark_two(grid, *parse_line('toggle 0,0 through 3,3'))
        self.assertEqual("2, 2, 2, 2\n"
                         "2, 2, 2, 2\n"
                         "2, 2, 2, 2\n"
                         "2, 2, 2, 2", str(grid))
        self.assertEqual(32, grid.tally_lit())
        process_command_mark_two(grid, *parse_line('turn off 0,0 through 3,3'))
        process_command_mark_two(grid, *parse_line('turn off 0,0 through 3,3'))
        process_command_mark_two(grid, *parse_line('turn off 0,0 through 3,3'))
        self.assertEqual("0, 0, 0, 0\n"
                         "0, 0, 0, 0\n"
                         "0, 0, 0, 0\n"
                         "0, 0, 0, 0", str(grid))
        self.assertEqual(0, grid.tally_lit())


class TestLightGrid(unittest.TestCase):
    def test_light_grid(self):
        grid = LightGrid(10, 10)
        self.assertEqual("..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........", str(grid))
        self.assertEqual(0, grid.tally_lit())
        process_command(grid, *parse_line('turn on 0,0 through 9,9'))
        self.assertEqual("##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########", str(grid))
        self.assertEqual(100, grid.tally_lit())
        process_command(grid, *parse_line('turn off 0,0 through 9,9'))
        self.assertEqual("..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........", str(grid))
        self.assertEqual(0, grid.tally_lit())
        process_command(grid, *parse_line('turn on 0,0 through 0,0'))
        self.assertEqual("..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "#.........", str(grid))
        self.assertEqual(1, grid.tally_lit())
        process_command(grid, *parse_line('turn on 9,0 through 9,0'))
        self.assertEqual("..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "#........#", str(grid))
        self.assertEqual(2, grid.tally_lit())
        process_command(grid, *parse_line('turn on 0,9 through 0,9'))
        self.assertEqual("#.........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "#........#", str(grid))
        self.assertEqual(3, grid.tally_lit())
        process_command(grid, *parse_line('turn on 9,9 through 9,9'))
        self.assertEqual("#........#\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "..........\n"
                         "#........#", str(grid))
        self.assertEqual(4, grid.tally_lit())
        process_command(grid, *parse_line('toggle 0,0 through 9,9'))
        self.assertEqual(".########.\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         "##########\n"
                         ".########.", str(grid))
        self.assertEqual(96, grid.tally_lit())

