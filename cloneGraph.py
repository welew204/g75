from typing import Optional


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def cloneGraph(node: Optional['Node']) -> Optional['Node']:
    # way to store vals as I visit+copy them
    oldToNew = {}

    # recursive DepthFirstSearch
    def clone(node):
        # base case
        if node in oldToNew:
            return oldToNew[node]

        # otherwise, we need make a new one, and copy in the vals
        copy = Node(node.val)
        oldToNew[node] = copy
        for nei in node.neighbors:
            copy.neighbors.append(clone(nei))

        return copy

    return clone(node) if node else None


test1 = [[2, 4], [1, 3], [2, 4], [1, 3]]
