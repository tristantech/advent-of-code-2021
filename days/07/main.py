FILE = "days/07/input.txt"

def solve(initial_locs, cost_func):
    lowest_crab = min(initial_locs)
    highest_crab = max(initial_locs)

    lowest_fuel = -1

    for x in range(lowest_crab, highest_crab+1):
        # Try moving them to this position and see how much
        # it costs. Keep track of the lowest fuel cost.
        fuel = 0
        for c in initial_locs:
            steps = abs(x - c)
            fuel += cost_func(steps)

        if lowest_fuel == -1 or fuel < lowest_fuel:
            lowest_fuel = fuel

    return lowest_fuel

with open(FILE) as f:
    crab_locations = list(map(int, f.read().strip().split(",")))

print("Part I", solve(crab_locations, lambda steps: steps))
print("Part II", solve(crab_locations, lambda steps: ((steps)*(steps+1) // 2)))
