import unittest
from abc import abstractmethod


class Wire:
    all_instances = {}

    def __init__(self, wire_id):
        self.signal_value = None
        self.wire_id = wire_id
        # Input from one of Gate, Wire, or Value
        self.receiver = None
        # Zero or more transmitter targets
        self.transmitter = set()
        if self.wire_id in self.all_instances.keys():
            raise ValueError(f'Wire id {self.wire_id} already exists')
        self.all_instances[self.wire_id] = self

    def __repr__(self):
        return f'Wire id({self.wire_id}) receiver({self.receiver}) transmitter({self.transmitter})'

    @classmethod
    def wire_factory(cls, wire_id):
        if isinstance(wire_id, int):
            raise ValueError('wire_id cannot be an integer')
        if wire_id in cls.all_instances.keys():
            return cls.all_instances[wire_id]
        return Wire(wire_id)

    def send_signal(self):
        assert(self.signal_value != None)
        for connector in self.transmitter:
            connector.receive(self.wire_id, self.signal_value)

class Connector:

    def __init__(self):
        self.transmitter = None
        self.signal_value = None

    def __repr__(self):
        return f'{self.__class__.__name__} transmitter({self.transmitter}) signal_value({self.signal_value})'

    @abstractmethod
    def operate(self):
        pass

class SingleReceiverConnector(Connector):
    def __init__(self):
        super().__init__()
        self.receiver = None

    def __repr__(self):
        return super().__repr__() + f' receiver({self.receiver})'

    def receive(self, wire_id, signal_value):
        if wire_id != self.receiver:
            raise ValueError(f'"{wire_id}" is not received here')
        self.received_signal = signal_value
        self.operate()
        follow_circuit(self.transmitter, self.signal_value)


    def gate_is_ready_to_transmit(self):
        return self.received_signal != None

    def calculate_signal_value(self):
        assert(self.gate_is_ready_to_transmit())
        self.operate()


class DoubleReceiverConnector(Connector):
    def __init__(self):
        super().__init__()
        self.received_signal_one = None
        self.received_signal_two = None
        self.receiver_one = None
        self.receiver_two = None
    def __repr__(self):
        return super().__repr__() + f' receiver_one({self.receiver_one}) receiver_two({self.receiver_two})'

    def receive(self, wire_id, signal_value):
        if wire_id == self.receiver_one:
            self.received_signal_one = signal_value
        elif wire_id == self.receiver_two:
            self.received_signal_two = signal_value
        else:
            raise ValueError(f'"{wire_id}" is not received here')
        if self.gate_is_ready_to_transmit():
            self.operate()
            follow_circuit(self.transmitter, self.signal_value)

    def gate_is_ready_to_transmit(self):
        return self.received_signal_one != None and self.received_signal_two != None

class ShiftConnector(SingleReceiverConnector):
    def __init__(self):
        super().__init__()
        self.shift_size = None
    def __repr__(self):
        return super().__repr__() + f' shift_size({self.shift_size})'

class NotConnector(SingleReceiverConnector):
    def operate(self):
        self.signal_value = ~self.received_signal & 65535


class OrConnector(DoubleReceiverConnector):
    def operate(self):
        if self.received_signal_one == None or self.received_signal_two == None:
            pass
        self.signal_value = self.received_signal_one | self.received_signal_two


class AndConnector(DoubleReceiverConnector):
    def operate(self):
        if self.received_signal_one == None or self.received_signal_two == None:
            pass
        self.signal_value = self.received_signal_one & self.received_signal_two


class LShiftConnector(ShiftConnector):
    def operate(self):
        self.signal_value = (self.received_signal << self.shift_size) & 65535


class RShiftConnector(ShiftConnector):
    def operate(self):
        self.signal_value = self.received_signal >> self.shift_size


class SignalConnector(Connector):
    def operate(self):
        pass

class WireToWireConnector(SingleReceiverConnector):
    def operate(self):
        self.signal_value = self.received_signal


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
        elif connection[1] == '->' and isinstance(connection[0], int):
            connector = SignalConnector()
            connector.signal_value = connection[0]
            connector.transmitter = connection[2]
        elif connection[1] == '->':
            connector = WireToWireConnector()
            connector.receiver = connection[0]
            connector.transmitter = connection[2]
        else:
            raise ValueError(f'Can not interpret "{connection}" ')
        rval.append(connector)
    return rval


def wire_it_up(connectors):
    for connector in connectors:
        wire = Wire.wire_factory(connector.transmitter)
        wire.receiver = connector
        match connector:
            case SingleReceiverConnector():
                wire = Wire.wire_factory(connector.receiver)
                wire.transmitter.add(connector)
            case DoubleReceiverConnector():
                if isinstance(connector.receiver_one, int):
                    connector.received_signal_one = connector.receiver_one
                else:
                    wire = Wire.wire_factory(connector.receiver_one)
                    wire.transmitter.add(connector)
                if isinstance(connector.receiver_two, int):
                    connector.received_signal_two = connector.receiver_two
                else:
                    wire = Wire.wire_factory(connector.receiver_two)
                    wire.transmitter.add(connector)
            case SignalConnector():
                pass
            case _:
                raise ValueError(f'Unrecognized type({connector.__class__.__name__})')


def follow_circuit(wire_id: str, signal_value: int):
    wire = Wire.wire_factory(wire_id)
    wire.signal_value = signal_value
    wire.send_signal()


def juice_it_up(connectors):
    for connector in connectors:
        if isinstance(connector, SignalConnector):
            follow_circuit(connector.transmitter, connector.signal_value)


def part_one(filename):
    connections = read_puzzle_input(filename)
    type_convert_to_ints(connections)
    connectors = type_convert_to_connectors(connections)
    wire_it_up(connectors)
    juice_it_up(connectors)
    for wire in Wire.all_instances.values():
        print(wire)
    for x in connectors:
        print(x)


part_one('Day_07_input.txt')


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
