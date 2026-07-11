def group_anagrams_sort(array):
    hash_map = dict()
    for i in array:
        key = "".join(sorted(i))
        if hash_map.get(key, 0) == 0:
            hash_map[key] = [i]
        else:
            hash_map[key].append(i)
    return list(hash_map.values())


def group_anagrams_count(array):
    hash_map = dict()
    for word in array:
        key = [0] * 26
        for char in word:
            key[ord(char) - ord("a")] += 1
        key = tuple(key)
        if hash_map.get(key, 0) == 0:
            hash_map[key] = [word]
        else:
            hash_map[key].append(word)
    return list(hash_map.values())


my_list = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams_count(my_list))
