def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        directions = f.read()
    return directions


def part_one(filename):
    data = read_puzzle_data(filename)
    print(data)


part_one('Day_03_input.txt')