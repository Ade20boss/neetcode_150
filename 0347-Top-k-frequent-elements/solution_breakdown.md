# LeetCode 347 — Top K Frequent Elements: My Notes

Return the `k` most frequently occurring elements in an array.
`[1,1,1,2,2,3], k=2` → `[1,2]` (1 appears 3×, 2 appears 2×).

Every approach starts the same way — **count how often each element appears** (a hash map,
element → count). The approaches differ in _how they then select the top k by count._ This
problem is fundamentally about **efficiency**, so the interesting part is the selection step.

---

## My scoreboard

| #   | Approach              | Time     | Space | Note                            |
| --- | --------------------- | -------- | ----- | ------------------------------- |
| 1   | Repeated max + delete | O(n·k)   | O(n)  | find max by count k times       |
| 2   | Bucket sort           | **O(n)** | O(n)  | use the count as an array index |

(Also worth knowing: a **heap** gives O(n log k) via `heapq.nlargest` or
`Counter(array).most_common(k)`.)

---

## 1. Repeated max + delete — O(n·k)

```python
from collections import defaultdict
def k_frequent(array, k):
    hash_map = defaultdict(int)
    res = []
    for i in array:
        hash_map[i] += 1
    for i in range(k):
        key = max(hash_map, key=hash_map.get)   # element with highest count
        res.append(key)
        del hash_map[key]                        # remove so next max is the next-highest
    return res
```

**The key tool: `max(hash_map, key=hash_map.get)`.** This finds the element with the highest
count in ONE pass. The `key=hash_map.get` tells `max` to _compare by count_ (each element's
value in the map) but _return the element itself_ (the key). Without `key=`, `max(hash_map)`
would return the largest _key_, which is wrong — I want the key with the largest _value_.

Then `del hash_map[key]` removes that element so the next iteration's `max` finds the
next-highest. Repeat k times.

**The bug I first had here:** I originally did `list(hash_map.values())` and then looked up
`hash_map[max_count]` — but that treats a _count_ as if it were an _element_. The map is
`element → count`, so indexing it by a count finds nothing (and with `defaultdict`, silently
creates a `0` entry instead of erroring). **Lesson: never drop the link between an element
and its count.** `.values()` throws away which element each count belonged to. Using
`key=hash_map.get` keeps element and count connected.

**Complexity: O(n·k).** Counting is O(n). Then `max` scans all unique elements (up to n) and
I do it k times → O(n·k). Fine for small k, but not optimal — and 347 wants better.

---

## 2. Bucket sort — O(n), the optimal solution

```python
from collections import defaultdict
def bucket_sort(array, k):
    hash_map = defaultdict(int)
    array_length = len(array)
    bucket = []
    res = []
    counter = 0
    for i in range(array_length + 1):        # need indices 0..array_length INCLUSIVE
        bucket.append([])
    for i in array:                          # count frequencies
        hash_map[i] += 1
    for i in hash_map:                       # place each element in bucket[its_count]
        bucket[hash_map[i]].append(i)
    for i in range(array_length, -1, -1):    # walk buckets high freq -> low
        if len(bucket[i]) == 0:
            continue
        for element in bucket[i]:            # collect ELEMENTS in the bucket
            if counter == k:
                return res
            res.append(element)
            counter += 1
    return res
```

**The key insight:** a frequency can be at most `len(array)` (an element can't appear more
times than there are elements). So counts live in a small bounded range `1..len(array)`, which
means I can use **the count itself as an array index.** (Same "the value IS the index" trick
as the 26-slot anagram solution and `ord(c) - ord('a')`.)

**How it works — place, then read:**

1. Make a list of buckets where **index = frequency**, **contents = elements with that
   frequency**. Need `len(array) + 1` buckets (indices 0 to len(array) inclusive).
2. Drop each element into `bucket[its_count]`. Element 1 appears 3× → `bucket[3].append(1)`.
   A bucket holds a _list_ because multiple elements can share a frequency.
3. Walk buckets from highest index (highest frequency) down to 0, collecting elements until I
   have k.

Instead of _sorting_ by frequency (which costs O(n log n)), I _place_ each element at its
frequency-position directly (O(1) each), then read positions in order (O(n)). No comparison
sorting needed — I use frequency as an address.

### The bugs I hit (fencepost family)

- **Buckets too small:** `range(array_length)` gives indices `0..len-1`, but an element that
  appears `len(array)` times needs `bucket[len(array)]` → IndexError. Fix: `range(array_length
    - 1)`. Max frequency is `array_length`, so I need `array_length + 1`slots. (Same fencepost
as Kestrel's`count + 1` activation buffers, the hex-dumper short row.)
- **Walk started too low:** `range(array_length - 1, ...)` never checks the top bucket. Fix:
  start at `array_length`.
- **Appended the bucket instead of its elements:** `res.append(bucket[i])` gives nested lists
  `[[1],[2]]`. Need an inner loop appending each _element_, and checking `counter == k`
  _per element_ (one bucket can hold several tied elements, so counting buckets would be
  wrong).

---

## The complexity insight (the real lesson): nested loops are NOT always O(n²)

I looked at the two nested loops in the bucket walk and thought "isn't this O(n²)?" It's not —
it's **O(n)** — and understanding why is the whole point.

Nested loops are O(n²) only when the inner loop runs ~n times _for each_ outer iteration. Here
it doesn't. The inner loop iterates over the elements _in_ a bucket, and **every element lives
in exactly one bucket.** So summed across the entire outer loop, the inner loop runs `n` times
_total_ — not n×n. The elements are _partitioned_ across the buckets; I visit each exactly once.

Concretely: buckets `[1]`, `[2,7]`, `[3,5,9]` → inner loop runs `1+2+3 = 6` times total, which
is the number of elements, not (buckets × elements).

**The rule to bank: to analyze nested loops, ask "how many times does the inner body run in
TOTAL," not "outer × worst-case-inner."** If the inner loop walks a _partition_ of the data
(each item appears in exactly one inner pass), the total is O(n) regardless of nesting. This
applies to graph adjacency lists, tree traversals, any "distribute into groups then visit all"
pattern.

- True O(n²): the same work repeats every outer step (e.g. brute-force Two Sum re-scans the
  whole array each time).
- This O(n): each element is touched exactly once across the whole nested structure. Nothing
  is re-scanned.

**Total for bucket sort:** build buckets O(n) + count O(n) + place O(n) + nested walk O(n) =
**O(n).** Optimal.

---

## Lessons (bigger than this problem)

1. **`max(iterable, key=func)`** — compare by one thing, return another. Here: compare by
   count, return the element. Broadly useful.
2. **Never separate an element from its metadata.** `.values()` alone loses which element each
   count belongs to. Keep them linked.
3. **Small bounded values can be used as array indices** — the counting/bucket-sort trick.
   Frequency → bucket index. Same family as `ord(c)-'a'` and the 26-slot list.
4. **Nested loops ≠ O(n²).** Sum the total inner executions. A partition-walk is O(n).
5. **Fencepost: max frequency = len(array), so you need len(array)+1 buckets.**

## Say-it-out-loud summary

> "Count frequencies with a hash map. The simple approach is to take the max-by-count k times
> (O(n·k)). The optimal is bucket sort: since a frequency is at most len(array), I make buckets
> indexed by frequency, drop each element into the bucket for its count, then read buckets from
> highest frequency down until I have k. That's O(n) — the nested bucket walk is still O(n)
> because every element sits in exactly one bucket, so the inner loop runs n times total, not
> n²."
