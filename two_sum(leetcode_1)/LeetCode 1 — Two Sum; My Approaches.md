My working notes on Two sum. written for me, i guess and any other person interested in my repo, not only the code, the insights, what tripped me up and how i got to my solution.

**The problem:** Given an array `nums` and a `target`, return the indices of the two numbers that add up to the target. Exactly one solution exists, and I can't use the same element twice.

This was the first problem where the optimal solution needed a real **insight leap** not just a cleaner  version of the obvious idea. So its worth  documenting properly.

## My scoreboard

| #   | My approach      | Time  | Space | My note                                                |
| --- | ---------------- | ----- | ----- | ------------------------------------------------------ |
| 1   | Brute force      | O(n²) | O(1)  | check every pair — the obvious baseline                |
| 2   | One-pass hashmap | O(n)  | O(n)  | store what I've seen, look up the complement — optimal |

Only two real approaches here(unlike the anagram and even the contains duplicate that had a lot of implementations of one idea). Brute force, and the hashmap. The hashmap is the whole point of this documentation.

---

## How I got the insight (worth remembering)

I solved the brute force version on my own first, then watched NeetCode's **brute force** — and _that's_ where the idea clicked, not his optimal explanation. Something about how he framed the pair-checking made me realize: I'm not really searching for "some other number," I'm searching for one _specific_ number — `target - current`. Once I saw the second number is _determined_ by the first, the "just look up the complement" idea fell out.

Lesson about myself: struggling first, THEN watching, is when explanations actually stick. And the spark for the fast solution was hiding in how the _slow_ one was framed. Keep watching the brute-force explanation even when I already have one.

---

## 1. Brute force — O(n²) time, O(1) space

```python
def two_sum(array: list[int], tg: int):
	if len(array) < 2:
		return
	for i in range(len(array) - 1):
		for j in range(i + 1, len(array)):
			if array[i] + array[j] == tg:
				return i, j
	return
```

**How it works:** Check every possible pair. For each element, compare it against every element after it, looking for a pair that sums to the target. 

**The bounds:** `j` starts at `i+1` so each pair is checked exactly once(comparing #2 and #5 is the same as comparing #5 and #2), and `i` runs to `len - 1`. Same "smart bounds delete redundant checks" move i keep using.

**Why O(n²):** nested loops — for each of n elements, I scan up to n others. Correct, simple, but slow. This is the baseline the hashmap improves on.

---

## 2. One-pass hashmap — O(n) time, O(n) space ← optimal


```python
def two_sum_optimal(array: list[int], tg: int):
	if (len(array) < 2):
		return
	index_map = dict()
	for i in range(len(array)):
		difference = tg - array[i]
		if difference in index_map:
			return i, index_map[difference]
		else:
			index_map[array[i]] = i
	return
```


**The core insight:** I don't need to _search_ the array for the second number. For any number I'm looking at, its partner is forced: `difference = target - current`. So instead of searching (O(n)), I keep a hashmap of numbers I've already seen and ask "have I seen the partner I need?" — which is an **O(1) key lookup**. That reframe — **store-and-lookup instead of search** — is what turns O(n²) into O(n).

**How it works:**

- Map is `value -> index` (the NUMBER is the key, the index is the value).
- For each element: compute its complement. If the complement is already a key in the map, I've found the pair → return the stored index of the complement + the current index.
- If not, add the current number and its index to the map, and keep going.

**Why the map is `value -> index` (a bug I caught):** I first built it `index -> value`, then searched `if difference in index_map.values()`. That's backwards — searching `.values()` is O(n), so I'd built a hashmap and then used it like a list, staying O(n²). The whole magic of a hashmap is that checking the KEYS (`x in my_dict`) is O(1). So the numbers have to be the keys. My backwards map and the `.values()` search were the same bug showing up twice. I actually built the backwards version because i was thinking duplicate keys would hurt.

**Build on the fly, check BEFORE adding:** I don't pre-build the whole map. I check for the complement first, then add the current element. This means the map only ever holds _earlier_ elements when I check — so I never accidentally pair a number with itself.

**Why duplicate keys don't hurt (two reasons):**

1. I only ever need ONE index of any value to form a pair — so if a value repeats and the later index overwrites the earlier one, I've lost nothing; either index forms a valid pair.
2. Check-before-add means I usually return _before_ any overwrite happens — the moment a duplicate's partner is already in the map, I find the pair and exit. Example: `[3, 3], target 6` → at i=1, difference 3 is already in the map from i=0, so I return `(1, 0)` before the second 3 ever overwrites anything.

**The bug I removed — `if array[i] > tg: continue`:** I first added this as an "optimization" (skip numbers bigger than the target). It's WRONG with negatives. For `[10, -6], target 4`: `10 > 4` so I'd skip it, but `10 + (-6) = 4` was the answer. And for a negative target like `-6`, almost every number looks "bigger," so it skips the whole array and returns None. It wasn't even a real speedup (the algorithm is already O(n)) — just added risk for zero benefit. Deleted it.

**Why O(n) time:** one pass; each lookup/insert is O(1) average. **Why O(n) space:** worst case (pair found only at the end), the map holds every element.

---

## What I learned (bigger than this problem)

**1. Store-and-lookup instead of search.** This is THE foundational hashmap pattern, and I'll see it constantly. Contains Duplicate was "have I seen this exact value?" Two Sum is "have I seen the value that _completes_ me?" Same muscle, one level up: turn the thing you're searching for into a key so the lookup is O(1) instead of O(n).

**2. A hashmap is only fast if you search its KEYS.** Searching `.values()` is O(n) — that defeats the entire purpose. If I need to look something up, it has to be a key.

**3. Check-before-add ordering solves the "self-pairing" and duplicate problems for free.** Building the map on the fly isn't just cleaner — it's more correct than pre-building for the duplicate case.

**4. Test with the input that BREAKS it.** The `> tg: continue` bug passed every friendly (all-positive) example and only died on negatives. That's the THIRD time a solution passed the nice inputs but lied on the adversarial ones (naive-duplicate indentation, anagram assumptions, this). My reflex now: throw negatives, zeros, duplicates, and empties at it before trusting it.

---

## The summary I want to be able to say out loud

> "Brute force checks every pair — O(n²). The optimal is a one-pass hashmap: for each number I compute its complement `target - num`, and I keep a map of `value -> index` for everything I've already seen. If the complement is already in the map, I've found the pair and return both indices; otherwise I add the current number and move on. It's O(n) time and O(n) space, and building the map as I go — checking before adding — handles duplicates and stops me pairing a number with itself."
