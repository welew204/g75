def searchRotArray(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l+r)//2  # get average
        if nums[mid] == target:
            # DING got the right index
            return mid
        # checking LEFT (aka UNSORTED) side
        if nums[l] <= nums[mid]:
            if target > nums[mid] or target < nums[l]:
                # target must be in right side
                l = mid + 1
            else:
                # target must be in left side
                r = mid - 1
        # checking RIGHT side
        else:
            if target < nums[mid] or target > nums[r]:
                # target must be in left side
                r = mid - 1
            else:
                # target must be in right side
                l = mid + 1
    return -1


""" MY EXTRANEOUS solution that was trying to handle specific cases of Lf piv/unpiv and Rt piv/unpiv
        if nums[l] < nums[r]:
            # UNROTATED
            if target < nums[mid]:
                # left side
                r = mid
                continue
            else:
                # right side
                l = mid+1
                continue
        elif nums[l] > nums[mid]:
            # pivot is in LEFT side
            if (target < nums[r] and target > nums[mid]):
                # target is in RIGHT
                l = mid+1
                continue
            elif (target < nums[mid] or target > nums[l]):
                # target is in LEFT
                r = mid
                continue
            else:
                # target IS NOT in the window where it should be
                return -1
        elif nums[l] <= nums[mid]:
            # pivot is in RIGHT side
            if (target > nums[l] and target < nums[mid]):
                # target is in LEFT
                r = mid
                continue
            elif (target > nums[mid] or target < nums[r]):
                # target is in RIGHT
                l = mid+1
                continue
            else:
                # target IS NOT in the window where it should be
                return -1
        else:
            return -1
    return -1
 """

# test inputs
nums1 = [4, 5, 6, 7, 0, 1, 2]
target1 = 0
#Output: 4
print(searchRotArray(nums1, target1))

nums2 = [4, 5, 6, 7, 0, 1, 2]
target2 = 3
#Output2: -1
print(searchRotArray(nums2, target2))

nums3 = [1]
target3 = 0
#Output3: -1
print(searchRotArray(nums3, target3))

nums4 = [6, 7, 0, 1, 2, 4, 5]
target4 = 3
#Output3: -1
print(searchRotArray(nums4, target4))

nums5 = [1]
target5 = 1
#ouput5: 0
print(searchRotArray(nums5, target5))

nums6 = [3, 1]
target6 = 1
#ouput5: 0
print(searchRotArray(nums6, target6))
