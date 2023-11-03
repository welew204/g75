def three_sum(nums):
    vals = {}  # {val:index}
    res = []
    for i, a in enumerate(nums):
        if i >= len(nums) - 2:
            break
        j = i+1
        target = 0 - a
        while j < len(nums):
            b = nums[j]
            if (target - b) in vals:
                k = vals[target - b]
                res.append([nums[i], nums[j], nums[k]])
            elif b not in vals:
                vals[b] = j
            j += 1
    return set(res)


def three_sum2(nums):
    # sort first
    nums.sort()
    res = []
    for i, a in enumerate(nums):
        if i > 0 and a == nums[i - 1]:
            continue  # in cases where the new a is same as prev a
        l, r = i + 1, len(nums) - 1
        while l < r:
            threeSum = a + nums[l] + nums[r]
            if threeSum > 0:
                r -= 1
            elif threeSum < 0:
                l += 1
            else:
                res.append([a, nums[l], nums[r]])
                l += 1
                while nums[l] == nums[l-1] and l < r:
                    l += 1
    return res


test1 = [-1, 0, 1, 2, -1, -4]
print(three_sum2(test1))
