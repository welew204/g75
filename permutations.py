def permute(nums):
    # naive: go thru every combination, rule out duplicates
    # DFS algo:
    perms = []

    def dfs(current_perm, option_ints):
        if len(current_perm) == len(nums):
            perms.append(current_perm)
            return

        for o in option_ints:
            next_perm = current_perm + [o]
            upd_options = option_ints.copy()
            upd_options.remove(o)
            dfs(next_perm, upd_options)

    full_list = nums.copy()
    dfs([], full_list)
    return perms


nums = [1, 2, 3]
nums2 = [0, 1]
nums3 = [3, 4, 5, 6, 7]
print(permute(nums3))

"""Example 1:

Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
Example 2:

Input: nums = [0,1]
Output: [[0,1],[1,0]]
Example 3:

Input: nums = [1]
Output: [[1]]"""
