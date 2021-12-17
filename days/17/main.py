"""
This is a crappy brute force solution. It makes some assumptions about what
ranges of velocities to try and number of timesteps to simulate, so it might
not work for your input.
"""

import re

FILE = "days/17/input.txt"

def trajectory(vx, vy, steps=500):
    """
    Returns the trajectory given an initial X and Y velocity, one
    point at a time.
    """
    x, y = 0, 0
    drag = -1 if vx > 0 else 1
    for t in range(steps):
        x += vx
        if vx != 0:
            vx += drag
        y += vy
        vy -= 1

        yield (t, x, y)

with open(FILE, "r") as f:
    r = re.compile("x=([0-9\-]+)..([0-9\-]+), y=([0-9\-]+)..([0-9\-]+)")
    target = list(map(int, r.findall(f.read())[0]))

ymax = None
best_initial_velocities = None
working_initial_velocities = set()

for vx in range(0, 100):
    for vy in range(-2000, 2000):
        this_run_ymax = None
        for t, x, y in trajectory(vx, vy):
            if this_run_ymax is None or y > this_run_ymax:
                this_run_ymax = y
            if target[1] >= x >= target[0] and target[3] >= y >= target[2]:
                print(f"Hit! v=({vx},{vy}) t={t}, this_max={this_run_ymax} vs {ymax}")
                working_initial_velocities.add((vx, vy))
                if ymax is None or this_run_ymax > ymax:
                    ymax = this_run_ymax
                    best_initial_velocities = (vx, vy)
                break

print("Part 1", ymax)
print("Part 2", len(working_initial_velocities))
