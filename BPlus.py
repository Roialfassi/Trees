class Node:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []
        self.next = None
        self.parent = None
        self.is_leaf = True

    def insert_in_leaf(self, key):
        """ Inserts a key in a leaf node in sorted order """
        index = 0
        while index < len(self.keys) and self.keys[index] < key:
            index += 1
        self.keys.insert(index, key)


class BplusTree:
    def __init__(self, order, verbose=False):
        self.root = Node(order)
        self.order = order
        self.verbose = verbose

    def insert(self, key):
        """ Public method to insert a key """
        if self.verbose:
            print(f"Inserting key: {key}")
        leaf = self._find_leaf(key)
        leaf.insert_in_leaf(key)

        if len(leaf.keys) >= self.order:
            self._split_leaf(leaf)

    def _find_leaf(self, key, node=None):
        """ Private method to find the appropriate leaf node for a given key """
        if node is None:
            node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return node

    def _split_leaf(self, leaf):
        """ Splits a full leaf node and adjusts the tree structure """
        mid_index = len(leaf.keys) // 2
        new_leaf = Node(leaf.order)
        new_leaf.is_leaf = True
        new_leaf.keys = leaf.keys[mid_index:]
        new_leaf.next = leaf.next
        leaf.keys = leaf.keys[:mid_index]
        leaf.next = new_leaf

        if leaf.parent:
            self._insert_in_parent(leaf, new_leaf, new_leaf.keys[0])
        else:
            self._create_new_root(leaf, new_leaf, new_leaf.keys[0])

    def _split_internal(self, node):
        """ Splits a full internal node and adjusts the tree structure """
        mid_index = len(node.keys) // 2
        new_internal = Node(node.order)
        new_internal.is_leaf = False
        new_internal.keys = node.keys[mid_index + 1:]
        new_internal.children = node.children[mid_index + 1:]

        for child in new_internal.children:
            child.parent = new_internal

        mid_key = node.keys[mid_index]
        node.keys = node.keys[:mid_index]
        node.children = node.children[:mid_index + 1]

        if node.parent:
            self._insert_in_parent(node, new_internal, mid_key)
        else:
            self._create_new_root(node, new_internal, mid_key)

    def _create_new_root(self, left, right, key):
        """ Creates a new root when the old root is split """
        new_root = Node(self.order)
        new_root.keys = [key]
        new_root.children = [left, right]
        new_root.is_leaf = False
        self.root = new_root
        left.parent = right.parent = new_root

    def _insert_in_parent(self, left, right, key):
        """ Inserts a new key into the parent node after a split """
        parent = left.parent
        index = parent.children.index(left) + 1
        parent.keys.insert(index - 1, key)
        parent.children.insert(index, right)
        right.parent = parent

        if len(parent.keys) >= self.order:
            self._split_internal(parent)

    def print_tree(self, node=None, indent="", last=True):
        """ Prints the tree structure in a visually appealing format """
        if not node:
            node = self.root

        ret = indent + ("`- " if last else "|- ") + str(node.keys) + "\n"
        indent += "   " if last else "|  "

        if not node.is_leaf:
            for i, child in enumerate(node.children[:-1]):
                ret += self.print_tree(child, indent, last=False)
            ret += self.print_tree(node.children[-1], indent, last=True)
        return ret


if __name__ == '__main__':
    # Example usage
    tree = BplusTree(order=4, verbose=True)
    keys_to_insert = [10, 20, 5, 15, 12, 30, 25, 22, 35, 36, 37, 38, 39]
    for key in keys_to_insert:
        tree.insert(key)
        print(tree.print_tree())
