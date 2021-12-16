from bitarray import bitarray
import enum

FILE = "days/08/input.txt"

class Seg(enum.IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6

rows = []
with open(FILE, "r") as f:
    for line in f:
        parts = line.split("|")
        if len(parts) != 2:
            continue
        rows.append((parts[0].strip().split(" "), parts[1].strip().split(" ")))

def part1(rows):
    count = 0
    for _, outputs in rows:
        for o in outputs:
            if len(o) in (2,3,4,7):
                count += 1
    return count

def letters_to_bitarray(str):
    lookup = "abcdefg"
    b = bitarray(7)
    b.setall(0)
    for c in str:
        b[lookup.index(c)] = 1
    return b

def decode_digit(decode_mapping, seg_str):
    lookup = "abcdefg"
    actual_segs = set()

    for c in seg_str:
        actual_segs.add(decode_mapping[lookup.index(c)])
    
    if actual_segs == {Seg.C, Seg.F}:
        return 1
    if actual_segs == {Seg.A, Seg.C, Seg.D, Seg.E, Seg.G}:
        return 2
    if actual_segs == {Seg.A, Seg.C, Seg.D, Seg.F, Seg.G}:
        return 3
    if actual_segs == {Seg.B, Seg.C, Seg.D, Seg.F}:
        return 4
    if actual_segs == {Seg.A, Seg.B, Seg.D, Seg.F, Seg.G}:
        return 5
    if actual_segs == {Seg.A, Seg.B, Seg.D, Seg.E, Seg.F, Seg.G}:
        return 6
    if actual_segs == {Seg.A, Seg.C, Seg.F}:
        return 7
    if actual_segs == {Seg.A, Seg.B, Seg.C, Seg.D, Seg.E, Seg.F, Seg.G}:
        return 8
    if actual_segs == {Seg.A, Seg.B, Seg.C, Seg.D, Seg.F, Seg.G}:
        return 9
    if actual_segs == {Seg.A, Seg.B, Seg.C, Seg.E, Seg.F, Seg.G}:
        return 0
    raise ValueError("Not a valid digit")

def part2(rows):
    count = 0
    for sigs, digits in rows:
        # Mapping of input signal to actual segment using ints (A=0 ... G=6)
        mapping = {i: None for i in Seg}

        # Keys = # of lit segments, values = list of indexes in sigs
        # with that length
        segment_counts = {i: [] for i in range(1, 8)}

        # Version of sigs in the binary representation
        sigs_bin = []

        for i, s in enumerate(sigs):
            # For each of the 10 signal patterns
            segment_counts[len(s)].append(i)
            sigs_bin.append(letters_to_bitarray(s))
        
        # Find A by comparing #1 and #7 (ID'd by length)
        mapping[Seg.A] = \
            (sigs_bin[segment_counts[2][0]] ^ sigs_bin[segment_counts[3][0]]) \
            .index(bitarray('1'))
        
        # Find D by identifying which element 2,3,5 (the len-5) have in common that
        # is *not* A or something in common with #4
        temp = sigs_bin[segment_counts[5][0]] & sigs_bin[segment_counts[5][1]] & \
             sigs_bin[segment_counts[5][2]]
        temp[mapping[Seg.A]] = 0 # Not the one already identified as Seg A
        temp &= sigs_bin[segment_counts[4][0]] # Not anything in common with 4
        mapping[Seg.D] = temp.index(bitarray('1'))

        # Find G by identifying which seg all the len-5 signals have in common
        # that is not already identified
        temp = sigs_bin[segment_counts[5][0]] & sigs_bin[segment_counts[5][1]] & \
             sigs_bin[segment_counts[5][2]]
        temp[mapping[Seg.A]] = 0
        temp[mapping[Seg.D]] = 0
        mapping[Seg.G] = temp.index(bitarray('1'))

        # Find B: Take the 4 letters the len-6 sigs have in common and eliminate
        # the two already identified. The eliminate the letter in common with #1.
        temp = sigs_bin[segment_counts[6][0]] & sigs_bin[segment_counts[6][1]] & \
             sigs_bin[segment_counts[6][2]]
        temp[mapping[Seg.A]] = 0
        temp[mapping[Seg.G]] = 0
        temp &= ~sigs_bin[segment_counts[2][0]] # Not anything in common with 1
        mapping[Seg.B] = temp.index(bitarray('1'))

        # Find F. It is the only unidentified segment in len-5 sigs that has
        # segment B lit (#5).
        has_b = -1
        for i in segment_counts[5]:
            if sigs_bin[i][mapping[Seg.B]]:
                has_b = sigs_bin[i]

        has_b[mapping[Seg.A]] = 0
        has_b[mapping[Seg.D]] = 0
        has_b[mapping[Seg.G]] = 0
        has_b[mapping[Seg.B]] = 0
        mapping[Seg.F] = has_b.index(bitarray('1'))

        # Find C. It is the other segment in #1
        temp = sigs_bin[segment_counts[2][0]]
        temp[mapping[Seg.F]] = 0
        mapping[Seg.C] = temp.index(bitarray('1'))

        # Find E. It is the only un-ID'd segment left
        temp = bitarray('1'*7)
        for seg in (Seg.A, Seg.B, Seg.C, Seg.D, Seg.F, Seg.G):
            temp[mapping[seg]] = 0
        mapping[Seg.E] = temp.index(bitarray('1'))

        for k, v in mapping.items():
            print(k, Seg(v) if v is not None else "-")
        
        #
        # Now decode the indicated numbers
        #

        # The dict was more convenient to build in its original order,
        # but now swap keys and values for easy decoding
        decode = {v: k for k, v in mapping.items()}

        for i, digit in enumerate(digits):
            count += 10**(3-i) * decode_digit(decode, digit)

    return count

print("Part I", part1(rows))
print("Part II", part2(rows))
