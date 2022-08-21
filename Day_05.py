import unittest


def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def has_at_least_three_vowels(candidate):
    tally = 0
    for c in candidate:
        if c in 'aeiouAEIOU':
            tally += 1
            if tally >= 3:
                return True
    return False


def has_double_letter(candidate):
    for i in range(len(candidate) - 1):
        if candidate[i] == candidate[i + 1]:
            return True
    return False


def is_nice(candidate):
    disallowed = ['ab', 'cd', 'pq', 'xy']
    for d in disallowed:
        if candidate.find(d) != -1:
            return False
    if not has_at_least_three_vowels(candidate):
        return False
    if not has_double_letter(candidate):
        return False
    return True


def part_one(filename):
    data = read_puzzle_data(filename)
    tally = 0
    for s in data:
        if is_nice(s):
            tally += 1
    return tally


print(part_one('Day_05_input.txt'))

class Test(unittest.TestCase):
    def test_is_nice(self):
        self.assertTrue(is_nice('ugknbfddgicrmopn'))
        self.assertTrue(is_nice('aaa'))
        self.assertFalse(is_nice('jchzalrnumimnmhp'))
        self.assertFalse(is_nice('haegwjzuvuyypxyu'))
        self.assertFalse(is_nice('dvszwmarrgswjxmb'))