import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        connections = f.read().strip().split('\n')
    parsed_connections = [connection.split(' ') for connection in connections]
    return parsed_connections


class SignalProvider:
    def __init__(self):
        self.output = None


class NumericSignal(SignalProvider):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal


class Wire(SignalProvider):
    all_instances = {}

    def __init__(self, wire_id):
        super().__init__()
        self.wire_id = wire_id
        self.input = None
        self.output = set()
        if self.wire_id in self.all_instances.keys():
            raise ValueError(f'Wire id {self.wire_id} already exists')
        self.all_instances[self.wire_id] = self

    @classmethod
    def wire_factory(cls, wire_id):
        if wire_id in cls.all_instances.keys():
            return cls.all_instances[wire_id]
        return Wire(wire_id)


class Gate(SignalProvider):
    def __init__(self):
        super().__init__()
        self.input_one = None
        self.input_two = None
        self.output = None


class AndGate(Gate):
    pass


class OrGate(Gate):
    pass


class NotOperation(SignalProvider):
    def __init__(self, operand):
        super().__init__()
        self.operand = operand


class BitShift(SignalProvider):
    def __init__(self, shift_size):
        super().__init__()
        self.shift_size = shift_size
    def __repr__(self):
        return f'{self.__class__.__name__} shift_size: {self.shift_size}'


class LeftShift(BitShift):
    pass


class RightShift(BitShift):
    pass


def wire_up_signal_providers(connections):
    for connection in connections:
        if connection[0] == 'NOT':
            assert (connection[2] == '->')
            op = NotOperation(connection[1])
            op.output = Wire.wire_factory(connection[3])
        elif connection[1] == 'OR':
            assert (connection[3] == '->')
            op = OrGate()
            op.output = Wire.wire_factory(connection[4])
            op.input_one = Wire.wire_factory(connection[0])
            op.input_two = Wire.wire_factory(connection[2])
        elif connection[1] == 'AND':
            assert (connection[3] == '->')
            op = AndGate()
            op.output = Wire.wire_factory(connection[4])
            op.input_one = Wire.wire_factory(connection[0])
            op.input_two = Wire.wire_factory(connection[2])
        elif connection[1] == 'LSHIFT':
            assert (connection[3] == '->')
            op = LeftShift(connection[2])
            op.output = Wire.wire_factory(connection[4])
            op.input_one = Wire.wire_factory(connection[0])
            op.input_two = Wire.wire_factory(connection[2])
        elif connection[1] == 'RSHIFT':
            assert (connection[3] == '->')
            op = LeftShift(connection[2])
            op.output = Wire.wire_factory(connection[4])
            op.input_one = Wire.wire_factory(connection[0])
            op.input_two = Wire.wire_factory(connection[2])
        elif connection[1] == '->':
            op = NumericSignal(connection[0])
            op.output = Wire.wire_factory(connection[2])
        else:
            raise ValueError(f'Can not interpret "{connection}" ')


def part_one(filename):
    connections = read_puzzle_input(filename)
    wire_up_signal_providers(connections)
    # [print(connection) for connection in connections]


part_one('Day_07_input.txt')


class Test(unittest.TestCase):
    def test_bit_shift(self):
        ls = LeftShift(2)
        self.assertEqual(2, ls.shift_size)
        rs = RightShift(3)
        self.assertEqual(3, rs.shift_size)
