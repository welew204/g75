# Definition for a binary tree node.
from collections import deque


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lowestCommonAncestor(root, p, q):
    # DFS to find p or q
    # when found, then there are only 2 options:
    # the other one is a descendent of the one you found
    # the other one is on the other side of the tree
    if not root:
        return None
    if root == p or root == q:
        return root

    l = lowestCommonAncestor(root.left, p, q)
    r = lowestCommonAncestor(root.right, p, q)

    if r and l:
        return root
    else:
        return r or l
