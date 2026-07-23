# LeetCode 11 — Container With Most Water: My Notes

Each number is the height of a vertical line on the x-axis, one unit apart. Pick **two** lines; with
the x-axis they form a container. Find the pair holding the most water.

```
height = [1,8,6,2,5,4,8,3,7]  ->  49
                                  (lines at index 1 and 8: width 7, height min(8,7)=7)
```

```
area = (j - i) * min(height[i], height[j])
        width          height
```

**Width** = distance between the two lines (difference in indices). **Height** = the **shorter** of
the two walls — water spills over the short side, so the container is only as tall as its lowest wall.

Two things that stop me overthinking the setup: the lines **in between don't matter** (the container
is defined purely by the two chosen walls — this isn't a realistic pour), and the lines have **no
width** (infinitely thin).

---

## The tension that makes this a real problem

**Wide pairs** have lots of width but often a short wall dragging the height down. **Narrow pairs**
might have two tall walls but little width. The best answer sits somewhere in that tradeoff, and it's
not at either extreme — so you can't just check the widest pair or the two tallest lines.

---

## APPROACH 1 — Brute force

Try every pair, keep the max.

```python
def most_water_brute(array):
    max_area = 0
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            area = (j - i) * min(array[i], array[j])
            if area > max_area:
                max_area = area
    return max_area
```

`i < j` via the `range(i+1, ...)` bound means every pair is tried exactly once. **O(n²) time, O(1)
space.** Correct, TLEs on LeetCode (n up to 10⁵ → ~10¹⁰ operations).

**Keep this.** It's the reference to verify the optimal version against — see the stress test below.

---

## APPROACH 2 — Converging two pointers (the real solution)

Start with the pointers as **wide as possible** (both ends), then move inward. The whole problem is
deciding **which pointer to move**, and proving it's safe.

### The derivation (this is the actual insight)

**Fact 1: width ALWAYS shrinks.** Both pointers only move inward, so every single move makes the
container narrower. Unavoidable.

**Fact 2: therefore the only way a future pair can beat the current one is by gaining HEIGHT.** It has
to gain enough height to outweigh the width it's guaranteed to lose.

**Fact 3: height = min(the two walls), so only the SHORTER wall caps it.**

Now the decision falls out. Say the walls are 3 and 9:

- **Move the TALLER wall** (9) inward, and suppose it lands on 15. New pair: 3 and 15. Height is
  _still_ `min(3,15) = 3`. **No height gained** — the short wall still caps it — and width was lost.
  This move can only make the area worse or equal. **The taller wall getting taller is irrelevant,
  because it was never the thing limiting you.**
- **Move the SHORTER wall** (3) inward. It might land on something shorter (area worse, fine, keep
  going) — or on something **taller**, in which case the min genuinely rises and the extra height can
  outweigh the lost width. **This is the only move that can ever increase the height.**

> **Rule: always move the pointer at the shorter wall.**

### Why it's SAFE to discard that wall forever (the discard argument)

Moving away from the short wall abandons it permanently. That's justified:

The short wall is _currently_ paired with the **widest possible partner** (the other pointer is as far
away as it can be). Any _other_ partner for it would be closer — so **narrower** — and the height would
still be capped at that short wall **or lower**. So **every remaining pair involving that wall is
provably worse than the one just measured.** Nothing is lost.

> One comparison retires an entire line, with proof. Each line is touched once → **O(n)**.
> Same shape as 167's discard argument ("this value can't be in any valid pair"), different rule.

### The equal-heights case (where my bug was)

When `height[left] == height[right]`, neither is strictly shorter. My first version did
`return max_area` here — **which is wrong**: equal heights doesn't mean you're done, it means neither
wall is strictly shorter. Returning threw away the entire rest of the array. On
`[1,18,7,3,8,8,10,1]` it returned 7; the real answer is 50.

The fix, and the proof: **when both walls are equal, BOTH are provably exhausted.** Run the discard
argument on each independently — say both are 5:

- Keep the left wall: its remaining partners are all inside, so **narrower**, and height is
  `min(5, partner) ≤ 5`. The pair just measured had height 5 at **maximum** width. Every remaining
  pair with it is worse. → discardable.
- Keep the right wall: identical argument. → discardable.

Both satisfy the discard condition, so moving both loses nothing. **The equal case is just the normal
case applied twice** — when neither wall is strictly taller, the capping argument applies to each.

_(Moving only ONE pointer on equal heights is also correct — just one wasted iteration measuring a
provably-worse pair. Moving both is the small optimization.)_

### The general principle behind every branch

> **A line is discardable the moment it's been measured at its maximum possible width while it is the
> thing capping the height.**

Normal case → that's the shorter wall. Equal case → that's both. One principle, every branch.

---

## The solution

```python
def most_water(array):
    max_area = 0
    left = 0
    right = len(array) - 1
    while left < right:
        area = (right - left) * min(array[left], array[right])
        if area > max_area:
            max_area = area

        if array[left] < array[right]:
            left += 1               # left is shorter -> discard it
        elif array[right] < array[left]:
            right -= 1              # right is shorter -> discard it
        else:
            left += 1               # equal: BOTH exhausted -> discard both
            right -= 1
    return max_area
```

_(The three branches can be collapsed to two — since equal lets you move either pointer, the equal
case can just fall into one side's `else`. Fewer branches, one less special case to get wrong.)_

---

## Complexity

|          | Brute force | Two pointers                      |
| -------- | ----------- | --------------------------------- |
| time     | O(n²)       | **O(n)** — each line retired once |
| space    | O(1)        | **O(1)** — two indices            |
| LeetCode | TLE         | accepted                          |

**This is optimal.** O(n) is the floor (you must look at the lines), O(1) space is the floor.

---

## The bug, and the lesson

My `<` and `>` branches were right in the first draft — those I'd reasoned out carefully. **The `else`
was the afterthought, and it was the one that broke.** It only fires on exactly-equal heights, which
the hand-picked examples (`[1,8,6,2,5,4,8,3,7]`, `[1,1]`, `[4,3,2,1,4]`) never triggered in a way that
mattered — all of them passed. Only random testing caught it: **37/2000 wrong.**

> **Lesson: the case you think is trivial is where the bug hides, because it's the one you didn't
> reason about.** Same shape as 3Sum's `i > 0` guard — a boundary case that felt like a formality.

**And this is why the brute force stays.** The two-pointer solution is short enough to _look_ obviously
right while the pointer logic is subtly wrong. Verifying against brute force on random inputs is what
actually proves it — weighting the random heights toward **small ranges** (0–1, 0–2, 0–3) so equal-height
collisions happen constantly, exactly where the bug lived. Final: **0 wrong in 5000 random cases**
plus 300 larger arrays.

---

## The reusable pattern

**Converging pointers from both ends, where the move is decided by a property of the current pair, and
each move retires a candidate with proof.** Same skeleton as 167 and 15 — only the decision rule
changes:

| problem            | decision rule             | what gets discarded                                |
| ------------------ | ------------------------- | -------------------------------------------------- |
| **167** Two Sum II | sum vs target             | the value that can't be in any valid pair          |
| **15** 3Sum        | sum vs target (in a loop) | same, plus duplicate values                        |
| **11** this one    | which wall is shorter     | the wall already at max width while capping height |

Next: **42 (Trapping Rain Water)** — looks like this problem but isn't. Instead of two walls forming
one container, you compute water trapped at _every_ position.

---

## Say-it-out-loud (interview version)

> "Brute force is every pair, O(n²). For O(n) I put a pointer at each end and move inward. The key
> observation is that width always shrinks on every move, so the only way to improve is to gain height
> — and height is capped by the shorter wall. Moving the taller wall can never raise the height, since
> the short one still caps it, and it always loses width, so that move can't help. So I always move the
> shorter wall. That's safe because the shorter wall is currently paired with its widest possible
> partner, so every remaining pair involving it would be narrower with the height still capped at or
> below that wall — provably worse. When both walls are equal, that argument applies to both, so I
> discard both. O(n) time, O(1) space."
