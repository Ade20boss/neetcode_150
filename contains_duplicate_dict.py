nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 3, 5, 6]


def contains_duplicate(array):
    hash_dict = dict()
    for i in array:
        if hash_dict.get(i, 0) == 0:
            hash_dict[i] = 1
        else:
            return True
    return False


print(contains_duplicate(nums))
