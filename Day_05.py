def read_puzzle_data(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def has_at_least_three_vowels(candidate):
    pass


def has_double_letter(candidate):
    pass


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
