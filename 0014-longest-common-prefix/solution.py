def wrong_long_prefix(strs):
    hash_map = dict()
    min_length = min(len(s) for s in strs)
    prefix = ""
    for i in range(len(strs)):
        for j in range(min_length):
            hash_map[strs[i][j]] = hash_map.get(strs[i][j], 0) + 1
    print(hash_map)
    for i in hash_map:
        if hash_map[i] != len(strs):
            return prefix
        else:
            prefix += i


def long_prefix_1(strs):
    prefix = ""
    min_length = min(len(s) for s in strs)
    for cols in range(min_length):
        for word in strs:
            if word[cols] != strs[0][cols]:
                return prefix
        prefix += word[cols]
    return prefix
