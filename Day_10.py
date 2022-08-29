import unittest


def look_and_say(s):
    result = []
    consecutive = 1
    prev_c = ''
    for c in s:
        if c == prev_c:
            consecutive += 1
        else:
            if prev_c:
                result.append(str(consecutive))
                result.append(str(prev_c))
            consecutive = 1
            prev_c = c
    result.append(str(consecutive))
    result.append(str(prev_c))
    return ''.join(result)



def part_one():
    result = '1113222113'
    for _ in range(40):
        result = look_and_say(result)
    print('After 40 iterations length is:', len(result))


part_one()

class Test(unittest.TestCase):
    def test_look_and_say(self):
        self.assertEqual('11', look_and_say('1'))
        self.assertEqual('21', look_and_say('11'))
        self.assertEqual('1211', look_and_say('21'))
        self.assertEqual('111221', look_and_say('1211'))
        self.assertEqual('312211', look_and_say('111221'))