FILE = "days/06/input.txt"

with open(FILE) as f:
    initial_fish = list(map(int, f.read().strip().split(",")))

def fish_simulator(fish, days):
    # Keeps track of number of fish at each day in their cycle
    histo = [0 for age in range(9)]

    for f in fish:
        histo[f] += 1
    
    for day in range(days):
        # Day 0 fish will reproduce
        ready_to_reproduce = histo[0]
        
        # Shift all fish one day closer to reproduction day, and
        # introduce the newly born fish at position 8.
        histo = histo[1:] + [ready_to_reproduce]

        # Fish that just reproduced now go back to day 6
        histo[6] += ready_to_reproduce
    
    return sum(histo)

print("Part I:", fish_simulator(initial_fish, 80))
print("Part II:", fish_simulator(initial_fish, 256))
