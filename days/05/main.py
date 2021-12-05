import re

FILE = "days/05/input.txt"

def points_along_line(x1, y1, x2, y2):
    # Number of points on line segment (including endpoints)
    steps = max(abs(x1-x2), abs(y1-y2)) + 1

    # Change in x and y at each step
    dx = max(min(x2-x1, 1), -1)
    dy = max(min(y2-y1, 1), -1)

    for i in range(steps):
        yield (x1 + dx*i, y1 + dy*i)

def solve(include_diagonals):
    with open(FILE) as f:
        hits = {}
        r = re.compile("([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)")
        for line in f:
            matches = r.findall(line)[0]
            x1,y1 = int(matches[0]), int(matches[1])
            x2,y2 = int(matches[2]), int(matches[3])

            if not (include_diagonals or (x1 == x2 or y1 == y2)):
                # Skip diagonal lines unless they have been requested
                continue

            for x, y in points_along_line(x1, y1, x2, y2):
                if (x, y) not in hits:
                    hits[(x, y)] = 1
                else:
                    hits[(x, y)] += 1

        return sum([1 for v in hits.values() if v > 1])

print("Part I:", solve(False))
print("Part II:", solve(True))
