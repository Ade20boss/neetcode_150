def two_sum(array: list[int], tg: int):
    if len(array) < 2:
        return
    for i in range(len(array) - 1):
        for j in range(i + 1, len(array)):
            if array[i] + array[j] == tg:
                return i, j
    return


def optimal_attempt(array: list[int], tg: int):
    if len(array) < 2:
        return
    index_map = dict()  # value, index
    for i in range(len(array)):
        difference = tg - array[i]
        if difference in index_map:
            return i, index_map[difference]
        else:
            index_map[array[i]] = i
    return
