# LeetCode 238 — Product of Array Except Self: My Notes

Given `nums`, return an array where `answer[i]` = the product of **every element except
`nums[i]`**. Example: `[1,2,3,4]` → `[24,12,8,6]` (24 = 2·3·4, 12 = 1·3·4, etc.).

**The two constraints that make this a real problem:**

1. Must run in **O(n)** — the naive way is O(n²), and beating that is the whole point.
2. **No division** — the "cheat" (multiply everything, divide by nums[i]) is banned, and it breaks
   on zeros anyway.

---

## Approach 1 — Brute force (my first solution): O(n²)

```python
def p_array(nums):
    new_array = []
    for i in range(len(nums)):
        num = nums[i]
        index = i
        product = 1
        del nums[i]                 # remove this element
        for j in nums:              # multiply all the others
            product *= j
        new_array.append(product)
        nums.insert(index, num)     # put it back
    return new_array
```

For each position, remove that element and multiply everything else. **Correct, but O(n²):** the
outer loop runs n times, and for _each_ one the inner loop multiplies ~n elements. This is a
_real_ n² — the inner loop genuinely re-scans the whole array for every position. (Also `del`
and `insert` are themselves O(n) list operations, making it even slower, and mutating the input
is fragile.) This is the baseline the problem wants me to BEAT.

---

## Approach 2 — Prefix products (the O(n) solution), built from the ground up

This is the part that confused me, so here it is rebuilt slowly, from the smallest idea up.
Read it in order; each step only needs the one before it.

### Step 0 — the one concept everything rests on: a RUNNING TOTAL

Forget the whole problem for a second. Say I have `2, 3, 5` and I want to add them up while
writing my total _as I go_:

```
total = 0
see 2:  total = 0 + 2 = 2
see 3:  total = 2 + 3 = 5
see 5:  total = 5 + 5 = 10
```

I don't re-add from the start each time. When I see the `3`, I just take my total-so-far (2) and
add 3. I **carry the total with me** as I walk. That's a running total.

Now do the exact same thing but _multiplying_ instead of adding — a **running product**. Start at
`1` instead of `0` (multiplying by 1 changes nothing, the way adding 0 does):

```
product = 1
see 2:  product = 1 × 2 = 2
see 3:  product = 2 × 3 = 6
see 5:  product = 6 × 5 = 30
```

That's the whole engine. Everything below is just this, used cleverly.

### Step 1 — the key insight: split "everything else" into LEFT × RIGHT

For any position `i`, the product of all the _other_ elements splits cleanly into two pieces:

> product of everything EXCEPT nums[i] = (product of everything to its LEFT) × (product of
> everything to its RIGHT)

Picture cutting the array at position i:

```
nums = [1, 2, | 3 | 4]
              ↑ cut here (position of the 3)
     LEFT  = 1×2 = 2        RIGHT = 4
     answer for the 3 = LEFT × RIGHT = 2 × 4 = 8   ✓
```

Check another: for the first `1` (position 0), there's nothing to its left, so LEFT = 1 (empty
product), and RIGHT = 2×3×4 = 24, so answer = 1 × 24 = 24. ✓

So: **if I had, for every position, "product of everything to its left" and "product of
everything to its right," I'd just multiply the two.** No division needed. The rest of the
problem is: how do I get those two things cheaply?

### Step 2 — build the LEFT products in ONE pass (this is where the running product comes in)

The naive way to get "product of everything left of position i" would be, for each i, to scan
all the elements before it and multiply — but that re-scans, giving O(n²). Instead I use the
running product from Step 0, with **one rule about ORDER**:

> **Walk left→right. At each position: WRITE DOWN the running product FIRST, THEN multiply the
> current number into it.**

Why "write first, then multiply"? Because if I record the product _before_ folding in the current
element, the recorded value contains everything I've passed _so far but not the current element_
— which is exactly "everything to the left of this position."

Full trace on `[1, 2, 3, 4]` (watch the order: record, then multiply):

```
product = 1                 (nothing to the left of position 0 yet)

position 0:  left[0] = product = 1        ← record FIRST (product of everything left of pos 0 = nothing = 1)
             product = 1 × nums[0] = 1×1 = 1   ← THEN fold in the 1

position 1:  left[1] = product = 1        ← record (everything left of pos 1 = {1})
             product = 1 × nums[1] = 1×2 = 2   ← fold in the 2

position 2:  left[2] = product = 2        ← record (everything left of pos 2 = {1,2})
             product = 2 × nums[2] = 2×3 = 6   ← fold in the 3

position 3:  left[3] = product = 6        ← record (everything left of pos 3 = {1,2,3})
             product = 6 × nums[3] = 6×4 = 24  ← fold in the 4

left = [1, 1, 2, 6]
```

Read `left`: `left[i]` = product of everything strictly to the left of position i. And crucially:
**each step did just ONE multiply**, reusing the running product from the step before. I never
re-scanned. One walk over the array = O(n).

### Step 3 — build the RIGHT products the same way, walking BACKWARD

Identical idea, but I walk right→left and record the running product before folding each element
in. Now the recorded value is "everything to the _right_ of this position."

Trace on `[1, 2, 3, 4]`:

```
product = 1                 (nothing to the right of the last position)

position 3:  right[3] = product = 1       ← record (nothing right of pos 3)
             product = 1 × nums[3] = 1×4 = 4    ← fold in the 4

position 2:  right[2] = product = 4       ← record (everything right of pos 2 = {4})
             product = 4 × nums[2] = 4×3 = 12   ← fold in the 3

position 1:  right[1] = product = 12      ← record (everything right of pos 1 = {3,4})
             product = 12 × nums[1] = 12×2 = 24 ← fold in the 2

position 0:  right[0] = product = 24      ← record (everything right of pos 0 = {2,3,4})
             product = 24 × nums[0] = 24×1 = 24 ← fold in the 1

right = [24, 12, 4, 1]
```

Note `right[i]` sits at position i even though I walked backward — I WRITE IT AT INDEX i (see the
big lesson below on why this matters).

### Step 4 — combine: multiply the two arrays position by position

```
left  = [1,  1,  2,  6]     (everything to the left of each position)
right = [24, 12, 4,  1]     (everything to the right of each position)
answer= [24, 12, 8,  6]     ← answer[i] = left[i] × right[i]
```

Check: answer[2] = left[2] × right[2] = 2 × 4 = 8 = product of everything except the 3. ✓

### Why it's O(n) (not O(n²))

Three passes: build `left` (n steps), build `right` (n steps), combine (n steps). They run **one
after another, NOT nested** — so it's n + n + n = 3n = **O(n)**. Contrast the brute force, which
nests a walk inside a walk (for each position, walk the rest) = n × n = O(n²). Sequential passes
ADD; nested passes MULTIPLY. That's the whole difference.

### The code

```python
def p_array_optimal(nums):
    n = len(nums)
    left = []
    right = [1] * n          # PRE-SIZED so I can write by index (see lesson below)
    output = []

    # LEFT pass: running product, RECORD before multiplying
    product = 1
    for i in range(n):
        left.append(product)     # record first...
        product *= nums[i]       # ...then fold in nums[i]

    # RIGHT pass: same idea, walking right→left
    product = 1
    for i in range(n - 1, -1, -1):
        right[i] = product       # WRITE AT INDEX i (not append!) — see lesson
        product *= nums[i]

    # COMBINE
    for i in range(n):
        output.append(left[i] * right[i])
    return output
```

- **Time: O(n)** — three separate passes (left, right, combine), each n steps. **They are NOT
  nested** — they run one after another: n + n + n = 3n = O(n). (Contrast the brute force, which
  nests a walk inside a walk = n × n = O(n²).)
- **Space: O(n)** — the two helper arrays. (Can be reduced to O(1) extra — see follow-up.)
- **No division** — satisfies the constraint. Handles zeros naturally (a zero on the left makes
  all left-products after it zero, which is correct).

---

## The lesson that cost me the most: append vs indexed assignment

I first tried to store both left and right products in ONE list and combine with an offset. It
kept breaking, and the real reason is subtle and worth remembering:

**The right pass walks right→left, but `append` always adds to the END of the list.** So the
first right-product I append (for the LAST position) landed at the front of the right section,
and the last one (for the FIRST position) landed at the back — the right-products came out
**reversed**. No offset arithmetic can fix a reversal.

**The fix: write by INDEX, not append.** `right[i] = product` puts each value at its correct
position `i`, regardless of which direction I'm walking. That's why `right` is pre-sized with
`[1] * n` — so I can assign into slot `i` directly.

> **Rule to remember: `append` builds in _walk order_. Indexed assignment (`arr[i] = ...`) builds
> in _position order_. When your walk direction differs from the order you need to store in, use
> indexed assignment.**

(Two separate lists also makes the combine trivial — `left[i] * right[i]`, no offset to get
wrong. The single-list-with-offset approach fought the structure the whole way.)

---

## Approach 3 — O(1) extra space (the optimal solution)

The output array doesn't count as "extra" space, so I can drop BOTH helper arrays and use only
the output plus a single variable:

1. **First pass:** write the left-products directly INTO the output array.
2. **Second pass:** walk right→left with a single running `product` variable (the right-product),
   and multiply it straight into `output[i]` — which already holds the left-product. In place,
   `output[i]` becomes `left_product × right_product` = the answer.

```python
def p_space_time_opt(nums):
    n = len(nums)
    output = [1] * n          # PRE-SIZED — indexed assignment needs the slot to exist
    product = 1
    for i in range(n):        # output holds LEFT-products after this loop
        output[i] = product
        product *= nums[i]
    product = 1
    for i in range(n - 1, -1, -1):   # fold RIGHT-products in place
        output[i] *= product
        product *= nums[i]
    return output
```

- **Time O(n), extra space O(1)** (only the output array + one `product` variable; no `left`/`right`
  arrays). This is the best possible.
- **The elegant bit:** the output array does double duty — it holds the left-products, then the
  backward pass multiplies each right-product in place to turn it into the final answer. The whole
  right-product array collapses into one scalar you carry backward.
- **Bug I hit:** started with `output = []` (empty) and did `output[i] = ...` → IndexError.
  Indexed assignment REPLACES an existing slot; it doesn't grow the list. Must pre-size with
  `[1] * n`. (Same lesson as Approach 2's `right` array — `append` grows, `[i]=` requires the slot
  to exist.)

---

## Lessons (bigger than this problem)

1. **Prefix products / running results:** build each entry from the previous one with O(1) work,
   instead of recomputing from scratch. Turns an O(n²) "look at everything before me" into O(n).
   (Seed of dynamic programming; same family as prefix sums.)
2. **Split at each position into "before" × "after"** — a reusable decomposition for array
   problems.
3. **append = walk order, indexed assignment = position order.** Use indexed writes when the walk
   direction and storage order differ.
4. **Sequential passes add (O(n)); nested passes multiply (O(n²)).** Three passes side-by-side is
   still O(n).
5. **Solidify the core before optimizing.** Bank the O(n); do O(1)-space later.

## Say-it-out-loud summary

> "Product of everything except position i = (product of everything left of i) × (product of
> everything right of i). I build a left-products array in one pass with a running product —
> writing the product BEFORE multiplying in the current element, so it excludes that element —
> then a right-products array the same way walking backward, then multiply them position by
> position. Three separate O(n) passes = O(n) total, no division. Key detail: I write the right
> products by index, not append, because the backward walk would otherwise store them reversed."
