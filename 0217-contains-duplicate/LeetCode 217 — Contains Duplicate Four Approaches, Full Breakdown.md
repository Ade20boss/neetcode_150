
**Problem:** given a list of integers, return `True` if any value appears at least twice, `False` if every element is distinct.

This is a study of **the same problem solved in four ways**, my personal note on how i approached it from a naive solution to an optimal solution

Every approach is a different answer to one question: **how do you remember what you've already seen?**

## The scoreboard

|#|Approach|Time|Space|Early exit?|Mutates input?|
|---|---|---|---|---|---|
|1|Naive (nested loop)|O(n²)|O(1)|yes|no|
|2|Sort + adjacent scan|O(n log n)|O(1)*|yes|yes (sorts it)|
|3|Dict|O(n) avg|O(n)|yes|no|
|4|Set (the winner)|O(n) avg|O(n)|yes|no|
* O(1) extra only if you sort **in place** with `.sort()`; `sorted()` builds a new list → O(n).

---

## 1. Naive (brute force) — O(n²) time, O(1) space

```python
def contains_duplicate(array):
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] == array[j]:
                return True
    return False
```

**How it works:** take each element, compare it against every element after it. Any matching pair means a duplicate, return True.

**The optimization (`j` starts at `i + 1`, not 0):**

- Comparing element `#2` with `#5` is the _same check_ as `#5` with `#2`. Doing both is redundant — you'd check every pair twice.

- Starting the inner loop at `i + 1` means each element only looks **forward**. Everything behind `i` was already compared against it earlier. Each pair is checked exactly **once** → half the work.

- Bonus: `j` can never equal `i`, so the old `if j == i: continue` guard becomes impossible to trigger and **disappears**.

- Recurring lesson: **choose smarter loop bounds and a special case vanishes.** (Same move as `range(len - 1)` below)

**Important:** the optimization does **not** change complexity — n²/2 is still O(n²). It's a _cleaner code_ win, not a _complexity_ win


---

## 2. Sort + adjacent scan — O(n log n) time, O(1)* space

```python
def contains_duplicate(array):
    array = sorted(array)
    for i in range(len(array) - 1):
        if array[i] == array[i + 1]:
            return True
    return False
```

**How it works:** Sorting drags equal values next to each other, so a duplicate can only exist as two adjacent elements. One linear pass comparing each element to its neighbor finds it.

**Why O(n log n):** the sort dominates (comparison sorts can't beat n log n). The O(n) scan is smaller and gets absorbed.

**Fencepost detail:** the loop runs `range(len - 1)` so `i + 1` is always valid — no out-of-bounds, no last-element guard. (Smart bounds again.)

**Space nuance (common interview gotcha):**

- `sorted(array)` **creates a new list** → O(n) extra space.
- `array.sort()` sorts **in place** → O(1) extra (O(log n) internals), but _mutates the caller's input_, which may not be allowed.
- So "sort is O(1) space" is only true if in-place sorting is acceptable.

**Use it when:** you can't/won't allocate a hash structure (memory constrained) and mutating/copying the input is fine. Slower than hashing but memory-light.


---

## 3. Dict (hash map) — O(n) time, O(n) space

python

```python
def contains_duplicate(array):
    hash_dict = dict()
    for i in array:
        if hash_dict.get(i, 0) == 0:
            hash_dict[i] = 1
        else:
            return True
    return False
```

**How it works:** walk once, storing every seen value as a **key**. `hash_dict.get(i, 0)` returns 0 when the key is absent (the default), so `== 0` means "new" → record it; anything else means "seen" → duplicate.

**Why O(n) time:** one pass over n elements, each dict lookup/insert **O(1) on average** — that's the whole point of a hash table.

**Why O(n) space:** worst case (all distinct), the dict holds all n values.

**The design flaw (why Set beats this):** look at what you store — `hash_dict[i] = 1`. The value `1` is **never read**. You only check whether the _key_ exists. A dict storing meaningless values purely to track key-presence is **a set wearing a costume**: same O(1) membership, but every entry drags a value you don't use → more memory, noisier code. **When you only care "have I seen this," the right tool is a `set`.**

**Use it when:** you actually need to associate _data_ with each key — counting occurrences, or storing indices. For pure presence, use a set


---

## 4. Set — O(n) time, O(n) space ← the winner

python

```python
def contains_duplicate(array):
    hash_set = set()
    for i in array:
        if i in hash_set:
            return True
        else:
            hash_set.add(i)
    return False
```

**How it works:** identical logic to the dict, but a `set` stores _only_ keys. If the current value is already in the set → duplicate; otherwise add it and continue.

**Why it's best of the four:**

- **O(n) time** — one pass, O(1)-average membership (`i in hash_set`).
- **Early exit** — returns the instant the first duplicate appears.
- **Cleaner + lighter than the dict** — no meaningless values, intent is obvious.

**The one-liner cousin:**

python

```python
return len(nums) != len(set(nums))
```

Dumps the whole list into a set (dropping dups) and compares lengths. Elegant, O(n), what you'd write casually. **But no early exit** — it _always_ builds a set of the entire list, even if a dup sits at index 1. The loop version bails immediately. So on inputs with an early duplicate, the "ugly" loop is _faster_. Genuine engineering point: shortest code isn't always best.

**Use it when:** default answer for "does a duplicate exist." First choice unless memory is tight (then sort) or you need per-key data (then dict).


## The interview-grade summary

> "Brute force is O(n²). I can sort and scan adjacent elements for O(n log n) with O(1) extra space if I sort in place. But the best is a hash set: O(n) time, O(n) space, with early exit on the first duplicate. I'd default to the set; if memory were tight I'd sort in place instead; and if I needed to associate data with each value — like indices for Contains Duplicate II — I'd use a dict rather than a set."
