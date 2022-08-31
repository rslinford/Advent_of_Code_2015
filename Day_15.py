import re
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def __repr__(self):
        return f'name({self.name}) capacity({self.capacity}) durability({self.durability}) flavor({self.flavor}) texture({self.texture}) calories({self.calories})'


def deserialize_ingredients(data: list[str]) -> list[Ingredient]:
    ingredients = []
    for line in data:
        result = re.search(
            r'^(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)$',
            line)
        name = result.group(1)
        capacity = int(result.group(2))
        durability = int(result.group(3))
        flavor = int(result.group(4))
        texture = int(result.group(5))
        calories = int(result.group(6))
        ingredients.append(Ingredient(name, capacity, durability, flavor, texture, calories))
    return ingredients


short = True


def part_one(filename):
    data = read_puzzle_input(filename)
    ingredients = deserialize_ingredients(data)
    for x in ingredients:
        print(x)


if short:
    print('Answer:', part_one('Day_15_short_input.txt'))
else:
    print('Answer:', part_one('Day_15_input.txt'))


class Test(unittest.TestCase):
    def test_deserialize_ingredients(self):
        data = read_puzzle_input('Day_15_short_input.txt')
        ingredients = deserialize_ingredients(data)
