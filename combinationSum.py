def comboSum(candidates, target):
    combos = []

    def dfs(path, current_sum, current_idx):
        if current_idx == len(candidates):
            return
        current_sum + candidates[current_idx+1]:

    dfs([], 0, 0)


"""
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.
Example 2:

Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
Example 3:

Input: candidates = [2], target = 1
Output: []
"""