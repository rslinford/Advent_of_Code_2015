import re
import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    return data


class Ingredient:
    all_instances = {}

    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories
        self.all_instances[name] = self

    def __repr__(self):
        return f'name({self.name}) capacity({self.capacity}) durability({self.durability}) flavor({self.flavor}) texture({self.texture}) calories({self.calories})'


class Cookie:
    def __init__(self):
        self.ingredients: dict[str, int] = {}

    def __repr__(self):
        return f'{self.__class__.__name__} ingredients({self.ingredients})'

    def add_ingredient(self, ingredient, amount):
        self.ingredients[ingredient] = amount

    def clear_ingredients(self):
        self.ingredients.clear()

    def calculate_score(self):
        rval = 0
        ingredient: Ingredient
        temp = {}
        temp['capacity'] = 0
        temp['durability'] = 0
        temp['flavor'] = 0
        temp['texture'] = 0
        for name, amount in self.ingredients.items():
            print(name, amount)
            ingredient = Ingredient.all_instances[name]
            temp['capacity'] += ingredient.capacity * amount
            temp['durability'] += ingredient.durability * amount
            temp['flavor'] += ingredient.flavor * amount
            temp['texture'] += ingredient.texture * amount
        if temp['capacity'] < 0:
            temp['capacity'] = 0
        if temp['durability'] < 0:
            temp['durability'] = 0
        if temp['flavor'] < 0:
            temp['flavor'] = 0
        if temp['texture'] < 0:
            temp['texture'] = 0
        return temp['capacity'] * temp['durability'] * temp['flavor'] * temp['texture']


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
    # for x in ingredients:
    #     print(x)


if short:
    print('Answer:', part_one('Day_15_short_input.txt'))
else:
    print('Answer:', part_one('Day_15_input.txt'))


class Test(unittest.TestCase):
    def test_deserialize_ingredients(self):
        data = read_puzzle_input('Day_15_short_input.txt')
        ingredients = deserialize_ingredients(data)
        self.assertEqual(ingredients[0].name, 'Butterscotch')
        self.assertEqual(ingredients[0].capacity, -1)
        self.assertEqual(ingredients[0].durability, -2)
        self.assertEqual(ingredients[0].flavor, 6)
        self.assertEqual(ingredients[0].texture, 3)
        self.assertEqual(ingredients[0].calories, 8)


class TestCookie(unittest.TestCase):
    def test_add_ingredient(self):
        c = Cookie()
        c.add_ingredient('Butterscotch', 25)
        c.add_ingredient('Cinnamon', 11)
        self.assertEqual(25, c.ingredients['Butterscotch'])
        self.assertEqual(11, c.ingredients['Cinnamon'])

    def test_calculate_score(self):
        data = read_puzzle_input('Day_15_short_input.txt')
        deserialize_ingredients(data)
        c = Cookie()
        c.add_ingredient('Butterscotch', 44)
        c.add_ingredient('Cinnamon', 56)
        self.assertEqual(62842880, c.calculate_score())
