import collections


def numIslands(grid):
    islands = 0
    visitd = set()
    rows, cols = len(grid), len(grid[0])

    def bfs(r, c):
        q = collections.deque()
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        q.append((r, c))

        while q:
            isl_r, isl_c = q.popleft()  # remove item from start of queue
            for dr, dc in directions:
                r, c = isl_r+dr, isl_c+dc
                if ((r, c) not in visitd and
                    0 <= r < rows and
                    0 <= c < cols and
                        grid[r][c] == "1"):
                    visitd.add((r, c))
                    q.append((r, c))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visitd:
                bfs(r, c)
                islands += 1

    return islands


test_grid_1 = [
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"]
]
test_grid_2 = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]
print(numIslands(test_grid_1))
print(numIslands(test_grid_2))
