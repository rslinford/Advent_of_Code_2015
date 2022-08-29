import unittest

def has_increasing_straight_of_at_least_three(password):
    prev_c = ''
    consecutive = 1
    for c in password:
        if prev_c:
            if ord(prev_c) + 1 == ord(c):
                consecutive += 1
                if consecutive >= 3:
                    return True
            else:
                consecutive = 1
        prev_c = c
    return False



def has_confusing_letters(password):
    for c in password:
        match c:
            case 'i' | 'o' | 'l':
                return True
    return False


def has_non_overlapping_pairs(password):
    prev_c = ''
    pair_tally = 0
    for c in password:
        if prev_c:
            if c == prev_c:
                pair_tally += 1
                if pair_tally >= 2:
                    return True
                c = ''
        prev_c = c
    return False


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
    def test_is_valid_password(self):
        self.assertFalse(is_valid_password('hijklmmn'))
        self.assertFalse(is_valid_password('abbceffg'))
        self.assertFalse(is_valid_password('abbcegjk'))
        self.assertTrue(is_valid_password('aabbpqr'))

    def test_has_increasing_straight_of_at_least_three(self):
        self.assertFalse(has_increasing_straight_of_at_least_three('124679'))
        self.assertTrue(has_increasing_straight_of_at_least_three('1245679'))
        self.assertTrue(has_increasing_straight_of_at_least_three('abc'))
        self.assertTrue(has_increasing_straight_of_at_least_three('aaaaxyz'))

    def test_has_confusing_letters(self):
        self.assertFalse(has_confusing_letters('abcdefg'))
        self.assertTrue(has_confusing_letters('abicdoefgl'))
        self.assertTrue(has_confusing_letters('aaaaaaai'))
        self.assertTrue(has_confusing_letters('oaaaaaaa'))
        self.assertTrue(has_confusing_letters('aaalaaaa'))

    def test_has_non_overlapping_pairs(self):
        self.assertFalse(has_non_overlapping_pairs('123456'))
        self.assertFalse(has_non_overlapping_pairs('12aaa6'))
        self.assertTrue(has_non_overlapping_pairs('12aaaa6'))
        self.assertTrue(has_non_overlapping_pairs('aacc'))