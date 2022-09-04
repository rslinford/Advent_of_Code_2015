import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n\n')
        replacements = [x.split(' => ') for x in data[0].strip().split('\n')]
        molecule = data[1].strip()
        return replacements, molecule


def replace(replacements, molecule):
    bag_of_molecules = set()
    for replacement in replacements:
        index = 0
        while index != -1:
            index = molecule.find(replacement[0], index)
            if index != -1:
                resulting_molecule = molecule[0:index] + replacement[1] + molecule[index + len(replacement[0]):]
                bag_of_molecules.add(resulting_molecule)
                index += 1
                if index >= len(molecule):
                    break
    return bag_of_molecules


def part_one(filename):
    replacements, molecule = read_puzzle_input(filename)
    bag = replace(replacements, molecule)
    print(f'A bag of {len(bag)} distinct molecules:')
    print(bag)


part_one('Day_19_input.txt')


class Test(unittest.TestCase):
    def test_read_puzzle_input(self):
        replacements, molecule = read_puzzle_input('Day_19_short_input.txt')
        self.assertEqual('HOH', molecule)
        self.assertEqual(['H', 'HO'], replacements[0])
        self.assertEqual(3, len(replacements))

    def test_replace(self):
        replacements, molecule = read_puzzle_input('Day_19_short_input.txt')
        bag = replace(replacements, molecule)
        self.assertEqual({'HHHH', 'HOOH', 'HOHO', 'OHOH'}, bag)
