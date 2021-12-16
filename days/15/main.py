from queue import PriorityQueue
from collections import defaultdict

FILE = "days/15/input.txt"

class Grid(object):
    def __init__(self, file_path, repeat=1):
        with open(FILE, "r") as f:
            self.grid = []
            for line in f:
                gridrow = []
                for c in line.strip():
                    gridrow.append(int(c))
                self.grid.append(gridrow)
        
        self.base_width = len(self.grid)
        self.base_height = len(self.grid[0])

        # `repeat` is the number of times the grid is tiled, which would
        # be 1 for Part 1 and 5 for Part 2
        self.height = self.base_height * repeat
        self.width = self.base_width * repeat
    
    def get_neighbors(self, x, y):
        """
        Return the coordinates of all neighbors (no diagonals), taking the
        boundaries in to account.
        """
        for dx, dy in ((0,1), (0,-1), (1,0), (-1,0)):
            if x + dx < 0 or x + dx >= self.width:
                continue
            if y + dy < 0 or y + dy >= self.height:
                continue
            yield (x+dx, y+dy)

    def get_cost(self, x, y):
        """
        Return the value at point (x, y), which we treat as the cost to
        travel to this cell. For points beyond what's given in the file,
        follow the description in Part 2 to generate the value.
        """
        tile_x = x // self.base_width
        inner_x = x % self.base_width
        tile_y = y // self.base_height
        inner_y = y % self.base_height

        return ((self.grid[inner_y][inner_x] + tile_x + tile_y - 1) % 9) + 1

    def get_target_vertex(self):
        return (self.width-1, self.height-1)

def solve(g):
    """ Run Dijkstra's with a heap to find the best path. """

    visited = set()
    queue = PriorityQueue()
    dist = defaultdict(lambda: 9999999999)
    prev = defaultdict(lambda: None)

    # Set up the starting point
    dist[(0,0)] = 0   
    queue.put((0, (0,0)))

    while not queue.empty():
        _, u = queue.get()

        if u == g.get_target_vertex():
            # At the end --we don't need to search any further
            break
        
        for nx, ny in g.get_neighbors(u[0], u[1]):
            # Visit all neighbors and see if we can reach it better than
            # any other known path
            distance = dist[u] + g.get_cost(nx, ny)

            if distance < dist[(nx, ny)]:
                dist[(nx, ny)] = distance
                prev[(nx, ny)] = u
                if (nx,ny) not in visited:
                    visited.add((nx, ny))
                    queue.put((distance, (nx,ny)))

    # Now tally up the cost by tracing the optimal path backwards
    cost = 0
    x, y = g.get_target_vertex()
    while True:
        cost += g.get_cost(x, y)
        x, y = prev[(x, y)]
        if (x, y) == (0,0):
            break

    return cost


print("Part 1", solve(Grid(FILE, 1)))
print("Part 2", solve(Grid(FILE, 5)))