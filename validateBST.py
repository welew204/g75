# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def isValidBST(root) -> bool:
    boundaries = [float('-inf'), float('inf')]

    def testSubtree(node, boundaries):
        if not node:
            # found leaf
            return True
        elif node.val <= boundaries[0] or node.val >= boundaries[1]:
            return False
        return (testSubtree(node.left, [boundaries[0], node.val]) and testSubtree(node.right, [node.val, boundaries[1]]))

    return testSubtree(root, boundaries)
