def comboSum(candidates, target):
    combos = []

    def dfs(path, current_sum, current_idx):
        if current_idx == len(candidates) or current_sum > target:
            return
        elif current_sum == target:
            curr_path = path.copy()
            combos.append(curr_path)
            return
        add_current = candidates[current_idx]
        #next_sum = current_sum + candidates[current_idx+1]
        # this is branching to cases where you take ANOTHER of the current_idz int
        path.append(add_current)
        dfs(path, current_sum+add_current, current_idx)
        # this is stepping back up
        path.pop()
        # this is branching to MOVING on to the next idx, and not considering current idx anymore...
        dfs(path, current_sum, current_idx+1)

    dfs([], 0, 0)
    return combos


candidates1 = [2, 3, 6, 7]
target1 = 7
print(comboSum(candidates1, target1))

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
