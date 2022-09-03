from itertools import combinations


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        containers = [int(x) for x in f.read().strip().split('\n')]
    return containers


def combine(containers):
    tally = 0
    for n in range(1, len(containers)):
        combos = combinations(containers, n)
        for c in combos:
            if sum(c) == 150:
                tally += 1
                print(sum(c), c)
    return tally


def combine_two(containers):
    tally = 0
    combos = combinations(containers, 4)
    for c in combos:
        if sum(c) == 150:
            print(sum(c), c, f'n={4}')
            tally += 1
    return tally


def part_two(filename):
    containers = read_puzzle_input(filename)
    return combine_two(containers)


print('Answer:', part_two('Day_17_input.txt'))


def part_one(filename):
    containers = read_puzzle_input(filename)
    return combine(containers)
# print('Answer:', part_one('Day_17_input.txt'))
