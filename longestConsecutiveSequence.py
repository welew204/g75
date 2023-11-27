import collections


def longestConsecutive(nums):
    arr = set(nums)
    seqs = collections.defaultdict(int)
    for i in arr:
        if i-1 not in arr:
            # checkign for left-neighbor
            seqs[i] += 1
            # init a right-neighbor checkr
            rn = i
            while rn+1 in arr:
                seqs[i] += 1
                rn += 1
    res = max(seqs.values()) if seqs else 0

    return res


def longestConsecutiveWB(nums):
    out = []
    for i, n in enumerate(nums):
        out.append(n)
        if i == 0:
            continue
        else:
            # sort the n into place
            while i > 0 and n < out[i-1]:
                temp = out[i-1]
                out[i-1] = n
                out[i] = temp
                i -= 1
    longestCons = 0  # because the first element will be consecutive w/ self
    tempCons = 0
    for i, n in enumerate(out):
        if i == 0:
            tempCons += 1
            longestCons = tempCons
            continue
        if n == out[i-1] + 1:  # ie, they're consecutive
            tempCons += 1
            longestCons = max(tempCons, longestCons)
        elif tempCons > 1 and n == out[i-1]:
            # identical element, sequence COULD be continued
            continue
        elif tempCons > 1 and n > out[i-1] + 1:
            tempCons = 1

    return longestCons


nums1 = [100, 4, 200, 1, 3, 2]
nums2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
nums3 = [1, 2, 0, 1]

print(longestConsecutive(nums2))
