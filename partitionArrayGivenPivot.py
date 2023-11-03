
def pivotArray(nums, pivot):
    index, p_less, p_more = 0, 0, 0
    while index < len(nums):
        targ = nums[index]
        if targ < pivot:
            if index > p_less:
                nums.insert(p_less, nums.pop(index))
            p_less += 1
            p_more += 1
        elif targ == pivot:
            if index > p_more:
                nums.insert(p_more, nums.pop(index))
            p_more += 1
        # otherwise, targ is greater than pivot, and can stay in place
        index += 1

    return nums


test1 = ([9, 12, 5, 10, 14, 3, 10], 10)
test2 = ([-3, 4, 3, 2], 2)
nums, piv = test1
print(pivotArray(nums, piv))
nums, piv = test2
print(pivotArray(nums, piv))
