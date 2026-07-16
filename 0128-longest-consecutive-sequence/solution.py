def lcs(array):
    sequences = []
    for i in array:
        if len(sequences) == 0:
            sequences.append([i])
            continue
        j = 0
        added = False
        while j < len(sequences):
            if i == sequences[j][-1] + 1:
                sequences[j].append(i)
                added = True
            j += 1
        if not added:
            sequences.append([i])

    return max(sequences, key=len)


def lcs_set(array):
    num_set = set(array)
    count = 0
    for i in num_set:
        if i - 1 in num_set:
            continue
        current_count = 1
        while i + 1 in num_set:
            current_count += 1
            i += 1
        if current_count > count:
            count = current_count
    return count


print(lcs_set([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
