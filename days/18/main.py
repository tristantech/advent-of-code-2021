FILE = "days/18/input.txt"

class TreeNode(object):
    def __init__(self, value=None):
        self.children = []
        self.value = value
        self.parent = None
    
    def add_child(self, child):
        """
        Add a child under this node. Max of 2 allowed!
        """
        assert(len(self.children) < 2)

        self.children.append(child)
        child.parent = self
    
    def node_depth(self):
        """
        Calculate the depth of this node from the root (root has a depth
        of 1).
        """
        i = 0
        ptr = self
        while not ptr.is_root():
            i += 1
            ptr = ptr.parent
        return i

    def traverse(self):
        """
        Walks this node's children from left to right
        """
        for c in self.children:
            yield c
            yield from c.traverse()

    def is_leaf(self):
        return len(self.children) == 0
    
    def is_root(self):
        return self.parent is None

    def get_adjacent(self, dir):
        """
        Find the leaf node that is immediately left or right of this node,
        or return None if no such node exists.
        """
        assert(dir in ("left", "right"))

        ptr = self
        while True:
            # Search upwards until we find a node where we can go left.

            if ptr.is_root():
                # Made it all the way to the root node and couldn't
                # find anywhere to go left.
                return None
            siblings = ptr.parent.children
            idx = siblings.index(ptr)
            if dir == "left" and idx == 1:
                # Found something to the left. Now drill down until we get
                # to the first leaf node / "Regular" number
                ptr = siblings[0]
                while not ptr.is_leaf():
                    ptr = ptr.children[1]
                return ptr
            elif dir == "right" and idx == 0:
                # Same as above, but go right.
                ptr = siblings[1]
                while not ptr.is_leaf():
                    ptr = ptr.children[0]
                return ptr

            ptr = ptr.parent

    def explode(self):
        """
        Carry out the explode step in the reduction process
        """
        assert(len(self.children) == 2)

        child1, child2 = self.children[0], self.children[1]
        assert(child1.is_leaf())
        assert(child2.is_leaf())

        left = self.get_adjacent("left")
        if left:
            left.value += child1.value

        right = self.get_adjacent("right")
        if right:
            right.value += child2.value

        # This node becomes a zero and loses its children.
        self.children = []
        self.value = 0

    def split(self):
        assert(len(self.children) == 0)

        num1 = self.value // 2
        num2 = self.value - num1

        self.value = None
        self.add_child(TreeNode(num1))
        self.add_child(TreeNode(num2))

    def get_magnitude(self):
        """
        Compute the magnitude of this node in accordance with the instructions
        """
        if len(self.children) > 0:
            assert(len(self.children) == 2)

            magnitude = 0
            magnitude += 3 * self.children[0].get_magnitude()
            magnitude += 2 * self.children[1].get_magnitude()
            return magnitude
        else:
            return self.value

def parse_input_to_tree(string):
    """
    Converts a string shellfish number in to the tree structure we use for
    performing the additions. For example, the number [[1,2],3] becomes:

                 O    <- Non-leaf nodes represent a shellfish number pair.
                / \      These always have two children.
               O   3  <- Leaf nodes have integer values.
              / \ 
              1 2
    """

    # Don't try this at home
    lists = eval(string)
    
    def parse_helper(lst, parent):
        for item in lst:
            if type(item) is list:
                new_parent = TreeNode()
                parent.add_child(new_parent)
                parse_helper(item, new_parent)

            elif type(item) is int:
                # "Regular" number
                new_node = TreeNode(item)
                parent.add_child(new_node)

            else:
                raise RuntimeError("Unexpected type")
    
    # Create a tree from this data using this recursive helper function to
    # build out the tree structure
    tree = TreeNode()
    parse_helper(lists, tree)

    return tree

def reduce_tree(tree):
    """
    Reduce the shellfish number in accordance to the rules.
    """
    while True:
        action_completed = False

        # Check if any pair needs to be exploded. 
        for node in tree.traverse():
            if node.node_depth() >= 4 and not node.is_leaf():
                # This node is too deeply nested. Time to explode it!
                node.explode()
                action_completed = True
                break

        if action_completed:
            continue

        # Check if any pair needs to be split
        for node in tree.traverse():
            if node.is_leaf() and node.value > 9:
                # Found a node that needs to be split
                node.split()
                action_completed = True
                break

        if action_completed:
            continue

        # If we reach this point, not further reduction is necessary
        break

def add_trees(tree1, tree2):
    """
    Add two trees together and reduce the result.
    """
    if (tree1 is None) != (tree2 is None):
        # If one tree is None, just return the other
        return tree1 or tree2

    new_root = TreeNode()
    new_root.add_child(tree1)
    new_root.add_child(tree2)

    reduce_tree(new_root)
    return new_root

def part1(file):
    with open(file, "r") as f:
        total = None
        for line in f:
            tree = parse_input_to_tree(line)
            total = add_trees(total, tree)
        return total.get_magnitude()

def part2(file):
    with open(file, "r") as f:
        lines = f.readlines()

    # Now try to add each pair of numbers. Re-parse them each time
    # because the reduction step is destructive.
    max_mag = 0
    for i in lines:
        for j in lines:
            if i == j:
                continue
            mag = add_trees(
                parse_input_to_tree(i),
                parse_input_to_tree(j)
            ).get_magnitude()
            if mag > max_mag:
                max_mag = mag
    return max_mag

print("Part 1", part1(FILE))
print("Part 2", part2(FILE))
