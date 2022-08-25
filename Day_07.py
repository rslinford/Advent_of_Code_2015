import unittest


def read_puzzle_input(filename):
    with open(filename, 'r') as f:
        connections = f.read().strip().split('\n')
    parsed_connections = [connection.split(' ') for connection in connections]
    return parsed_connections


class SignalProvider:
    def __repr__(self):
        return f'{self.__class__.__name__}'

class SingleSignalProvider(SignalProvider):
    def __init__(self, output):
        self.output = output
        self.output.receiver = self

    def __repr__(self):
        return f'{self.__class__.__name__} output {self.output.wire_id}'

class MultiSignalProvider(SignalProvider):
    def __init__(self, output):
        self.output_set = set()
        self.output_set.add(output)
        if output:
            output.receiver = self

    def __repr__(self):
        return f'{self.__class__.__name__} output {self.output_set}'

    def add_output(self, output):
        self.output_set.add(output)


class NumericSignal(SingleSignalProvider):
    def __init__(self, signal, output):
        super().__init__(output)
        self.signal = signal
    def __repr__(self):
        return f'{self.__class__.__name__} signal: {self.signal} output: {self.output.wire_id}'

class Wire(MultiSignalProvider):
    all_instances = {}

    def __init__(self, wire_id, output):
        super().__init__(output)
        self.wire_id = wire_id
        self.input = None
        self.output = set()
        if self.wire_id in self.all_instances.keys():
            raise ValueError(f'Wire id {self.wire_id} already exists')
        self.all_instances[self.wire_id] = self

    def __repr__(self):
        return f'Wire id: {self.wire_id} input: {self.input.wire_id} outputs: {[x.wire_id for x in self.output]}'

    @classmethod
    def wire_factory(cls, wire_id, output=None):
        if wire_id in cls.all_instances.keys():
            return cls.all_instances[wire_id]
        return Wire(wire_id, output)


class Gate(SignalProvider):
    def __init__(self, input_one: Wire, input_two: Wire, output: Wire):
        super().__init__()
        self.input_one = input_one
        self.input_two = input_two
        self.output = output
        self.output.input = self


class AndGate(Gate):
    def __init__(self, input_one, input_two, output):
        super().__init__(input_one, input_two, output)


class OrGate(Gate):
    def __init__(self, input_one, input_two, output):
        super().__init__(input_one, input_two, output)


class NotOperation(SignalProvider):
    def __init__(self, operand: Wire, output: Wire):
        super().__init__()
        self.operand = operand
        self.output = output
        self.output.input = self


class BitShift(SignalProvider):
    def __init__(self, shift_size, operand, output):
        super().__init__()
        self.shift_size = shift_size
        self.operand = operand
        self.output = output
        self.output.input = self
    def __repr__(self):
        return f'{self.__class__.__name__} shift_size: {self.shift_size}'


# LeftShift(connection[2], Wire.wire_factory(connection[0]), Wire.wire_factory(connection[4]))
class LeftShift(BitShift):
    def __init__(self, shift_size, operand, output):
        super().__init__(shift_size, operand, output)

# RightShift(Wire.wire_factory(connection[2]), Wire.wire_factory(connection[0]), Wire.wire_factory(connection[4]))
class RightShift(BitShift):
    def __init__(self, shift_size, operand, output):
        super().__init__(shift_size, operand, output)


def wire_up_signal_providers(connections):
    for connection in connections:
        if connection[0] == 'NOT':
            assert (connection[2] == '->')
            op = NotOperation(Wire.wire_factory(connection[1]), Wire.wire_factory(connection[3]))
            op.output.input = op
        elif connection[1] == 'OR':
            assert (connection[3] == '->')
            OrGate(Wire.wire_factory(connection[0]), Wire.wire_factory(connection[2]), Wire.wire_factory(connection[4]))
        elif connection[1] == 'AND':
            assert (connection[3] == '->')
            AndGate(Wire.wire_factory(connection[0]), Wire.wire_factory(connection[2]), Wire.wire_factory(connection[4]))
        elif connection[1] == 'LSHIFT':
            assert (connection[3] == '->')
            LeftShift(connection[2], Wire.wire_factory(connection[0]), Wire.wire_factory(connection[4]))
        elif connection[1] == 'RSHIFT':
            assert (connection[3] == '->')
            RightShift(Wire.wire_factory(connection[2]), Wire.wire_factory(connection[0]), Wire.wire_factory(connection[4]))
        elif connection[1] == '->':
            op = NumericSignal(connection[0],  Wire.wire_factory(connection[2]))
        else:
            raise ValueError(f'Can not interpret "{connection}" ')


def part_one(filename):
    connections = read_puzzle_input(filename)
    wire_up_signal_providers(connections)
    # [print(connection) for connection in connections]


# part_one('Day_07_input.txt')


class Test(unittest.TestCase):
    def test_bit_shift(self):
        a, b, c = Wire('a', None), Wire('b', None), Wire('c', None)
        ls = LeftShift(2, a, b)
        self.assertEqual(2, ls.shift_size)
        rs = RightShift(3, b, c)
        self.assertEqual(3, rs.shift_size)

    def test_wire_up_signal_providers(self):
        connections = read_puzzle_input('Day_07_short_input.txt')
        wire_up_signal_providers(connections)
        [print(x) for x in Wire.all_instances.values()]
