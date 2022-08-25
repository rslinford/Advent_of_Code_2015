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
                    tally += 1
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
                case _:
                    tally += 1
    return tally


def encode(data):
    rval = []
    for x in data:
        row = []
        row.append('"')
        for c in x:
            match c:
                case '\"':
                    row.append('\\"')
                case '\\':
                    row.append('\\\\')
                case _:
                    row.append(c)
        row.append('"')
        rval.append(''.join(row))

    return rval


def part_one(filename):
    data = read_puzzle_input(filename)
    for x in data:
        print(x)
    literal_count = count_literal_chars(data)
    in_memory_count = count_in_memory_bytes(data)
    print('Literal char count', literal_count)
    print('In memory char count', in_memory_count)
    print("Difference:", literal_count - in_memory_count)


def part_two(filename):
    data = read_puzzle_input(filename)
    original_count = count_literal_chars(data)
    encoded_data = encode(data)
    encoded_count = count_literal_chars(encoded_data)
    for x in encoded_data:
        print(x)
    print('Original char count', original_count)
    print('Char count after encoding', encoded_count)
    print("Difference:", encoded_count - original_count)


part_two('Day_08_input.txt')
