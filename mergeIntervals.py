# https://leetcode.com/problems/merge-intervals/

def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for idx, itv in enumerate(intervals):
        # add element (either by itself or merged with prev)
        if idx == 0:
            res.append(itv)
        elif itv[0] <= res[-1][1]:
            if itv[1] <= res[-1][1]:
                continue
            else:
                res[-1][1] = itv[1]
        else:
            res.append(itv)
    return res


intervals1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
#Output: [[1,6],[8,10],[15,18]]
print(merge(intervals1))

intervals2 = [[1, 4], [4, 5]]
print(merge(intervals2))
#Output: [[1,5]]

intervals3 = [[1, 4], [2, 3]]
print(merge(intervals3))
#Output: [[1,4]]
