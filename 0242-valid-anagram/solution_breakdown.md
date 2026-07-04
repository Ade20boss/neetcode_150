
My working notes on how I solved Valid Anagram five different ways. Written for future me, so I remember not just _what_ I wrote but _why_ each version works and what I learned.

The problem: given two strings `s` and `t`, return `True` if `t` is an anagram of `s` — same characters, same counts, any order.

The realization that framed everything: this whole problem is really just **"how do I compare two strings while ignoring order?"** I found there are two families of answers — **sort both** and compare (O(n log n)), or **count both** and compare the tallies (O(n)). Counting wins because I never pay to establish an order I don't actually care about.

---

## My scoreboard

|#|My approach|Time|Space|My note|
|---|---|---|---|---|
|1|Sort + compare (naive)|O(n log n)|O(n)*|order-erasing by reordering|
|2|Counter + manual loop|O(n)|O(n)|works, but "correct-by-interaction"|
|3|Counter == Counter (1-liner)|O(n)|O(n)|the idiomatic one|
|4|Build two dicts, compare|O(n)|O(n)|my first from-scratch version|
|5|One dict, +/- to zero|O(n)|O(k)→O(1)|the tightest one — I'm proud of this|

* I used `sorted()`, which builds new lists → O(n) space.

**My takeaway:** all five are correct. Sorting is simplest but slowest. Everything in the counting family is O(n). #5 is the one I'd bring to an interview; #4 is the clean from-scratch version; #3 is what I'd actually type in real code.

---

## The thing that confused me: why can't I just do `s == t`?

I got stuck here for a bit. I thought maybe I could just compare the strings directly. But `s == t` checks if they're **identical** — same characters in the **same order**, position by position. Anagrams are the same characters in a _different_ order (`listen`/`silent`). So `==` is order-sensitive, and if `s == t` were ever True the strings would literally be the same string — useless for this. An anagram is about the **multiset** of characters (which letters, how many), not the sequence. That's exactly why I have to sort or count first — to strip the order out before comparing.

---

## 1. Sort + compare (my naive baseline) — O(n log n)

```python
def is_anagram_naive(s, t):
    return sorted(t) == sorted(s)
```

I sorted both strings so their characters line up in the same canonical order — then two anagrams become identical and `==` finally means "same letters":

```
"listen" -> ['e','i','l','n','s','t']
"silent" -> ['e','i','l','n','s','t']   -> equal -> True
"rat"    -> ['a','r','t'] vs "car" -> ['a','c','r']  -> differ -> False
```

It's O(n log n) because the sort dominates. I realized this is the "naive" one because I'm paying to _reorder_ data whose order I don't even care about — counting avoids that.

---

## 2. Counter + manual loop — O(n)

```python
from collections import Counter
def is_anagram_optimal(s, t):
    if len(s) != len(t):
        return False
    s_freq = Counter(s)
    t_freq = Counter(t)
    for i in s:
        if s_freq[i] != t_freq[i]:
            return False
    return True
```

This was basically my first real solution. `Counter(s)` builds a frequency map in one pass (`Counter("aab")` -> `{'a':2,'b':1}`), then I loop over `s` checking each character's count matches in both.

**What I learned is subtle here:** my loop only iterates `for i in s`, so it only directly checks characters that are in `s`. A character that's in `t` but not `s` never gets visited directly — BUT it still works, because Counter returns `0` for missing keys (not an error), and my length check guarantees that any "extra in t" forces some "extra in s" that the loop _does_ catch. So it's correct, but only because two things line up (Counter's zero-default

- my length guard). My later versions (#3 and #5) are correct _directly_, without me having to reason about that interaction — and I now think simpler-and-directly-correct is better.

Also: I'm building two full Counters _and_ manually looping. That loop is redundant — #3 does the whole comparison with one `==`.

---

## 3. Counter == Counter (my one-liner) — O(n)

```python
from collections import Counter
def is_anagram_one_liner(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
```

I realized a `Counter` is just a dict of `{char: count}`, and two dicts are equal when they have the same keys with the same values — so `==` does my entire manual loop from #2 in one operation. This is the version I'd write in real code.

The catch I noted: using `Counter` is almost cheating in an interview, because it hides the counting mechanism. but as usual i need to see me _build_ the count myself (that's #4 and #5) to prove I could implement `Counter` if it didn't exist.

---

## 4. Build two dicts myself — O(n)

```python
def is_anagram_build_dict(s, t):
    if len(s) != len(t):
        return False
    s_freq = dict()
    t_freq = dict()
    for i in range(len(s)):
        s_freq[s[i]] = s_freq.get(s[i], 0) + 1
        t_freq[t[i]] = t_freq.get(t[i], 0) + 1
    return s_freq == t_freq
```

This is where I built the frequency map by hand instead of leaning on `Counter` — basically proving to myself I understand what `Counter` was doing. Build a count for each string, then compare with `==`.

**The technique I learned:** `dict.get(char, 0) + 1`. Accessing a missing dict key throws a `KeyError`, so I use `.get(char, 0)` to return 0 when the key isn't there yet — meaning `freq[char] = freq.get(char, 0) + 1` works whether or not I've seen the character before. (Same `.get()` tool I used in Contains Duplicate.)

---

## 5. One dict, increment/decrement to zero — O(n), O(1) space ← my favorite

```python
def is_anagram_one_dict(s, t):
    if len(s) != len(t):
        return False
    count = dict()
    for i in range(len(s)):
        count[s[i]] = count.get(s[i], 0) + 1   # s pushes counts UP
        count[t[i]] = count.get(t[i], 0) - 1   # t pushes counts DOWN
    for c in count:
        if count[c] != 0:
            return False
    return True
```

This one took me a while to _get_, but once it clicked it was my favorite. The idea: use ONE dict and let the two strings fight each other in it. `s` **increments** each character, `t` **decrements** each character. If they're anagrams, every increment from `s` gets cancelled by a decrement from `t`, so every count lands on exactly **0**. Any nonzero leftover means not an anagram. (I think of it as a tug-of-war per character — anagram means every rope ends dead center.)

**The trace that made it click for me** — my tricky case `chase` vs `chair`:

```
shared c,h,a all cancel to 0
's':1, 'e':1 left positive  -> extra letters in s
'i':-1,'r':-1 left negative -> extra letters in t
-> nonzero values remain -> False
```

So mismatches get caught two ways: a **positive** leftover means `s` had a char `t` didn't cancel; a **negative** leftover means `t` had a char `s` never provided (decrementing a missing key drops it below 0). The matching letters silently cancel to 0 and vanish — only the _differences_ are left standing. All-zero is only possible for a real anagram.

**What I'm most proud of:** I merged the two count loops into ONE. Since my length check guarantees `len(s) == len(t)`, I could increment `s[i]` and decrement `t[i]` in the same loop by indexing both strings at position `i`. Still O(n), just tighter — and I got there on my own, it wasn't in the version I was shown.

Space is O(k) where k = distinct characters (≤ 26 for lowercase) → effectively O(1).

---

## What I learned (bigger than this problem)

**1. Sequential loops ADD, nested loops MULTIPLY.** I worried that #5's multiple passes made it inefficient. But three loops side-by-side is `n + n + n = O(n)` — the constant `3` gets dropped. Only loops _nested inside each other_ multiply into O(n²). So more loops ≠ worse complexity; only nesting is. That reframed how I judge efficiency.

**2. Sorting vs counting are two ways to ignore order.** Sorting reorders (O(n log n)); counting tallies (O(n)). Counting wins because it never establishes an order I don't need — same reason `set` beat `sort` in Contains Duplicate.

**3. `==` on strings compares order too** — which is exactly why I couldn't just do `s == t` and had to sort or count first.

**4. "Correct directly" beats "correct-by-interaction."** My #2 works only because the length guard and the partial loop line up. My #3/#4/#5 are correct without that reasoning. I'll aim for the directly-correct kind.

**5. `dict.get(key, 0)` is my clean "first time seeing this key" tool** — no KeyError, works for counting both up and down.

**6. I should test with the input that BREAKS it, not the one that passes.** `aacc`/`ccac` (same letters, different counts) and `chase`/`chair` (shared letters, not an anagram) were the killers. My question to ask every time: "what input would make this lie to me?"

**7. The length check is a free early exit** — different lengths can't be anagrams, so I bail in O(1) before counting anything. It's a correctness guard AND a speed win.

---

## The summary

> "Anagram means same character counts regardless of order, so I can't just compare the strings directly — that checks order too. Simplest is sorting both and comparing, O(n log n). Better is counting: one pass with a single dict, incrementing for `s` and decrementing for `t`, then check every count is zero — O(n) time, O(1) space since the alphabet is bounded."

