nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 3, 5, 6]


nums = sorted(nums)


def contains_duplicate(array):
    for i in range(len(array) - 1):
        if array[i] == array[i + 1]:
            return True
    return False


print(contains_duplicate(nums))
