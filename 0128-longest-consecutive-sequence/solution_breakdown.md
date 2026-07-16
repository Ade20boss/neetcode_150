# LeetCode 128 — Longest Consecutive Sequence: My Notes

Given an unsorted array of integers, return the **length** of the longest run of consecutive
numbers. Example: `[100, 4, 200, 1, 3, 2]` → `4`, because `1, 2, 3, 4` are all present.

**Two things to pin down before writing any code** (both cost me time when I got them wrong):

1. **Order in the input does not matter.** The array is a _bag of numbers_, not a sequence. In
   `[100, 4, 200, 1, 3, 2]`, the answer 1,2,3,4 is scattered all over the input. This sounds
   obvious and I still wrote two solutions that quietly assumed otherwise.
2. **Return the LENGTH, not the sequence.** I returned the list on my first attempt.

**The constraint that IS the problem:** must run in **O(n)**. The obvious approaches are all
O(n²) or O(n log n). Everything interesting about this problem lives in that constraint.

---

## Approach 1 — build the sequences physically (BROKEN)

My first instinct: keep a list of running sequences. For each number, try to tack it onto the end
of an existing sequence. If it doesn't fit anywhere, start a new sequence.

```python
def lcs(array):
    sequences = []
    for i in array:
        if len(sequences) == 0:
            sequences.append([i])
            continue
        j = 0
        added = False
        while j < len(sequences):
            if i == sequences[j][-1] + 1:      # does i extend this sequence?
                sequences[j].append(i)
                added = True
            j += 1
        if not added:
            sequences.append([i])              # nope — start a new one
    return max(sequences, key=len)
```

I ran it. **Every single test failed:**

```
input=[100, 4, 200, 1, 3, 2]        returned: [1, 2]     expected length: 4
input=[1, 3, 2]                     returned: [1, 2]     expected length: 3
input=[3, 2, 1]                     returned: [3]        expected length: 3
input=[0,3,7,2,5,8,4,6,0,1]         returned: [0, 1]     expected length: 9
input=[1, 2, 0, 1]                  returned: [1, 2]     expected length: 3
```

### Bug 1 — returns the list, not the length

`max(sequences, key=len)` gives me the longest _sequence_, not its length. Easy fix, but worth
noting: `key=len` is exactly the keyword-only `key` parameter I'd learned about in Goodrich an
hour earlier. It compares by `len(...)` but returns the original item — which is precisely why I
got a list back instead of a number.

### Bug 2 — it can only ever extend FORWARD

`[3, 2, 1]` → `[[3], [2], [1]]`, answer 1. Trace it:

```
i=3:  sequences empty            -> [[3]]
i=2:  is 2 == sequences[0][-1] + 1?   is 2 == 3+1 = 4?   NO   -> [[3], [2]]
i=1:  is 1 == 3+1 = 4?  NO
      is 1 == 2+1 = 3?  NO                                    -> [[3], [2], [1]]
```

A perfectly good 3-long chain, shattered into three fragments. The only test I wrote was
`i == sequences[j][-1] + 1` — "does this number come _after_ the last element?" **There is
nothing in the code that can put a number at the FRONT of a sequence.** Descending input
destroys it completely.

### Bug 3 — it cannot MERGE (this is the nastier one)

`[1, 3, 2]` → `[[1,2], [3]]`, answer 2. Trace:

```
i=1:  -> [[1]]
i=3:  is 3 == 1+1 = 2?  NO      -> [[1], [3]]
i=2:  is 2 == 1+1 = 2?  YES     -> [[1,2], [3]]
```

Look at what just happened. `2` is the **bridge** between `[1]` and `[3]`. It should have fused
them into `[1,2,3]`. Instead I have two fragments sitting side by side that _together_ are the
answer, and my code has no concept of joining them.

This bug is worse than bug 2 because **fixing bug 2 doesn't fix this one.** Even with
front-extension working, a number can arrive and connect two _existing_ sequences, and appending
to one of them still doesn't merge them.

### Bug 4 — it's O(n²) anyway

The inner `while` scans **every sequence** for **every element**. That's n × (number of
sequences), which in the worst case is n × n. And I'd need to bolt merging logic _on top_ of
that. It's getting slower and more complicated at the same time.

### The real lesson from Approach 1

Every fix revealed another bug. That's a signal — not that my code was buggy, but that **the
whole idea was wrong.**

I was trying to **construct** the sequences: physically build the lists, grow them, merge them.
But the problem doesn't ask for the sequences. **It asks for a length.** All that list-building
machinery is work I'm doing for an answer I'm going to throw away.

> **The pivot: do I need to build the sequences at all?**

If I had a magic O(1) "is the number `x` present?" — what could I do without ever constructing a
single list?

That's a **set**.

---

## Approach 2 — set + counter (BROKEN, but the set was right)

```python
def lcs_set(array):
    num_set = set(array)
    count = 0
    for i in array:
        if i + 1 in num_set:
            count += 1
        else:
            count = 0
    return count
```

Results:

```
input=[1, 2, 3, 4]                  returned: 0      expected: 4     <-- !!!
input=[100, 4, 200, 1, 3, 2]        returned: 3      expected: 4
input=[1, 3, 2]                     returned: 1      expected: 3
input=[3, 2, 1]                     returned: 2      expected: 3
input=[0,3,7,2,5,8,4,6,0,1]         returned: 4      expected: 9
input=[10, 20, 30]                  returned: 0      expected: 1
```

**`[1,2,3,4]` returns 0.** The most perfect input imaginable, the worst possible answer. That's
the smoking gun.

```
i=1:  2 in set?  yes  -> count = 1
i=2:  3 in set?  yes  -> count = 2
i=3:  4 in set?  yes  -> count = 3
i=4:  5 in set?  NO   -> count = 0     <-- built it up, then wiped it
```

I reset the counter to zero right after building it correctly, then the loop ended and I returned
the wreckage.

But **the reset is a symptom, not the disease.** The actual problem:

> **My loop walks the ARRAY. The array's order is arbitrary.**

Look at `[100, 4, 200, 1, 3, 2]` → 3. The counter went: 100 (no), 4 (no), 200 (no), 1 (yes),
3 (yes), 2 (yes) → 3. But `1`, `3`, `2` **aren't a chain** — they're three unrelated numbers that
each happened to have a successor _somewhere_ in the set. My count was tallying:

> "how many numbers _in a row in the input array_ have a successor somewhere"

That is a **meaningless quantity**. It has nothing to do with consecutive sequences at all.

### Where the bad instinct came from

I imported the **counter-with-reset** pattern from problems where array order _means_ something
(longest run of X, max subarray, etc.). Here it doesn't. The array is a bag.

> **Lesson: before reaching for a pattern, ask whether the structure the pattern relies on is
> actually present.** Counter-with-reset relies on adjacency in the input meaning something.

The set was right. Using it to answer "does this have a successor?" while marching through
arbitrary array order was not.

---

## Approach 3 — hopping by position (BROKEN, and it CRASHED)

Right realisation (stop scanning, start _hopping_), wrong execution:

```python
def lcs_set(array):
    num_set = set(array)
    count = 0
    i = 0
    while True:
        current_pos = i
        next_item = array[current_pos] + 1
        if next_item in num_set:
            count += 1
            next_pos = array.index(next_item, current_pos)   # where does it live?
            i += (next_pos - current_pos)
        else:
            return count
```

Results:

```
input=[1, 2, 3, 4]              returned: 3      expected: 4
input=[100, 4, 200, 1, 3, 2]    returned: 0      expected: 4
input=[1, 3, 2]                 CRASHED: ValueError: 3 is not in list
input=[3, 2, 1]                 returned: 0      expected: 3
```

### The crash is the most useful thing here

`ValueError: 3 is not in list` — but 3 **is** in the list, at index 1. I called
`array.index(3, current_pos)` with `current_pos = 2`, so it searched **forward from position 2**
and never looked back. The number is there; it's just _behind_ me.

> **That crash means: I'm still navigating by array POSITION, and array positions are meaningless
> here.** The chain 1→2→3 has nothing to do with where those numbers sit in the input. I built a
> hopping mechanism that hops through _positions_, when the chain lives in _values_.

### Bug: `array.index()` is a linear scan

I built a set to get O(1) lookups... then threw that away by asking the _array_ where things live.
Every hop is O(n). The set is doing nothing for me.

### Bug: only ever starts at `array[0]`

`[3, 2, 1]` → 0. Started at `3`, found no `4`, gave up. Never tried `1`. Same for
`[100, 4, 200, 1, 3, 2]` → 0: started at 100, no 101, returned immediately.

### Bug: off-by-one (edges vs nodes)

`[1,2,3,4]` → 3. I count a hop each time I find a successor: 1→2, 2→3, 3→4 = **three hops**. But
there are **four numbers**. I'm counting **edges, not nodes**. (Fencepost — same family as
Kestrel's `count` vs `count + 1` for the `inputs` array.)

### The realisation that unlocks everything

> **After `num_set = set(array)`, why do I need the array at all?**

I have `1` and I want to walk the chain. I ask "is 2 in the set?" Yes. Now I want 3. Do I need to
know _where_ 2 lives in the array? **No — I already know its value.** It's `1 + 1`. The next is
`1 + 2`. **The whole chain is generated from the starting value alone.** The set only ever
answers yes/no.

**Walk by VALUE, not by POSITION.** The array is dead weight once the set exists.

---

## The second insight: which numbers deserve to be starting points?

Walking by value fixes navigation. But if I walk from **every** number, that's an O(n) walk done
n times = **O(n²)**. Still fails the constraint.

So: which numbers are worth starting from?

**My first guess: "start from the lowest number in the set."** Wrong — test it:

```
[10, 11, 12, 1, 2]
```

Lowest is `1`. Walk: 1→2, no 3. Length 2. But `10, 11, 12` is right there with length 3. **There
can be MANY separate chains, each with its own start.** The global minimum only gives me the start
of _one_ of them.

**Second guess: "a number starts a chain if `i + 1` is in the set."** Also wrong. Is `11 + 1 = 12`
in the set? Yes — so `11` would be a "start." But it's sitting in the _middle_ of 10→11→12. That
rule says _"there's something after me,"_ which is true of almost every number in a chain. It
doesn't separate starts from middles at all.

I was **looking in the wrong direction.**

**The answer:** what makes `10` and `1` chain-starts, and `11`, `12`, `2` not?

> **A number starts a chain if and only if there is NOTHING in the set one below it.**
> `i - 1 not in num_set`

- `10` → is `9` in the set? No → **start**
- `11` → is `10` in the set? Yes → middle, skip it
- `1` → is `0` in the set? No → **start**
- `2` → is `1` in the set? Yes → middle, skip it

Nothing before you = you're the start. And it's an O(1) set lookup.

---

## The guard saga (four more failed attempts)

I had both insights. Getting them into code took four tries, and **every single failure was
mechanical, not conceptual.**

### Attempt 4 — I dropped the guard entirely

```python
def lcs_set(array):
    num_set = set(array)
    counts = []
    for i in num_set:
        count = 0                     # <-- fencepost, again
        while True:
            if i + 1 in num_set:
                count += 1
                i += 1
            else:
                counts.append(count)
                break
    return max(counts)                # <-- crashes on []
```

```
input=[1, 2, 3, 4]          returned: 3    expected: 4
input=[3, 2, 1]             returned: 2    expected: 3
input=[0,3,7,2,5,8,4,6,0,1] returned: 8    expected: 9
input=[10, 20, 30]          returned: 0    expected: 1
input=[]                    CRASHED: ValueError: max() iterable argument is empty
```

**The chain-start guard isn't in the code.** I'd just spent four rounds deriving it and then
didn't write it. Every number gets walked from: `[1,2,3,4]` walks from 1 (3 steps), 2 (2), 3 (1),
4 (0) = 6 steps for 4 numbers. **O(n²).**

**Off-by-one again:** every answer exactly 1 too low. `count = 0` counts hops, not numbers. A lone
number like `10` scores 0 when a chain of one has length 1.

**`max([])` crashes on empty input** — same shape as the `decode("")` crash in problem 271.

**One thing I got right without being told:** iterating `for i in num_set` instead of
`for i in array` handles **duplicates for free**. `[1, 1, 2]` has one `1` in the set.

### Attempt 5 — I INVERTED the guard

```python
    for i in num_set:
        if i - 1 not in num_set:    # <-- BACKWARDS
            continue
        count = 1                   # fencepost fixed, at least
```

```
input=[5]                   returned: None   expected: 1
input=[10, 20, 30]          returned: None   expected: 1
input=[1, 2, 3, 4]          returned: 3      expected: 4
```

**`[5]` returns `None`.** A single number, and the loop never walked anything at all.

`5` is a chain start — no `4` in the set. My guard says _"is 4 not in the set? Yes → **skip
it**."_ **I was skipping the chain starts and walking from the middles** — precisely inverted.

`[10, 20, 30]` → `None` for the same reason: three numbers, all starts, all skipped, `counts` stays
empty. `[1,2,3,4]` → 3: `1` skipped, then walked from `2` (3), `3` (2), `4` (1) → max 3. **I was
doing all the redundant walks and skipping the only useful one.** Back to O(n²) _and_ wrong.

### Attempt 6 — guard fixed → CORRECT, but wasteful

```python
        if i - 1 in num_set:      # skip middles. correct at last.
            continue
```

All tests passed except `[]` → `None`. But `counts` is a list that collects **every** chain length
and then takes the max — when I only ever look at the biggest. `[10, 20, 30, 40, ...]` appends a
singleton for every element: **O(n) space for nothing.**

Same move as 238's O(1)-space follow-up: I didn't need the whole `right` array, just one scalar
carried along. **The whole `counts` list collapses into one running variable.**

### Attempt 7 — O(1) space, and it HUNG

```python
        current_count = 1
        while True:
            if i + 1 in num_set:
                current_count += 1
                i += 1
            else:
                if current_count > count:
                    count = current_count
                    break              # <-- TRAPPED INSIDE THE IF
```

```
input=[1, 2, 3, 4]              returned: 4      expected: 4      (passed!)
input=[100, 4, 200, 1, 3, 2]    ***HANG — infinite loop***
input=[10, 20, 30]              ***HANG — infinite loop***
```

Trace `[10, 20, 30]`:

```
i=10:  walk. current_count=1. no 11 -> else: 1 > 0? YES -> count=1, break.   fine
i=20:  walk. current_count=1. no 21 -> else: 1 > 1? NO  -> if body skipped
                                                        -> NO BREAK
                                    -> loop back: no 21 -> else: 1 > 1? NO -> ...FOREVER
```

**I made _exiting the walk_ conditional on _finding a new best_.** Those are two completely
unrelated things. The chain ends when the chain ends — whether or not it beat the record.

`[1,2,3,4]` passed **only by luck**: the first walk always beats `count = 0`, so it always breaks.
Any _second_ chain that fails to set a new record hangs forever.

**Note the tell:** there is no compiler warning for "this loop can't exit." `-Wall` — my first
reviewer in C — does not exist in Python. **Only running it finds this.**

**One thing that fixed itself:** `[]` now returns `0`. Initializing `count = 0` and returning it
means the empty case falls out naturally — no `if counts:` guard needed. **The better structure
made the edge case disappear** instead of requiring a special branch.

### Attempt 8 — break unindented → correct, and then the real fix

Un-nesting the `break` made it correct. But the better fix was to make the bug **unwriteable**:

```python
        while i + 1 in num_set:       # the exit condition lives in the header
            current_count += 1
            i += 1
```

`while True:` puts the exit in my hands — which is _exactly how_ I attached it to the wrong
condition. A condition-driven `while` says what the loop _means_ ("keep going while the successor
exists") and there is no `break` left to misplace.

> **Lesson: when a bug comes from control flow attached to the wrong condition, the fix is often
> to restructure so the condition CAN'T be misattached — not to correct the attachment.**

---

## The final solution — O(n) time, O(n) space

```python
def lcs_set(array):
    num_set = set(array)
    count = 0

    for i in num_set:
        if i - 1 in num_set:      # I have a predecessor -> I'm a middle, skip
            continue

        current_count = 1         # a lone number is a chain of length 1
        while i + 1 in num_set:   # walk the chain by VALUE
            current_count += 1
            i += 1

        if current_count > count:
            count = current_count

    return count
```

Verified: all edge cases pass (empty, single, all-singletons, duplicates, negatives, descending,
scattered), and **0 mismatches against a brute-force checker over 5000 random inputs.**

---

## Why it's O(n) even though there's a `while` inside a `for`

This is the part that felt wrong and isn't. **The shape "while inside for" tells you nothing.**
What matters is how much the inner loop runs **in total**.

Count it on `[1,2,3,4, 10,11, 20]` (n = 7):

```
outer hits 1   -> chain start -> inner walks 4 steps  (1,2,3,4)
outer hits 2   -> has a 1 before it -> skip -> inner runs ZERO times
outer hits 3   -> skip                       -> ZERO
outer hits 4   -> skip                       -> ZERO
outer hits 10  -> chain start -> inner walks 2 steps  (10,11)
outer hits 11  -> skip                       -> ZERO
outer hits 20  -> chain start -> inner walks 1 step   (20)

total inner steps: 4 + 0 + 0 + 0 + 2 + 0 + 1 = 7        n = 7
```

Not a coincidence:

> **Every number belongs to exactly ONE chain, and only that chain's start walks through it.**

So across _all_ the walks combined, each number is stepped on **exactly once**. The inner loop's
total work is **n**, not n _per_ outer iteration. Outer O(n) + total inner O(n) = **O(n)**.

The guard is what makes this true. Without it, every number starts a walk, walks overlap
massively, and it collapses back to O(n²).

**Contrast with Approach 1**, which really _was_ O(n²): its inner `while` scanned _every sequence_
for _every_ element, and that inner work **didn't shrink as the outer advanced**. That's the
difference between a genuine n × n and a partition.

> Same reasoning as the bucket-sort lesson already in my README: **sum the total inner executions,
> don't multiply outer × inner. A loop over a partition of the data is O(n).**

**Measured proof** (worst case, one long shuffled chain):

```
n=  50000   0.0174s   0.3475 µs/elem
n= 100000   0.0443s   0.4428 µs/elem
n= 200000   0.0815s   0.4075 µs/elem
n= 400000   0.1733s   0.4332 µs/elem
```

**µs per element is flat across an 8× range.** That's what linear looks like. Quadratic would
have made the last row ~64× the first.

---

## Approach 4 — sort and scan (the real alternative)

```python
def lcs_sort(array):
    if not array:
        return 0
    array = sorted(set(array))            # set kills duplicates, sorted orders
    count = 1
    current_count = 1
    for i in range(1, len(array)):
        if array[i] == array[i - 1] + 1:  # chain continues
            current_count += 1
        else:                             # chain broke, restart
            current_count = 1
        if current_count > count:
            count = current_count
    return count
```

Sorting makes array order _meaningful_, which retroactively makes the counter-with-reset from
Approach 2 valid — the pattern wasn't wrong, the structure just wasn't there yet.

**This is a genuine space-time tradeoff:** O(1) extra space, but O(n log n) time. Real dial, both
ends useful. (Unlike PEP 393, which spends space to _preserve a fixed guarantee_ — not a tunable
tradeoff. That distinction is in my README.)

Fails the problem's O(n) constraint, but in an interview it's the right thing to mention as the
"if I couldn't use the extra space" answer.

---

## Complexity scoreboard

| #   | Approach                              | Time           | Space    | Correct? | Notes                                                    |
| --- | ------------------------------------- | -------------- | -------- | -------- | -------------------------------------------------------- |
| 1   | Build sequences as lists              | O(n²)          | O(n)     | ✗        | Can't front-extend, can't merge, returns a list          |
| 2   | Set + counter over array order        | O(n)           | O(n)     | ✗        | Counts a meaningless quantity — array order is arbitrary |
| 3   | Hop by array position (`array.index`) | O(n²)          | O(n)     | ✗        | Crashes; `index()` is a linear scan; one start only      |
| 4   | Sort + scan for runs                  | **O(n log n)** | **O(1)** | ✓        | Genuine tradeoff: less space, more time                  |
| 5   | **Set + chain-start guard**           | **O(n)**       | **O(n)** | ✓        | **OPTIMAL** — meets the constraint                       |

**Why #5 can't be beaten:** you must look at every element at least once just to know it isn't
part of some chain, so **O(n) is the floor** — and #5 sits on the floor.

---

## Lessons (bigger than this problem)

1. **Only start work from the ANCHOR.** The guard — walk only from things with nothing before
   them — is what turns "nested loops" into "a partition of the data," and O(n²) into O(n). _New
   pattern for the README._
2. **If every fix reveals a new bug, the IDEA is wrong, not the code.** Approach 1's endless
   parade of edge cases (front-extend, then merge, then merge-three...) was a signal to stop
   patching and ask what I was really being asked for.
3. **Don't build what you're not asked for.** The problem wants a _length_. I built lists.
   Constructing the answer's _structure_ when you only need a _measurement_ is wasted work — and
   every piece of that structure is a new bug surface.
4. **Check that a pattern's prerequisites hold before reaching for it.** Counter-with-reset needs
   input adjacency to _mean_ something. Here it doesn't (until you sort — and then it does).
5. **Walk by VALUE, not by POSITION.** Once the set exists, the array is dead weight — the chain
   generates itself from the start value (`i+1`, `i+2`, ...). Asking the array _where_ a value
   lives (`array.index`) throws away the whole reason you built the set.
6. **"While inside for" ≠ O(n²).** Sum the _total_ inner executions. If the inner work partitions
   the data, it's O(n).
7. **Fencepost, again:** counting **edges** (hops) vs **nodes** (numbers). Off-by-one every time.
   Same family as Kestrel's `count` vs `count+1`.
8. **Make the bug unwriteable, don't just fix it.** `while True` + a hand-placed `break` is what
   _allowed_ me to attach the exit to the wrong condition. `while <condition>` removes the
   possibility.
9. **A better structure can delete an edge case.** Going O(1)-space turned `max([])`-crashes-on-
   empty into `return 0`, for free. No special branch.
10. **Python has no `-Wall`.** In C the compiler is my first reviewer. In Python, _running it
    against edge cases IS the compiler._ These five would have caught **every** bug in this
    session: **empty · single element · all singletons · duplicates · negatives (+ descending).**

---

## Say-it-out-loud summary

> "Order in the input doesn't matter, so I dump everything into a set — that gives me O(1) 'is
> this number present?' lookups, and kills duplicates for free. Then, for each number, I check
> whether it's the START of a chain: it is if `i - 1` isn't in the set, meaning nothing precedes
> it. If it isn't a start I skip it entirely — that's the key move. From a start, I walk forward
> by value — `i+1`, `i+2` — counting until the chain breaks, and track the running best.
>
> It looks like a nested loop but it's O(n): every number belongs to exactly one chain, and only
> that chain's start walks through it, so across all the walks combined each number is visited
> exactly once. Total inner work is n, not n per outer iteration. Without the chain-start guard
> you'd re-walk every chain from every one of its members and it'd be O(n²).
>
> O(n) time, O(n) space for the set. If space were the constraint I'd sort and scan for runs
> instead — O(1) extra space but O(n log n) time. That's the real tradeoff here."

---

## Meta-note (worth being honest about)

I derived the two real insights — _walk by value_ and _only walk from chain starts_ — essentially
unaided. That's the hard part of this problem and the reason it's a Medium.

**Every single failure after that was execution-detail, and all four are in my documented
recurring bug families:**

| Bug                                        | Family                              |
| ------------------------------------------ | ----------------------------------- |
| Dropped the guard I'd just derived         | —                                   |
| Inverted the guard (`not in` vs `in`)      | inverted logic / De Morgan          |
| `count = 0` instead of `count = 1` (twice) | fencepost — edges vs nodes          |
| `break` trapped inside the `if`            | control flow on the wrong condition |

**My reasoning is ahead of my execution.** Every one of those bugs was invisible until the code
_ran_. In C, `-Wall` catches a chunk of this class for me. Python offers nothing — so for Python,
**the edge-case run IS the compiler.** Run it before believing it.
