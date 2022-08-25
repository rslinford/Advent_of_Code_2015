def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data

def count_literal_chars(data):
    tally = 0
    for x in data:
        tally += len(x)
    return tally

def count_in_memory_bytes(data):
    tally = 0
    escaped = False
    hex_mode = False
    hex_count = 0
    for x in data:
        for c in x:
            if hex_mode:
                hex_count += 1
                if hex_count == 2:
                    hex_mode = False
                    escaped = False
                    hex_count = 0
                continue
            match c:
                case '"':
                    if escaped:
                        tally += 1
                        escaped = False
                case '\\':
                    if escaped:
                        tally += 1
                        escaped = False
                    else:
                        escaped = True
                case 'x':
                    if escaped:
                        hex_mode = True
                    else:
                        tally += 1
    return tally


def part_one(filename):
    data = read_puzzle_input(filename)
    for x in data:
        print(x)
    print('Literal char count', count_literal_chars(data))
    print('In memory char count', count_in_memory_bytes(data))


part_one('Day_08_short_input.txt')
