import unittest


class Connector:
    def __init__(self):
        self.output_wire = None

    def __repr__(self):
        return f'{self.__class__.__name__} output_wire({self.output_wire})'


class SingleWireOperandConnector(Connector):
    def __init__(self):
        super().__init__()
        self.operand_wire = None

    def __repr__(self):
        return super().__repr__() + f' operand_wire({self.operand_wire})'


class DoubleWireOperandConnector(Connector):
    def __init__(self):
        super().__init__()
        self.operand_wire_one = None
        self.operand_wire_two = None
    def __repr__(self):
        return super().__repr__() + f' operand_wire_one({self.operand_wire_one}) operand_wire_two({self.operand_wire_two})'


class ShiftConnector(SingleWireOperandConnector):
    def __init__(self):
        super().__init__()
        self.operand_shift_size = None
    def __repr__(self):
        return super().__repr__() + f' operand_shift_size({self.operand_shift_size})'

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
    def __init__(self):
        super().__init__()
        self.signal_value = None
    def __repr__(self):
        return super().__repr__() + f' signal_value({self.signal_value})'


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


def type_convert_to_connectors(connections):
    rval = []
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
        rval.append(connector)
    return rval


def part_one(filename):
    connections = read_puzzle_input(filename)
    type_convert_to_ints(connections)
    connectors = type_convert_to_connectors(connections)
    for x in connectors:
        print(x)


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

    def test_type_convert_to_connectors(self):
        parsed_connections = read_puzzle_input('Day_07_short_input.txt')
        type_convert_to_ints(parsed_connections)
        connectors = type_convert_to_connectors(parsed_connections)
        self.assertEqual(123, connectors[0].signal_value)
        self.assertEqual('x', connectors[0].output_wire)
        self.assertEqual('d', connectors[2].output_wire)
        self.assertEqual('x', connectors[2].operand_wire_one)
        self.assertEqual('y', connectors[2].operand_wire_two)
        self.assertEqual('f', connectors[4].output_wire)
        self.assertEqual(2, connectors[4].operand_shift_size)
        self.assertEqual('x', connectors[4].operand_wire)
