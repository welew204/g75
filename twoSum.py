def twoSum(nums, target):
    # first, go thru and add every item to dict, w/ ind
    # then, second pass check for diff
    vals = {}
    for i, v in enumerate(nums):
        if v in vals:
            continue
        vals[v] = i
    for j, r in enumerate(nums):
        diff = target - r
        if diff in vals and j != vals[diff]:
            return [j, vals[diff]]
    # still O(n) because it's 2n passes, with constant-time calls to the dict


def twoSumII(nums, target):
    # where I need to return the values and can trash the og indices
    # nums.sort()
    l, r = 0, len(nums)-1
    while l < r:
        chkr = nums[l] + nums[r]
        if chkr == target:
            return [l+1, r+1]
        elif chkr < target:
            l += 1
            while nums[l] == nums[l+1] and l+1 < r:
                l += 1
        elif chkr > target:
            r -= 1


test2 = [3, 2, 4]

#print(twoSum(test2, 6))

twoSumIItest = [0, 0, 3, 4]
twoSumIItest2 = [1, 2, 3, 4, 4, 9, 56, 90]

print(twoSumII(twoSumIItest2, 8))
