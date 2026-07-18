# LeetCode 125 — Valid Palindrome: My Notes

Return whether a string reads the same forwards and backwards — **after** lowercasing it and
throwing away everything that isn't a letter or a digit.

```
"A man, a plan, a canal: Panama"  ->  "amanaplanacanalpanama"  ->  True
"race a car"                      ->  "raceacar"               ->  False
" "                               ->  ""                       ->  True
```

**Two rules that ARE the whole problem** (and both tripped me up):

1. **Only letters and digits count.** Spaces, commas, colons, apostrophes, underscores — all invisible.
2. **Case doesn't matter.** `A` and `a` are the same character.

This is the **first problem in the Two Pointers section**, and the section exists to teach one idea:
_walk the original data from two ends at once, instead of building a second copy of it._ Keep that in
mind — it's why the optimal answer here is not the obvious one.

---

## First instinct — reverse it and compare (BROKEN)

My first idea: reverse the string, then compare `reversed[n-1-i]` to `s[i]`.

```python
def is_palindrome(s):
    rev = s[::-1]
    n = len(s)
    for i in range(n):
        if rev[n - 1 - i] != s[i]:
            return False
    return True
```

I ran it. It returned **`True` for every string I gave it — including `"hello"`.**

### Why it's a tautology

Take `"abc"`:

```
s    =  a  b  c        rev  =  c  b  a
index   0  1  2                0  1  2
```

Where did `rev[2]` come from? It's `'a'` — and `'a'` was `s[0]`. **Reversing MOVED it there.** So:

```
rev[2] IS s[0]      I compare it to s[0]   ->  always equal
rev[1] IS s[1]      I compare it to s[1]   ->  always equal
rev[0] IS s[2]      I compare it to s[2]   ->  always equal
```

**I reversed the string, then read it from the far end — which put every character back where it
started.** Two operations that cancel out. The loop asks "is `s[i]` equal to `s[i]`?" — yes, forever.

> **Lesson: don't undo your own work.** If I keep the reversed string, I have to compare it at the
> _same_ index (`rev[i]` vs `s[i]`), which pairs first-with-last. Or just `s == s[::-1]`.

---

## What a palindrome check actually is

`"racecar"` — compare mirror pairs walking inward:

```
r  a  c  e  c  a  r
↑                 ↑     first vs last       r == r  ✓
   ↑           ↑        second vs 2nd-last  a == a  ✓
      ↑     ↑           third vs 3rd-last   c == c  ✓
         ↑              middle — no partner, done
```

If every mirror pair matches, it's a palindrome. **I don't need a reversed copy to compare
first-to-last — I just need two index variables.**

---

## Approach 1 — two pointers, skip-in-place (OPTIMAL)

```python
def is_palindrome(s):
    left = 0
    right = len(s) - 1

    while left < right:
        if not s[left].isalnum():        # junk on the left -> ADVANCE, then retry
            left += 1
            continue
        if not s[right].isalnum():       # junk on the right -> ADVANCE, then retry
            right -= 1
            continue

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

### How to check "is this punctuation?" — flip the question

There are thousands of punctuation/symbol characters; I can't list them. So I don't ask _"is this
junk?"_ — I ask **"is this a letter or a digit?"** with the built-in `c.isalnum()`, and skip anything
that isn't.

```
"a".isalnum() -> True     ",".isalnum() -> False
"5".isalnum() -> True     " ".isalnum() -> False
"_".isalnum() -> False    (underscore is NOT alnum — a real trap, handled for free)
```

`.isalnum()` and `.lower()` are the two built-ins this problem is really testing. Most people reach
for regex or a manual `'a' <= c <= 'z'` range; knowing these two methods exist _is_ the problem.

### The `while left < right` condition — why `<` and not `<=`

```
odd length  "racecar":  pointers MEET  -> left == right -> stop (middle has no partner)
even length "abba":      pointers CROSS -> left  > right -> stop
```

`left < right` handles both. A single middle character always reads the same either way, so there's
nothing to check when they land on it. (`<=` would compare the middle to itself — always true, so no
wrong answers, just one wasted comparison. `<` is cleaner.)

The `<` also makes the **all-junk / empty** cases work for free: the pointers skip everything, cross,
the loop never runs, and it returns `True`. `""`, `" "`, `".,"` all handled with no special case.

### The bugs I hit getting here (both worth remembering)

**Bug 1 — `continue` without advancing (near-infinite loop).** My first skip was:

```python
if not s[left].isalnum() or not s[right].isalnum():
    continue                                    # <-- moves NOTHING
```

`continue` jumps to the top of the loop **without moving either pointer.** So a comma at `left` gets
re-checked forever. It only _didn't_ hang in testing because a different bug (below) returned first.

> This is the **trapped-control-flow family from problem 128** — there, a `break` was attached to the
> wrong condition; here, a `continue` skips the state change the loop depends on. Same root cause:
> **control flow that bypasses the thing that makes progress.** Second time this has bitten me.

The fix is two _separate_ `if`s, each advancing its own pointer — which also fixes a hidden problem in
the `or`: if only `right` is junk, a combined `continue` can't know which side to move. Splitting
solves both at once.

**Bug 2 — forgot `.lower()`.** Compared `A` to `a` as unequal, failing the Panama string. The case
rule is rule #2 and I skipped it on the first pass.

---

## Approach 2 — clean, then compare to reverse (O(n) space)

```python
def is_palindrome(s):
    cleaned = "".join(c for c in s if c.isalnum()).lower()
    return cleaned == cleaned[::-1]
```

Readable, idiomatic, correct. Build a cleaned+lowercased string, compare to its slice-reverse.

**One bug on the way here:** I first wrote `return cleaned == reversed(cleaned)`. It returned `False`
for everything, including `"racecar"`.

```
reversed("racecar")  ->  <reversed object at 0x...>     # an ITERATOR, not a string
```

`reversed()` returns a lazy iterator, not a string, so I was comparing a string to an iterator object
— never equal. The fix is the slice `cleaned[::-1]`, which returns an actual reversed string (the same
idiom from Encode/Decode Strings).

> **Lesson: know what a function RETURNS before comparing its output.** `reversed()` → iterator,
> `.sort()` → `None`, `map()` → iterator. Python has a whole family of lazy/in-place functions that
> don't hand back the thing you'd expect.

**Small right call:** `.lower()` goes on the _whole finished string_ (outside the `join`), not on each
character inside the generator — one call instead of one-per-character.

---

## Complexity — both, and why the tradeoff is the point

| Approach                       | Time     | Space    | Note                                     |
| ------------------------------ | -------- | -------- | ---------------------------------------- |
| 0 — reverse & read backwards   | O(n)     | O(n)     | **broken** (tautology)                   |
| 1 — **two pointers, in place** | **O(n)** | **O(1)** | **OPTIMAL** — two int pointers, no copy  |
| 2 — clean + compare reverse    | O(n)     | O(n)     | builds `cleaned` **and** `cleaned[::-1]` |

Same time. **The whole difference is space**, and that difference is exactly what the Two Pointers
section is teaching:

- Approach 2 allocates a whole cleaned string, then a whole reversed copy of it. On a 1-million-char
  input, that's ~2 million characters of extra memory just to answer yes/no.
- Approach 1 walks the original with **two integers** and can **exit early** — `"xbbbbbbbbbb..."`
  fails on comparison #1 without allocating anything.

> **This is optimal.** O(n) time is the floor — you must look at each character at least once to
> know. O(1) space is the floor — two pointers, no copy. Approach 1 sits on both floors.

### On "isn't it O(n/2)?"

I only compare ~half the pairs (the two pointers split the string between them), so I wanted to write
**O(n/2)**. But **O(n/2) isn't a thing** — big-O drops constant factors, because it describes how work
_grows_, not the exact count. `n/2`, `n`, `100n`, `n+5` are all straight lines → all **O(n)**. The
constant changes the slope, not the shape; only the shape (line vs parabola) matters.

Also the ½ is a bit of a lie: the two pointers together still touch all `n` characters — they _share_
the work, `n/2` each, total `n`.

> **Companion to my "big-O ≠ speed" note:** that one says constants matter for _real-world speed_;
> this one says constants _don't appear in the notation_. Both true, different lenses.

---

## The reusable pattern

**Two pointers converging from both ends, skipping junk on each side independently, walking inward.**
The skeleton — `while left < right`, skip-and-advance on each side, compare, step both — recurs across
the rest of this section: **167 (Two Sum II), 15 (3Sum), 11 (Container With Most Water), 42 (Trapping
Rain Water).** The detail that transfers most: **advance the pointer BEFORE you `continue`**, or the
loop stalls.

---

## Say-it-out-loud (interview version)

> "Two pointers, one at each end. On each side I skip anything that isn't alphanumeric, moving that
> pointer inward until it lands on a real character. Then I compare the two characters
> case-insensitively — if they differ, it's not a palindrome; if they match, I step both pointers in
> and continue until they meet in the middle. It's O(n) time and O(1) space, because I never build a
> cleaned copy — I skip over the junk in place. The cleaner-to-read alternative is to strip and
> lowercase into a new string and compare it to its reverse, but that's O(n) space for the two extra
> strings, so I'd only reach for it when memory isn't a concern."
