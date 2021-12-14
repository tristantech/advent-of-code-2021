from collections import Counter, defaultdict
import math

FILE = "days/14/input.txt"

def solve(template, rules, iterations):
    # Initial set of pairs
    c = Counter([f"{template[i-1]}{template[i]}" for i in range(1, len(template))])

    for _ in range(iterations):
        # This dict contains all the updates (plus or minus) we need to apply
        # to each pair count before the next iteration
        updates = defaultdict(lambda: 0)

        for pair in c.keys():
            # For every pair of letters currently being tracked

            if pair not in rules:
                # Don't do anything if there is no rule for this pair (nothing
                # gets expanded)
                continue

            # The original pair is now gone. Make sure we subtract *each* of
            # the pairs!
            updates[pair] -= c[pair]

            # Add two new pairs made with the letters of the original pair
            # and the new letter, multiplied by the number of pairs we are
            # replacing.
            updates[f"{pair[0]}{rules[pair]}"] += c[pair]
            updates[f"{rules[pair]}{pair[1]}"] += c[pair]

        # Apply the updates to the main pair counter.
        c += updates

    # Finally, we need to convert pair counts to individual letter counts. This
    # double-counts all letters except the first and last.
    letter_counts = defaultdict(lambda: 0)
    for pair in c.keys():
        letter_counts[pair[0]] += c[pair]
        letter_counts[pair[1]] += c[pair]
    
    # Increase first and last letters from starting string
    letter_counts[template[0]] += 1
    letter_counts[template[-1]] += 1

    return ((max(letter_counts.values()) // 2) - 
            (min(letter_counts.values()) // 2))


with open(FILE, "r") as f:
    sections = f.read().strip().split("\n\n")
    
    template = sections[0].strip()
    rules = {}

    for line in sections[1].split("\n"):
        # Conversion rules
        parts = line.split("->")
        rules[parts[0].strip()] = parts[1].strip()

print("Part 1", solve(template, rules, 10))
print("Part 2", solve(template, rules, 40))