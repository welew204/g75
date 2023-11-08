import collections


def rottingOranges(grid):
    rows, cols = len(grid), len(grid[0])
    minutes = 0
    total_oranges = set()
    rotten_oranges = set()
    to_rot = []
    prev_fresh = 0

    def rot_neighbors(r, c):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        for d in directions:
            dr, dc = r+d[0], c+d[1]
            if (0 <= dr < rows and
                0 <= dc < cols and
                    grid[dr][dc] == 1):
                to_rot.append((dr, dc))

    while True:
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    total_oranges.add((i, j))
                elif grid[i][j] == 2:
                    total_oranges.add((i, j))
                    rotten_oranges.add((i, j))
                    rot_neighbors(i, j)
        for o in to_rot:
            ri, rj = o
            grid[ri][rj] = 2
        to_rot = []
        if len(total_oranges) == len(rotten_oranges):
            return minutes
        elif prev_fresh == len(total_oranges) - len(rotten_oranges):
            # this means no NEW oranges have gotten rotten, and won't be reached on subsequent minutes
            return -1
        else:
            prev_fresh = len(total_oranges) - len(rotten_oranges)
            minutes += 1


test_grid1 = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
test_grid2 = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
test_grid3 = [[0, 2]]

print(rottingOranges(test_grid3))
