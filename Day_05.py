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


def is_nice_one(candidate):
    disallowed = ['ab', 'cd', 'pq', 'xy']
    for d in disallowed:
        if candidate.find(d) != -1:
            return False
    if not has_at_least_three_vowels(candidate):
        return False
    if not has_double_letter(candidate):
        return False
    return True


def has_two_pair(candidate):
    for i in range(len(candidate) - 1):
        for j in range(i+2, len(candidate) - 1):
            if candidate[i] == candidate[j] and candidate[i+1] == candidate[j+1]:
                return True
    return False


def has_repeat_with_one_letter_between(candidate):
    for i in range(len(candidate) - 2):
        if candidate[i] == candidate[i+2]:
            return True
    return False


def is_nice_two(candidate):
    if not has_two_pair(candidate):
        return False
    if not has_repeat_with_one_letter_between(candidate):
        return False

    return True

def part_one(filename):
    data = read_puzzle_data(filename)
    tally = 0
    for s in data:
        if is_nice_one(s):
            tally += 1
    return tally


def part_two(filename):
    data = read_puzzle_data(filename)
    tally = 0
    for s in data:
        if is_nice_two(s):
            tally += 1
    return tally

print(part_two('Day_05_input.txt'))

class Test(unittest.TestCase):
    def test_is_nice_one(self):
        self.assertTrue(is_nice_one('ugknbfddgicrmopn'))
        self.assertTrue(is_nice_one('aaa'))
        self.assertFalse(is_nice_one('jchzalrnumimnmhp'))
        self.assertFalse(is_nice_one('haegwjzuvuyypxyu'))
        self.assertFalse(is_nice_one('dvszwmarrgswjxmb'))

    def test_has_two_pair(self):
        self.assertTrue(has_two_pair('qjhvhtzxzqqjkmpb'))
        self.assertTrue(has_two_pair('xxyxx'))
        self.assertTrue(has_two_pair('uurcxstgmygtbstg'))
        self.assertFalse(has_two_pair('ieodomkazucvgmuy'))
        self.assertFalse(has_two_pair('abcdefghijk'))

    def test_has_repeat_with_one_letter_between(self):
        self.assertTrue(has_repeat_with_one_letter_between('qjhvhtzxzqqjkmpb'))
        self.assertTrue(has_repeat_with_one_letter_between('xxyxx'))
        self.assertFalse(has_repeat_with_one_letter_between('uurcxstgmygtbstg'))
        self.assertTrue(has_repeat_with_one_letter_between('ieodomkazucvgmuy'))
        self.assertFalse(has_repeat_with_one_letter_between('abcdefghijk'))
