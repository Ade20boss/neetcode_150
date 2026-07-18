def p_array(nums):
    new_array = []
    for i in range(len(nums)):
        num = nums[i]
        index = i
        product = 1
        del nums[i]
        for j in nums:
            product *= j
        new_array.append(product)
        nums.insert(index, num)
    return new_array


def p_array_optimal(nums):
    n = len(nums)
    left = []
    right = [1] * n
    output = []

    product = 1
    for i in range(n):
        left.append(product)
        product *= nums[i]

    product = 1
    for i in range(n - 1, -1, -1):
        right[i] = product
        product *= nums[i]

    for i in range(n):
        output.append(left[i] * right[i])
    return output


def p_space_time_opt(nums):
    n = len(nums)
    output = [1] * n

    product = 1
    for i in range(n):
        output[i] = product
        product *= nums[i]

    product = 1
    for i in range(n - 1, -1, -1):
        output[i] *= product
        product *= nums[i]
    return output


nums = [-1, 1, 0, -3, 3]
print(p_array_optimal(nums))
