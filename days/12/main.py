FILE = "days/12/input.txt"

with open(FILE, "r") as f:
    # Build a list of neighbors for each node
    connections = {}
    for line in f:
        parts = line.strip().split("-")
        if len(parts) < 2:
            continue

        a, b = parts[0], parts[1]
        if a not in connections:
            connections[a] = []
        if b not in connections:
            connections[b] = []
        connections[a].append(b)
        connections[b].append(a)

def is_little_cave(node):
    return node.islower() and node not in ("start", "end")

def is_big_cave(node):
    return node.isupper()

def count_paths(conn, allow_second_visits):
    # DFS recursive helper
    def helper(node, visited, little_cave_revisited):
        if node in visited:
            if is_little_cave(node) and not little_cave_revisited:
                # We can revisit a single little cave once per path
                little_cave_revisited = True
            else:
                return 0

        if node == "end":
            # Bubble up a 1 to indicate we found one new path
            return 1
        
        if not is_big_cave(node):
            # Big caves can be revisited an unlimited number of times, but
            # track all little caves and the start node.
            visited.add(node)
        
        count = 0
        for neighbor in conn[node]:
            # Continue path finding in each neighbor's direction. Each child
            # path gets a its own copy of the visited nodes up to this point
            # because the paths will diverge here.
            count += helper(neighbor, visited.copy(), little_cave_revisited)
        return count
    
    return helper("start", set(), not allow_second_visits)

print("Part I", count_paths(connections, False))
print("Part II", count_paths(connections, True))
