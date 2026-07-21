# LeetCode 167 — Two Sum II: My Notes

Sorted, 1-indexed array. Find the two numbers that sum to `target`, return their 1-based positions.
Exactly one solution. **Must use O(1) extra space.**

```
numbers = [2, 7, 11, 15], target = 9  ->  [1, 2]   (2 + 7 = 9)
```

This is the second problem in **Two Pointers**, and it's the one that teaches why **sorted input is a
superpower**.

---

## The two things that decide the whole approach

**1. The constraint rules OUT the hash map.** The Two Sum I trick — a hash map of "value → index,"
checking for `target - num` as you go — would give the right answer here too. But it costs **O(n)
extra space**, and this problem explicitly requires **O(1)**. So the map is disqualified by fiat.

**2. The sorted input makes the map UNNECESSARY anyway.** This is the deeper half, and the part that
transfers. In Two Sum I the array was _unsorted_, so I had no idea which direction to search — the hash
map bought O(1) lookups to compensate for that blindness. Here, **sorted gives me direction for free.**
I don't need the map's lookups because the order tells me which way to move.

> So it's not that I'm _settling_ for two pointers because the map is banned. Two pointers is the
> genuinely _better_ tool once the array is sorted. **The constraint rules out the map; the sorted
> input makes the map pointless.** Same conclusion from two directions.

---

## The approach — two pointers, converge from both ends

```python
def two_sum_ii(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return left + 1, right + 1      # +1 each: 1-INDEXED
        elif s < target:
            left += 1
        else:
            right -= 1
    return None
```

`left` starts on the smallest value, `right` on the largest. Look at the sum and let the sorted order
decide the move:

```
sum too BIG    -> I need it smaller -> move right DOWN (toward smaller values)
sum too SMALL  -> I need it bigger  -> move left  UP   (toward larger values)
sum == target  -> done
```

### Why this is O(n) and not O(n²) — the discard argument

The key insight, and the reason the nested loop disappears: **each move rules out a value permanently.**

Say the sum is too big, so I move `right` down. What did I just learn? `numbers[right]` was too big
_even paired with the smallest available number_ (`numbers[left]`). Every _other_ remaining partner is
`>= numbers[left]`, so pairing `numbers[right]` with any of them would be **even bigger** — all still
too big. So `numbers[right]` can't be part of _any_ valid pair. **One comparison eliminates a whole
row.** Symmetric argument when the sum is too small and I move `left` up.

That's why I never need to re-examine a value: every step throws one away for good. n values, one pass,
**O(n)**.

---

## The gotchas

**1-INDEXED.** The problem wants positions starting at 1, so the answer is `left + 1, right + 1`, not
`left, right`. Reading the return spec carefully is half the problem.

**`while left < right`, not `while True`.** My first version used `while True`, which works _only_
because the problem guarantees a solution — the `== target` return always fires before the pointers
cross. But that safety comes from the problem's promise, not my code. `while left < right` encodes the
real stopping rule (stop when the pointers meet) in the loop itself, so the function stays correct even
on an input with no valid pair (it returns None instead of crashing or looping forever).

> **Lesson: let the loop condition encode the stopping rule, rather than trusting an external
> guarantee and looping forever.** `while left < right` says something true about the algorithm;
> `while True` says "I trust the input."

**The `else: return None` after the loop is unreachable here** (a solution is guaranteed), but it makes
the function _total_ — every path returns something — which is the safer, production shape.

---

## Complexity

|       | Two Sum I (unsorted)               | Two Sum II (sorted)                  |
| ----- | ---------------------------------- | ------------------------------------ |
| tool  | hash map                           | two pointers                         |
| time  | O(n)                               | O(n)                                 |
| space | **O(n)** (the map)                 | **O(1)** (two indices)               |
| why   | unsorted -> need map for direction | sorted -> order gives direction free |

**This is optimal.** O(n) time is the floor — you must look at values to find the pair. O(1) space is
the floor — two integer pointers, no structure. Sitting on both.

---

## The reusable pattern

**Sorted array + find-a-pair-by-value = two pointers from both ends, moved by comparing the sum to the
target.** The discard argument (each move eliminates a value that can't be in any answer) is what makes
it linear. This exact move recurs in **15 (3Sum)** — which is this, wrapped in a loop — and **11
(Container With Most Water)** and **42 (Trapping Rain Water)**, where the _decision rule_ changes but
the converging-pointers skeleton is identical.

---

## Say-it-out-loud (interview version)

> "The array's sorted and I'm told to use constant space, so a hash map is out — but sorted input means
> I don't need one. I put one pointer at each end and look at the sum. If it's too big I move the right
> pointer down to shrink it; if it's too small I move the left pointer up to grow it; if it equals the
> target I'm done. Each move is safe because sorted order proves the value I'm leaving can't be in any
> valid pair — so it's one linear pass, O(n) time and O(1) space. I return the positions plus one
> because the problem is 1-indexed."
