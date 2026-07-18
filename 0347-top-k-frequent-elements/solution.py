from collections import defaultdict


def k_frequent(array, k):
    hash_map = defaultdict(int)
    res = []
    for i in array:
        hash_map[i] += 1
    for i in range(k):
        key = max(hash_map, key=hash_map.get)
        res.append(key)
        del hash_map[key]
    return res


def bucket_sort(array, k):
    hash_map = defaultdict(int)
    array_length = len(array)
    if k > array_length:
        return None
    bucket = []
    res = []
    counter = 0
    for i in range(array_length + 1):
        bucket.append([])
    for i in array:
        hash_map[i] += 1
    if k > len(hash_map):
        return None
    for i in hash_map:
        bucket[hash_map[i]].append(i)
    for i in range(array_length, -1, -1):
        if len(bucket[i]) == 0:
            continue
        for element in bucket[i]:
            if counter == k:
                return res
            res.append(element)
            counter += 1
    return res


nums = [1, 1, 1, 2, 2, 3]
k = 7
print(bucket_sort(nums, 2))
