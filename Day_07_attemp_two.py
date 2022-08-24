import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        connections = f.read().strip().split('\n')
    parsed_connections = [connection.split(' ') for connection in connections]
    return parsed_connections

def type_convert_to_ints(parsed_connections):
    for i in range(len(parsed_connections)):
        for j in range(len(parsed_connections[i])):
            if parsed_connections[i][j].isdigit():
                parsed_connections[i][j] = int(parsed_connections[i][j])

def part_one(filename):
    connections = read_puzzle_input(filename)
    type_convert_to_ints(connections)
    for x in connections:
        print(x)

class Connector:
    def __init__(self):
        self.output_wire = None

class SingleWireOperandConnector(Connector):
    pass

class DoubleWireOperandConnector(Connector):
    def __init__(self):
        super().__init__()
        self.operand_wire_one = None
        self.operand_wire_two = None

class ShiftConnector(SingleWireOperandConnector):
    def __init__(self):
        super().__init__()
        self.operand_shift_size = None

class NotConnector(SingleWireOperandConnector):
    pass

class OrConnector(DoubleWireOperandConnector):
    pass

class AndConnector(DoubleWireOperandConnector):
    pass

class LShiftConnector(ShiftConnector):
    pass

class RShiftConnector(ShiftConnector):
    pass

class SignalConnector(Connector):
    pass

def x(connections):
    for connection in connections:
        if connection[0] == 'NOT':
            assert (connection[2] == '->')
            connector = NotConnector()
            connector.operand_wire = connection[1]
            connector.output_wire = connection[3]
        elif connection[1] == 'OR':
            assert (connection[3] == '->')
            connector = OrConnector()
            connector.operand_wire_one = connection[0]
            connector.operand_wire_two = connection[2]
            connector.output_wire = connection[4]
        elif connection[1] == 'AND':
            assert (connection[3] == '->')
            connector = AndConnector()
            connector.operand_wire_one = connection[0]
            connector.operand_wire_two = connection[2]
            connector.output_wire = connection[4]
        elif connection[1] == 'LSHIFT':
            assert (connection[3] == '->')
            connector = LShiftConnector()
            connector.operand_wire = connection[0]
            connector.operand_shift_size = connection[2]
            connector.output_wire = connection[4]
        elif connection[1] == 'RSHIFT':
            assert (connection[3] == '->')
            connector = RShiftConnector()
            connector.operand_wire = connection[0]
            connector.operand_shift_size = connection[2]
            connector.output_wire = connection[4]
        elif connection[1] == '->':
            connector = SignalConnector()
            connector.signal_value = connection[0]
            connector.output_wire = connection[2]
        else:
            raise ValueError(f'Can not interpret "{connection}" ')


part_one('Day_07_short_input.txt')

class Test(unittest.TestCase):
    def test_read_puzzle_input(self):
        parsed_connections = read_puzzle_input('Day_07_short_input.txt')
        self.assertEqual(8, len(parsed_connections))
        self.assertEqual('123', parsed_connections[0][0])
        self.assertEqual('->', parsed_connections[0][1])
        self.assertEqual('x', parsed_connections[0][2])

    def test_type_convert(self):
        parsed_connections = read_puzzle_input('Day_07_short_input.txt')
        self.assertEqual('123', parsed_connections[0][0])
        type_convert_to_ints(parsed_connections)
        self.assertEqual(123, parsed_connections[0][0])
