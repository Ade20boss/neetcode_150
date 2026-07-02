nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 3, 5, 6]


def contains_duplicate(array):
    array = sorted(array)
    for i in range(len(array) - 1):
        if array[i] == array[i + 1]:
            return True
    return False


print(contains_duplicate(nums))
