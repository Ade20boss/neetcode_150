# LeetCode 15 — 3Sum: My Notes

Find **all unique triplets** `[a, b, c]` in the array where `a + b + c == 0`.

```
nums = [-1, 0, 1, 2, -1, -4]  ->  [[-1, -1, 2], [-1, 0, 1]]
```

This is the hardest problem in the **Two Pointers** section, and it's the one where 167 (Two Sum II)
stops being a standalone trick and becomes a _building block_ inside a bigger algorithm.

---

## The distinction that tripped me up: "distinct" means INDICES, not VALUES

I first wrote checks like `nums[i] != nums[j]` to avoid "duplicates." **That was wrong**, and it threw
out valid answers (`[-1,-1,2]`, `[0,0,0]`). Here's the precise picture — there are THREE different
things all wearing the word "duplicate":

| thing                                                             | required? | who handles it              |
| ----------------------------------------------------------------- | --------- | --------------------------- |
| **distinct indices** (can't use one array slot twice)             | YES       | the loop bounds `i < j < k` |
| **unique triplets in the output** (don't report `[-1,0,1]` twice) | YES       | the dedup logic             |
| **distinct values** (the three numbers must differ)               | **NO**    | nobody — it's not required  |

`[-1, -1, 2]` uses two _different_ `-1`s sitting at two _different_ positions. Perfectly legal. What
must be unique is the **triplet in the output**, not the values inside it. I conflated "don't report
the same triplet twice" with "make the values different" — they sound identical and are completely
different. **Lesson: distinct = distinct positions. Equal values at different indices are fine.**

---

## APPROACH 1 — Brute force, from the ground up

### The idea

The most direct reading of the problem: try _every_ group of three positions and keep the ones that
sum to zero. Three nested loops, each starting one past the previous:

```python
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            if nums[i] + nums[j] + nums[k] == 0:
                # found one
```

The `j = i+1`, `k = j+1` staggering does two things at once:

- guarantees **distinct indices** (`i < j < k`, no slot reused), and
- means every combination is tried in exactly **one order** (I never pick the same three positions
  twice), which is the same "each index starts after the one before" idea from the two-pointer layout.

### Why the value-inequality checks were a bug

I added `nums[i] != nums[j] and ...`. That solves a problem I don't have (distinct values aren't
required) and **breaks correct answers**: `[0,0,0]` gets rejected, `[-1,-1,2]` gets rejected. Delete
them — `i < j < k` already gives distinct indices, which is all "distinct" means.

### The real duplicate problem, and the dedup

Brute force finds all correct triplets but produces **repeats of the same triplet in different order**:
`[-1,0,1]` and `[0,1,-1]` are the same triplet. To dedup, canonicalize each triplet and use a set:

```python
key = tuple(sorted((nums[i], nums[j], nums[k])))   # reordered dups become identical
if key not in seen:
    seen.add(key)
    result.append(list(key))
```

`sorted()` makes `[0,1,-1]` and `[-1,0,1]` both become `[-1,0,1]`; `tuple()` makes it hashable so a
set can catch it.

### Complexity — and why it TLEs

- **Time: O(n³)** — three nested loops. On LeetCode's large inputs (a few thousand elements), that's
  billions of operations → **Time Limit Exceeded**. The dedup didn't cause the TLE; the triple loop
  did.
- **Space: O(n)** — the `seen` set.

Brute force is the correct _baseline_ (verify the fast version against it), but it's too slow to submit.
Note the shape: it fixes duplicates **after** generating them — treating the symptom.

---

## APPROACH 2 — Sort + two pointers, from the ground up

### The core insight: 3Sum is 167 in a loop

I want `a + b + c = 0`. **Fix one number** `a = nums[i]`. Then I need `b + c = -a` — which is
**exactly Two Sum II** (find a pair summing to a target in a sorted array) run on the numbers to the
right of `i`. So:

1. **Sort** the array.
2. **Loop** `i` over each number as the fixed `a`.
3. For each `a`, run the **converging two-pointer** on the slice `[i+1 ... end]`, looking for `-a`.

### The pointer layout (this confused me at first)

`left` and `right` do **not** start at the array ends. They search only the slice **to the right of
`i`**:

```
sorted: [-4, -1, -1, 0, 1, 2]
          i   left        right
          ↑   ↑           ↑
       fixed i+1         end
```

- `left = i + 1` (just past the fixed number), moves rightward.
- `right = n - 1` (last index), moves leftward.
- They converge toward each other, each moving **by one**, exactly like 167.

**Why `left = i+1` and not 0** — two reasons:

1. Distinct indices: the fixed number can't pair with itself.
2. **It kills reorder-duplicates by construction.** By only looking rightward of `i`, the fixed
   element is always the _smallest-indexed_ member of the triplet, so each triplet is found exactly
   once (I never find `[-1,0,1]` again later with `0` or `1` as the fixed number). This is why the
   O(n²) version doesn't produce the reorder-duplicates that brute force did.

### The converge (straight from 167)

```python
total = nums[i] + nums[left] + nums[right]
if   total < 0:  left += 1     # too small -> need bigger -> move left up
elif total > 0:  right -= 1    # too big   -> need smaller -> move right down
else:            # found a triplet
```

The rule that **each move only advances ONE pointer** is the whole discipline: when the sum is too
small, `left` points at a number that might still be part of a valid triplet with some _other_ right
value, so I anchor `right` and probe with `left`. Move both and I'd leap over answers.

### Difference from 167: DON'T stop at the first match

167 returned on the first hit (it promised one answer). Here, **one fixed `a` can yield multiple
triplets** — several pairs to its right can sum to `-a`. So after recording a triplet I keep the
`while` going, converging until the pointers meet. I only stop the inner loop when `left` and `right`
cross; _then_ the outer loop advances `i`.

---

## The duplicate-skipping — the part that took the longest

Sorting put equal values **adjacent**, so a duplicate is always the thing sitting _right next to me_.
That turns "have I seen this value?" into "is my neighbor the same as me?" — a cheap neighbor-check,
no set. There are **two** skip points:

### Skip-1: duplicate FIXED number (outer loop)

```python
if i > 0 and nums[i] == nums[i - 1]:
    continue
```

If the value I'm about to fix equals the one I just fixed, its search would regenerate identical
triplets — so skip it. Compare to `nums[i-1]` (the previous fixed value), and the **`i > 0` guard**
prevents `nums[-1]` from wrapping around to the last element at `i == 0` (a bug I hit — it made
`[0,0,0]` return `[]` because `nums[0] == nums[-1]` fired a spurious skip).

### Skip-2: duplicate PAIR values (inner loop, after a match)

When I find a triplet, the values next to `left` and `right` might be copies that would regenerate the
same triplet. So I slide each pointer across its run of equal values:

```python
while left < right and nums[left] == nums[left + 1]:
    left += 1
while left < right and nums[right] == nums[right - 1]:
    right -= 1
left += 1
right -= 1
```

**The two-part motion — this is the key mental model:**

1. **Skip loops** slide each pointer to the _last_ copy in its run of duplicates
   ("while my neighbor is a copy of me, step onto it").
2. **Final `left += 1` / `right -= 1`** steps _off_ the last copy onto the next genuinely new value.

The skip loops carry the pointers _to the edge_ of the duplicate run; the final step carries them
_over_ it. Concretely, on `[-2, 0,0,0, 2,2,2]` with `a = -2`: `left` slides across all three 0s, `right`
across all three 2s, then both step off — so `[-2,0,2]` is appended exactly **once** instead of 9 times.

### The two levels together

- **Skip-1** stops duplicate _fixed numbers_ (don't re-run the whole search on the same `a`).
- **Skip-2** stops duplicate _pairs_ within one search (don't re-append the same triplet).

Both exploit the same fact — **sorting makes equal values adjacent** — so both are neighbor-checks.
Skip-1 looks behind the fixed pointer (`nums[i-1]`); skip-2 looks ahead of the moving pointers
(`nums[left+1]`, `nums[right-1]`). Same idea, three pointers, **zero extra memory**.

### Optimization: break on positive

```python
if nums[i] > 0:
    break
```

Once the fixed number is positive, everything to its right is positive too (sorted), so no triplet can
sum to zero — and every _later_ fixed number is also positive, so **stop entirely** (`break`, not
`continue`). `> 0` not `>= 0`, because `a == 0` is still live (`[0,0,0]`). Also implies: an array with
no negatives has no triplet (except all-zeros), which this break handles for free.

---

## Complexity — the two approaches side by side

|            | Brute force           | Sort + two pointers                      |
| ---------- | --------------------- | ---------------------------------------- |
| time       | **O(n³)**             | **O(n²)** (O(n log n) sort + O(n²) loop) |
| space      | O(n) (the set)        | **O(1)** extra (neighbor-skips, no set)  |
| duplicates | fixed AFTER (symptom) | prevented from forming (root)            |
| LeetCode   | **TLE**               | **accepted**                             |

**Why O(n²):** the outer loop is O(n), and for each fixed number the two-pointer converge is O(n)
(the pointers together traverse the slice once). O(n) × O(n) = O(n²). The sort is O(n log n), which is
dominated. **This is optimal** for 3Sum — you can't do better than O(n²) without more exotic machinery.

### On the set-vs-neighbor-skip choice

My first working O(n²) version used a **set** to dedup (like brute force did). It passed, but it was
O(n) space and fixed duplicates _after_ generating them. The neighbor-skip version is O(1) space and
prevents them from ever forming. **I had the "duplicates are adjacent when sorted" insight early but
reached for the familiar set under the pressure of making it work** — a common pattern: understand the
elegant approach, default to the familiar one. The neighbor-skip is the version 3Sum exists to teach.

---

## The bug history (every one was mechanical, not conceptual)

Building this cold, I hit — and fixed — a chain of bugs, each a known family:

1. **Value-inequality checks** (`nums[i] != nums[j]`) — solved a non-problem, broke valid triplets.
   _Fix: `i<j<k` already gives distinct indices._
2. **Moving both pointers on a miss** — leaps over answers. _Fix: move ONE, chosen by sum sign (167's
   rule)._
3. **Not advancing on a match** — infinite loop (append forever, pointers never move). _The
   trapped-control-flow family from 128 / Valid Palindrome._
4. **`nums[i-1]` wraparound at `i=0`** — `nums[-1]` grabs the last element, spurious skip. _The
   index-past-boundary family. Fix: `i > 0` guard._
5. **Skip loops walking off the end** — no bound, IndexError. _Same boundary family. Fix: `left < right`
   INSIDE the skip condition._
6. **Missing the final step-off / `+= vs -=` sign flip** — hang or crash. _Transcription (the recurring
   one)._

**Not one was a reasoning failure** — all mechanical/boundary slips, each fixed the moment I saw where
it broke. That's the muscle-memory these problems build.

---

## The reusable pattern

**k-Sum reduces to (k-1)-Sum in a loop.** 3Sum = fix one number + 2Sum-on-a-sorted-array. 4Sum = fix
one number + 3Sum. The two-pointer converge is the base case, and duplicate-skipping via
adjacent-neighbor checks (enabled by the sort) is how you keep the output unique with O(1) space. This
exact structure recurs in **18 (4Sum)** and the converging-pointer skeleton continues in **11
(Container With Most Water)** and **42 (Trapping Rain Water)**.

---

## Say-it-out-loud (interview version)

> "Brute force is three nested loops, O(n³), which TLEs. To do better I sort the array, then fix each
> number and run a two-pointer search on the numbers to its right for a pair summing to the negative of
> the fixed number — that's Two Sum II inside a loop, so O(n²). Sorting does double duty: it enables the
> two-pointer direction rule, and it makes equal values adjacent so I can skip duplicates with
> neighbor-checks instead of a set — O(1) extra space. I skip duplicates in two places: the fixed
> number, so I don't re-run the same search, and the two pointers after a match, so I don't report the
> same triplet twice. I also break once the fixed number goes positive, since no positive triple can
> sum to zero."
