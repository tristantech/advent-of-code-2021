FILE = "days/09/input.txt"

with open(FILE, "r") as f:
    grid = []
    for line in f:
        gridrow = []
        for c in line.strip():
            gridrow.append(int(c))
        grid.append(gridrow)

def find_low_points(g):
    low_points = []

    for y in range(len(g[0])):
        for x in range(len(g)):
            z = g[x][y]
            is_low_pt = True

            # Make sure we are lower than all surrounding
            # points, taking bounds in to consideration.
            if x > 0 and z >= g[x-1][y]:
                is_low_pt = False
            if y > 0 and z >= g[x][y-1]:
                is_low_pt = False
            if x < len(g)-1 and z >= g[x+1][y]:
                is_low_pt = False
            if y < len(g[0])-1 and z >= g[x][y+1]:
                is_low_pt = False
            
            if is_low_pt:
                low_points.append((x, y, z))

    return low_points

def flood(x, y, g, visited):
    # Make sure we don't visit any cell more than once
    if (x,y) in visited:
        return 0
    visited.add((x,y))

    # If we hit a 9 (edge of basin), stop. Otherwise, this
    # counts as part of the basin.
    if g[x][y] == 9:
        return 0
    else:
        count = 1

    # Now try hunting in each direction as long as we don't
    # go out of bounds. Any additional basin space we find
    # in each direction gets added to our total count.
    if x > 0:
        count += flood(x-1, y, g, visited)
    if y > 0:
        count += flood(x, y-1, g, visited)
    if x < len(g)-1:
        count += flood(x+1, y, g, visited)
    if y < len(g[0])-1:
        count += flood(x, y+1, g, visited)

    return count

def part1(low_points):
    risk_counter = 0
    for _, _, z in low_points:
        risk_counter += z + 1
    return risk_counter

def part2(low_points, grid):
    # Go to each low point and do a DFS
    basins = []
    for x, y, _ in low_points:
        v = set()
        basins.append(flood(x, y, grid, v))
    
    # This could be further optimized with a min-heap, but
    # whatever
    basins.sort()
    return basins[-1] * basins[-2] * basins[-3]

low_points = find_low_points(grid)

print("Part I", part1(low_points))
print("Part II", part2(low_points, grid))
