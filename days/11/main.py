FILE = "days/11/input.txt"

class Grid(object):
    def __init__(self, file_path):
        with open(FILE, "r") as f:
            self.grid = []
            for line in f:
                gridrow = []
                for c in line.strip():
                    gridrow.append(int(c))
                self.grid.append(gridrow)
        
        self.height = len(self.grid)
        self.width = len(self.grid[0])
    
    def iterate(self):
        """ Simulate one step of the octopus puzzle """
        num_flashes = 0

        # Phase 1 - increment all octopuses
        self._increment_all_octopuses()

        # Phase 2 - run flash algorithm until we converge (no new flashes)
        has_flashed = set()
        count = 0
        while True:
            count = self._run_reaction(has_flashed)
            num_flashes += count
            if count == 0:
                break

        return num_flashes

    def _increment_all_octopuses(self):
        """ Increases all octopus numbers by 1 """
        for x in range(self.width):
            for y in range(self.height):
                self.grid[y][x] += 1

    def _run_reaction(self, has_flashed):
        """
        Runs one iteration of the flash sub-algorithm:
            1. Identify octopuses that are about to flash (>9) AND have
               not flashed already. Caller must provide a set to keep track
               of octopuses that already flashed previously in this step.
            2. Reset these octopuses to zero and increment each of their
               neighbors (unless the neighbor flashed, in which case they
               remain at zero)
        This algorithm should be run repeatedly until convergence, which
        is indicated by zero new flashes occurring. 
        """
        num_flashes = 0
        about_to_flash = []
        for x in range(self.width):
            for y in range(self.height):
                # Find all octopuses about to flash
                if self.grid[y][x] > 9 and (x,y) not in has_flashed:
                    about_to_flash.append((x,y))

        # Go back to each octopus and flash it and update neighbors
        for x, y in about_to_flash:
            num_flashes += 1
            has_flashed.add((x,y))
            self.grid[y][x] = 0
            for xn, yn in self._get_neighbors(x, y):
                # Boost neighbors that have not yet flashed
                if (xn, yn) in has_flashed:
                    continue
                self.grid[yn][xn] += 1
        
        return num_flashes

    def _get_neighbors(self, x, y):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    # Same point
                    continue
                if x + dx < 0 or x + dx >= self.width:
                    continue
                if y + dy < 0 or y + dy >= self.height:
                    continue
                yield (x+dx, y+dy)

    def get_total_octopuses(self):
        return self.width * self.height

    def print_grid(self):
        """ For debugging """
        for row in self.grid:
            print("".join(f"{c:2d}" for c in row))

def part1(steps):
    g = Grid(FILE)
    total = 0
    for _ in range(steps):
        total += g.iterate()
    
    return total

def part2():
    g = Grid(FILE)
    step = 0
    while True:
        step += 1
        num_flashes = g.iterate()
        if num_flashes == g.get_total_octopuses():
            return step

print("Part I:", part1(100))
print("Part II:", part2())