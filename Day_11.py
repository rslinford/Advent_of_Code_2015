import unittest

def has_increasing_straight_of_at_least_three(password):
    pass


def has_confusing_letters(password):
    pass


def has_non_overlapping_pairs(password):
    pass


def is_valid_password(password):
    if not has_increasing_straight_of_at_least_three(password):
        return False
    if has_confusing_letters(password):
        return False
    if not has_non_overlapping_pairs(password):
        return False
    return True

def part_one():
    old_password = 'vzbxkghb'


part_one()


class Test(unittest.TestCase):
    def test(self):
        self.assertFalse(is_valid_password('hijklmmn'))
        self.assertFalse(is_valid_password('abbceffg'))
        self.assertFalse(is_valid_password('abbcegjk'))
