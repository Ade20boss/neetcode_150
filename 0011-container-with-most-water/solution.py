def most_water(array):
    max_area = 0
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            area = (j - i) * min(array[i], array[j])
            if area > max_area:
                max_area = area
    return max_area


height = [1, 1]
print(most_water(height))


def most_water_ii(array):
    max_area = 0
    left = 0
    right = len(array) - 1
    while left < right:
        area = (right - left) * min(array[left], array[right])
        if area > max_area:
            max_area = area
        if array[left] < array[right]:
            left += 1
        elif array[right] < array[left]:
            right -= 1
        else:
            left += 1
            right -= 1
    return max_area


print(most_water_ii([1, 1]))
