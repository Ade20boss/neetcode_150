def three_sum(array):
    sum_list = []
    seen = set()
    result = []
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            for k in range(j + 1, len(array)):
                if array[i] + array[j] + array[k] == 0:
                    sum_list.append([array[i], array[j], array[k]])
    for i in sum_list:
        summed = tuple(sorted(i))
        if summed in seen:
            continue
        else:
            seen.add(summed)
            result.append(list(summed))
    return result


def threeSum(array):
    sum_list = []
    array = sorted(array)
    for i in range(len(array)):
        if array[i] > 0:
            break
        if i > 0 and array[i] == array[i - 1]:
            continue
        left = i + 1
        right = len(array) - 1
        while left < right:
            triplet = [array[i], array[left], array[right]]
            summed = sum(triplet)
            if summed == 0:
                sum_list.append(triplet)

                while left < right and array[left] == array[left + 1]:
                    left += 1
                while left < right and array[right] == array[right - 1]:
                    right -= 1
                left += 1
                right += 1
            elif summed < 0:
                left += 1
            elif summed > 0:
                right -= 1

    return sum_list


nums = [-1, 0, 1, 2, -1, -4]
print(threeSum(nums))
