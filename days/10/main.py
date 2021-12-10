FILE = "days/10/input.txt"

OPENING = ['[', '(', '{', '<']
CLOSING = [']', ')', '}', '>']

SCORES_CORRUPTION = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

SCORES_AUTOCOMPLETE = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

def scan_line(line):
    """
    Scan a line and check for corruption. Returns (score, stack) where
    `score` is the corruption score, or 0 if not corrupt. `stack` is the
    list of all unclosed chunks in order.
    """
    stack = []
    line = line.strip()
    for c in line:
        if c in OPENING:
            # Begin tracking new chunk
            stack.append(c)
        elif c in CLOSING:
            # Pop char off stack and make sure it matches. If so,
            # the chunk can be considered closed and it is no longer
            # tracked in the stack. If no match, we found corruption.
            x = stack.pop()
            if OPENING.index(x) != CLOSING.index(c):
                # Mismatch
                return SCORES_CORRUPTION[c], stack
        else:
            raise ValueError(f"Illegal char '{c}'")

    # Not corrupt
    return 0, stack

def part1(lines):
    score = 0
    for l in lines:
        s, _ = scan_line(l)
        score += s
    return score

def part2(lines):
    scores = []
    for l in lines:
        corrupt_score, stack = scan_line(l)
        if corrupt_score > 0:
            # Not dealing with corrupted lines
            continue
        
        score = 0

        # To get closing string, just read the stack backwards because
        # it contains all the unclosed chunks.
        for c in stack[::-1]:
            score *= 5
            score += SCORES_AUTOCOMPLETE[c]
        scores.append(score)

    scores.sort()
    return scores[len(scores)//2]

with open(FILE, "r") as f:
    lines = f.readlines()

print("Part I", part1(lines))
print("Part II", part2(lines))
