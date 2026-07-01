nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 3, 5, 6]


def contains_duplicate(array):
    hash_set = set()
    for i in array:
        if i in hash_set:
            return True
        else:
            hash_set.add(i)
    return False


print(contains_duplicate(nums))
