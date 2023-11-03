def levelOrder(root):
    res = []
    pointer = 0
    while pointer < len(root):
        current_level = []
        if pointer == 0:
            current_level.append(root[pointer])
            res.append(current_level)
            pointer += 1  # set the root
            continue
        prev_level_len = len(res[-1])  # the current end of the list of results
        steps_to_look_thru = prev_level_len*2
        for i in range(pointer, pointer+(steps_to_look_thru)):
            if root[i] == None:
                continue
            else:
                current_level.append(root[i])
        res.append(current_level)
        pointer += steps_to_look_thru
    return res


test1 = [3, 9, 20, None, None, 15, 7]
print(levelOrder(test1))
