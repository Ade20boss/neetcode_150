"""
LeetCode 167 — Two Sum II (Input Array Is Sorted)

Given a 1-INDEXED array `numbers` that is already sorted in non-decreasing order,
find two numbers that add up to `target`. Return their 1-based positions.

    numbers = [2, 7, 11, 15], target = 9  ->  [1, 2]   (2 + 7 = 9)

Constraints that decide the approach:
  - Exactly one solution exists.
  - **Must use only O(1) constant extra space.**  <- this rules out the hash map.
  - The array is SORTED.                          <- this makes two pointers possible.
"""


# ---------------------------------------------------------------------------
# APPROACH — two pointers, converge from both ends (OPTIMAL: O(n) / O(1))
# ---------------------------------------------------------------------------
# left starts at the smallest value, right at the largest. The sorted order
# gives a free decision rule:
#   sum too big   -> shrink it -> move right DOWN (toward smaller values)
#   sum too small -> grow it   -> move left  UP   (toward larger values)
#   sum == target -> done
def two_sum_ii(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return left + 1, right + 1  # +1 each: the problem is 1-INDEXED
        elif s < target:
            left += 1
        else:
            right -= 1
    return None  # unreachable given the guarantee,
    # but keeps the function total/safe


if __name__ == "__main__":
    tests = [
        ([2, 7, 11, 15], 9, (1, 2)),
        ([2, 3, 4], 6, (1, 3)),
        ([-1, 0], -1, (1, 2)),
        ([1, 2, 3, 4, 4, 9, 56, 90], 8, (4, 5)),
        ([5, 25, 75], 100, (2, 3)),
    ]
    for nums, tgt, expected in tests:
        got = two_sum_ii(nums, tgt)
        mark = "OK  " if got == expected else "FAIL"
        print(f"[{mark}] {got} exp {expected}   {nums} target {tgt}")
