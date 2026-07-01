nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 3, 5, 6]


def contains_duplicate(array):
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] == array[j]:
                return True

    return False


print(contains_duplicate(nums))
