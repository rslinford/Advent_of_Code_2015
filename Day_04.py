import hashlib


def part_one(secret_key):
    i = 0
    while True:
        i += 1
        combined = f'{secret_key}{i}'
        result = hashlib.md5(combined.encode('utf-8')).hexdigest()
        if result.find('00000') == 0:
            print(f'{combined} hashes to {result}  answer: {i}')
            break

def part_two(secret_key):
    i = 0
    while True:
        i += 1
        combined = f'{secret_key}{i}'
        result = hashlib.md5(combined.encode('utf-8')).hexdigest()
        if result.find('000000') == 0:
            print(f'{combined} hashes to {result}  answer: {i}')
            break


part_two('ckczppom')