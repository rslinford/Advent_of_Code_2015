def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n\n')
        replacements = data[0].strip().split('\n')
        molecule = data[1].strip()
        return replacements, molecule


def part_one(filename):
    replacements, molecule = read_puzzle_input(filename)
    print(replacements)
    print(molecule)


part_one('Day_19_input.txt')
