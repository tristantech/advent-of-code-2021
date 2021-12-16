import binascii
import enum

from bitarray import bitarray
from bitarray.util import ba2int

FILE = "days/16/input.txt"

class PacketType(enum.IntEnum):
    Sum = 0
    Product = 1
    Min = 2
    Max = 3
    Literal = 4
    GreaterThan = 5
    LessThan = 6
    Equal = 7

class BasePacket(object):
    """
    Used as a base class for the specific packet types (Operator and
    Literal), but also as a container for the root packet(s). In practice,
    there is only ever one root packet in the bitstrings used in AoC.
    """
    def __init__(self):
        self.children = []

    def add_child(self, child_packet):
        """ Adds a subpacket to this packet """
        self.children.append(child_packet)
    
    def walk_children(self):
        """
        Walk the packet hierarchy. Yield each child and its own children.
        """
        for c in self.children:
            yield c
            yield from c.walk_children()
    
    def solve(self):
        # The superpacket can potentially contain multiple unrelated parent
        # packets, so solve each separately and return multiple results.
        return [c.solve() for c in self.children]

class LiteralPacket(BasePacket):
    def __init__(self, version, typ, value):
        self.version = version
        self.typ = typ
        self.value = value

        super().__init__()

    def add_child(self, child_packet):
        raise RuntimeError("Literal packets cannot have child packets")

    def solve(self):
        # No children or operations to evaluate, so just return our value
        return self.value

    def __str__(self) -> str:
        return f"<Literal v={self.version} t={self.typ} val={self.value}>"

    __repr__ = __str__

class OperatorPacket(BasePacket):
    def __init__(self, version, typ):
        self.version = version
        self.typ = typ

        super().__init__()

    def solve(self):
        # Evaluate this packet (and its children) based on the type
        if self.typ == PacketType.Sum:
            return sum([c.solve() for c in self.children])
        elif self.typ == PacketType.Product:
            prod = 1
            for c in self.children:
                prod *= c.solve()
            return prod
        elif self.typ == PacketType.Min:
            return min([c.solve() for c in self.children])
        elif self.typ == PacketType.Max:
            return max([c.solve() for c in self.children])
        elif self.typ == PacketType.Literal:
            raise RuntimeError("This should not be a literal packet")
        elif self.typ == PacketType.GreaterThan:
            assert(len(self.children) == 2)
            return int(self.children[0].solve() > self.children[1].solve())
        elif self.typ == PacketType.LessThan:
            assert(len(self.children) == 2)
            return int(self.children[0].solve() < self.children[1].solve())
        elif self.typ == PacketType.Equal:
            assert(len(self.children) == 2)
            return int(self.children[0].solve() == self.children[1].solve())
        else:
            raise RuntimeError(f"Unsupported type {self.typ}")

    def __str__(self) -> str:
        kids = ",".join([str(c) for c in self.children])
        return f"<Operator v={self.version} t={self.typ} kids=[{kids}]>"

    __repr__ = __str__


def decode(ascii_data):
    bin_data = binascii.a2b_hex(ascii_data)
    bits = bitarray()
    bits.frombytes(bin_data)

    def decode_helper(parent, i=0):
        """
        Recursive packet parser. If a packet has subpackets (children), they
        will be automatically decoded as well and added to the `parent` packet.

         * `parent` - Parent packet or superpacket that newly discovered packets
                      should get added to.
         * `i`      - bit position within the `bits` bitarray to start decoding
                      at.
        
        Returns the bit position right after the end of the packet that was
        decoded.
        """
        v = ba2int(bits[i:i+3])
        t = PacketType(ba2int(bits[i+3:i+6]))
        i += 6

        if t == PacketType.Literal:
            # Literal packet
            value = 0
            more_to_decode = True
            while more_to_decode:
                chunk = bits[i:i+5]
                if chunk[0] == 0:
                    more_to_decode = False
                value <<= 4
                value |= ba2int(chunk[1:])
                i += 5
            
            new_packet = LiteralPacket(v, t, value)
            parent.add_child(new_packet)
        else:
            # Operator packet
            length_mode = bits[i]
            i+= 1

            # Create a new packet object for this and register it
            new_packet = OperatorPacket(v, t)
            parent.add_child(new_packet)

            if length_mode == 1:
                # "the next 11 bits are a number that represents
                # the number of sub-packets immediately contained"
                num_sub_packets = ba2int(bits[i:i+11])
                i += 11

                for _ in range(num_sub_packets):
                    i = decode_helper(new_packet, i)

            else:
                # "the next 15 bits are a number that represents the
                # total length in bits of the sub-packets contained by
                # this packet."
                subpackets_bit_count = ba2int(bits[i:i+15])
                i += 15

                subpackets_end_bit = i + subpackets_bit_count
                while i < subpackets_end_bit:
                    i = decode_helper(new_packet, i)

        # Return the position in to the bit array where the packet ended
        return i

    # Superpacket isn't truly a packet, but it holds all the decoded root
    # packets as its children. For AoC, there will only be one root packet.
    superpacket = BasePacket()
    decode_helper(superpacket)

    return superpacket

def part1(data):
    sp = decode(data)

    version_sum = 0
    for c in sp.walk_children():
        # Sum every packet's version number
        version_sum += c.version

    return version_sum

def part2(data):
    sp = decode(data)

    # Evaluate the only root packet
    return sp.solve()[0]

with open(FILE, "r") as f:
    data = f.read()

print("Part 1", part1(data))
print("Part 2", part2(data))
