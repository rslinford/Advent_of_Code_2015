def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def part_one(filename):
    data = read_puzzle_data(filename)


part_one('Day_05_input.txt')
