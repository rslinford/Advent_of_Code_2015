import unittest

class Wire:
    all_instances = {}

    def __init__(self, wire_id):
        self.wire_id = wire_id
        # Input from one of Gate, Wire, or Value
        self.receiver = None
        # Zero or more transmitter targets
        self.transmitter = set()
        if self.wire_id in self.all_instances.keys():
            raise ValueError(f'Wire id {self.wire_id} already exists')
        self.all_instances[self.wire_id] = self

    def __repr__(self):
        return f'Wire id({self.wire_id}) input({self.receiver}) outputs({[x.wire_id for x in self.transmitter]})'

    @classmethod
    def wire_factory(cls, wire_id):
        if wire_id in cls.all_instances.keys():
            return cls.all_instances[wire_id]
        return Wire(wire_id)


class Connector:
    def __init__(self):
        self.transmitter = None

    def __repr__(self):
        return f'{self.__class__.__name__} transmitter({self.transmitter})'


class SingleReceiverConnector(Connector):
    def __init__(self):
        super().__init__()
        self.receiver = None

    def __repr__(self):
        return super().__repr__() + f' receiver({self.receiver})'


class DoubleReceiverConnector(Connector):
    def __init__(self):
        super().__init__()
        self.receiver_one = None
        self.receiver_two = None
    def __repr__(self):
        return super().__repr__() + f' receiver_one({self.receiver_one}) receiver_two({self.receiver_two})'


class ShiftConnector(SingleReceiverConnector):
    def __init__(self):
        super().__init__()
        self.shift_size = None
    def __repr__(self):
        return super().__repr__() + f' shift_size({self.shift_size})'

class NotConnector(SingleReceiverConnector):
    pass


class OrConnector(DoubleReceiverConnector):
    pass


class AndConnector(DoubleReceiverConnector):
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
            connector.receiver = connection[1]
            connector.transmitter = connection[3]
        elif connection[1] == 'OR':
            assert (connection[3] == '->')
            connector = OrConnector()
            connector.receiver_one = connection[0]
            connector.receiver_two = connection[2]
            connector.transmitter = connection[4]
        elif connection[1] == 'AND':
            assert (connection[3] == '->')
            connector = AndConnector()
            connector.receiver_one = connection[0]
            connector.receiver_two = connection[2]
            connector.transmitter = connection[4]
        elif connection[1] == 'LSHIFT':
            assert (connection[3] == '->')
            connector = LShiftConnector()
            connector.receiver = connection[0]
            connector.shift_size = connection[2]
            connector.transmitter = connection[4]
        elif connection[1] == 'RSHIFT':
            assert (connection[3] == '->')
            connector = RShiftConnector()
            connector.receiver = connection[0]
            connector.shift_size = connection[2]
            connector.transmitter = connection[4]
        elif connection[1] == '->':
            connector = SignalConnector()
            connector.signal_value = connection[0]
            connector.transmitter = connection[2]
        else:
            raise ValueError(f'Can not interpret "{connection}" ')
        rval.append(connector)
    return rval


def wire_it_up(connectors):
    for connector in connectors:
        output_wire = Wire.wire_factory(connector.transmitter)
        output_wire.receiver = connector


def x(connectors):
    for connector in connectors:
        match connector:
            case NotConnector():
                pass
            case OrConnector():
                pass
            case AndConnector():
                pass
            case LShiftConnector():
                pass
            case RShiftConnector():
                pass
            case SignalConnector():
                pass
            case _:
                raise ValueError(f'Unrecognized type({connector.__class__.__name__})')


def part_one(filename):
    connections = read_puzzle_input(filename)
    type_convert_to_ints(connections)
    connectors = type_convert_to_connectors(connections)
    wire_it_up(connectors)
    for wire in Wire.all_instances.values():
        print(wire)
    # for x in connectors:
    #     print(x)


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
        self.assertEqual('x', connectors[0].transmitter)
        self.assertEqual('d', connectors[2].transmitter)
        self.assertEqual('x', connectors[2].receiver_one)
        self.assertEqual('y', connectors[2].receiver_two)
        self.assertEqual('f', connectors[4].transmitter)
        self.assertEqual(2, connectors[4].shift_size)
        self.assertEqual('x', connectors[4].receiver)

    def test_wire(self):
        # self.assertEqual(0, len(Wire.all_instances))
        w1 = Wire('ab')
        # self.assertEqual(1, len(Wire.all_instances))
        self.assertEqual('ab', w1.wire_id)
        with self.assertRaises(ValueError):
            Wire('ab')
        w2 = Wire.wire_factory('ab')
        self.assertIs(w1, w2)

