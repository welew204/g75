import random
from pprint import pprint


def make_input():
    m = random.randint(1, 10**4)
    n = random.randint(1, 10**4)
    input = [[0 for f in range(n)] for g in range(m)]
    for i in range(m):
        for j in range(n):
            num = random.randint(0, 1)
            input[i][j] = num
    return input


def closest_zero_dry(mat):
    m = len(mat)
    n = len(mat[0])
    output = [[float('inf') for _ in range(m)] for _ in range(n)]
    queue = []
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                output[i][j] = 0
                queue.append((i, j))

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while len(queue) > 0:
        z = queue.pop(0)
        i, j = z
        for dif_r, dif_c in neighbors:
            n_row, n_col = dif_r+i, dif_c+j
            if 0 <= n_row < m and 0 <= n_col < n:
                current_val = output[i][j]
                if output[n_row][n_col] > current_val + 1:
                    output[n_row][n_col] = current_val + 1
                    queue.append((n_row, n_col))
    return output


def find_closest_zero_matrix(input):
    n = len(input[0])
    m = len(input)
    output = [[float('inf') for i in range(n)] for j in range(m)]
    # pprint(output)

    tbd_queue = []
    for i in range(m):
        for j in range(n):
            if input[i][j] == 0:
                tbd_queue.append((i, j))
                output[i][j] = 0

    while len(tbd_queue) > 0:
        z = tbd_queue.pop(0)
        i, j = z
        current_value = output[i][j]
        if j > 0:
            left_neighbor = input[i][j-1]
            if left_neighbor > current_value + 1:
                output[i][j-1] = current_value + 1
                tbd_queue.append((i, j-1))
        elif j+1 < len(output[i]):
            right_neighbor = input[i][j+1]
            if right_neighbor > current_value + 1:
                output[i][j+1] = current_value + 1
                tbd_queue.append((i, j+1))
        elif i > 0:
            upstairs_neighbor = input[i-1][j]
            if upstairs_neighbor > current_value + 1:
                output[i-1][j] = current_value + 1
                tbd_queue.append((i-1, j))
        elif i+1 < len(output):
            downstairs_neighbor = input[i+1][j]
            if downstairs_neighbor > current_value + 1:
                output[i+1][j] = current_value + 1
                tbd_queue.append((i+1, j))

    return output


if __name__ == '__main__':
    inputEZ = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    input = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    output = closest_zero_dry(input)
    pprint(output)
