FILE = "days/13/input.txt"

X = 0
Y = 1

with open(FILE, "r") as f:
    sections = f.read().strip().split("\n\n")
    coords = []
    fold_instructions = []
    for line in sections[0].split("\n"):
        # Coords
        pair = line.strip().split(",")
        coords.append((int(pair[0]), int(pair[1])))

    for line in sections[1].split("\n"):
        # Fold instructions
        parts = line.split("=")
        fold_instructions.append(("x" if "x" in parts[0] else "y", int(parts[1])))

def fold(coords, folds):
    coords = set(coords)
    new_coords = set()
    for axis, line in folds:
        for x, y in coords:
            if axis == "x" and x > line:
                # Mirror over vertical line
                new_coords.add((2*line - x, y))
            elif axis == "y" and y > line:
                # Mirror over horizontal line
                new_coords.add((x, 2*line - y))
            else:
                # No transformation for this point
                new_coords.add((x, y))

        coords = new_coords
        new_coords = set()
    return coords

def part1(coords, fold_instructions):
    return len(fold(coords, fold_instructions[0:1]))

def part2(coords, fold_instructions):
    import matplotlib.pyplot as plt
    
    # Invert the Y-coords or else the image will be
    # up-side down due to the puzzle's coordinate system
    points = fold(coords, fold_instructions)
    x = [x for x, _ in points]
    y = [-y for _, y in points]

    plt.scatter(x, y)
    plt.show()

print("Part I", part1(coords, fold_instructions))

# Part 2 is best viewed as a plot
part2(coords, fold_instructions)
