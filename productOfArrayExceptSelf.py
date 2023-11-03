def productExceptSelf(nums):
    out = [1 for _ in range(len(nums))]
    # first pass
    snowball1 = 1
    for i, n in enumerate(nums):
        if i == 0:
            out[i] = 1
        else:
            snowball1 *= nums[i-1]
            out[i] = snowball1
    # second pass
    snowball2 = 1
    while i > -1:
        if i == len(nums)-1:  # aka last element
            pass
        else:
            snowball2 *= nums[i+1]
            out[i] *= snowball2
        i -= 1
    return out


test1 = [1, 2, 3, 4]
test2 = [-1, 1, 0, -3, 3]

print(productExceptSelf(test2))
