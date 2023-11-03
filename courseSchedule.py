from collections import defaultdict

# Neetcode solve:


def canFinish(numCourses, prerequisites) -> bool:
    catalog = {i: [] for i in range(numCourses)}

    for crs, pre in prerequisites:
        catalog[crs].append(pre)

    visitSet = set()

    def dfs(crs):
        if crs in visitSet:
            return False
        if catalog[crs] == []:
            return True

        visitSet.add(crs)
        for p in catalog[crs]:
            if not dfs(p):
                # meaning: if dfs fails for any prereq (bc it's in visitset), then the whole fnc returns False
                return False

        # bc we're done visiting this node on THIS search (to detect for circularity in this graph)
        visitSet.remove(crs)
        catalog[crs] = []  # to save O() on future dfs
        return True

    for n in range(numCourses):
        if not dfs(n):
            return False

    return True


"""def canFinish(numCourses, prerequisites) -> bool:
    courses_taken = set()
    catalog = defaultdict(list)
    for p in prerequisites:
        course, prereq = p
        if course == prereq:
            return False  # indicates circular dependency
        elif prereq not in catalog:
            catalog[prereq]
        if course not in catalog:
            catalog[course].append(prereq)
    while True:

    return True if courses_taken <= numCourses else False"""


test1 = [[1, 0]]
test2 = [[1, 0], [0, 1]]
test3 = []
test4 = [[2, 0], [2, 1]]
test5 = [[0, 10], [3, 18], [5, 5], [6, 11],
         [11, 14], [13, 1], [15, 1], [17, 4]]
test6 = [[1, 0], [0, 2], [2, 1]]

print(canFinish(20, test5))
print(canFinish(3, test6))
print(canFinish(3, test4))
print(canFinish(3, test1))
print(canFinish(2, test2))
print(canFinish(2, test1))
print(canFinish(1, test3))
