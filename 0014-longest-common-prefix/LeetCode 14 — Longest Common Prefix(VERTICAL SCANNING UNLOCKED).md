
My working notes on Longest Common Prefix. This one taught me more about _choosing the right tool_ than about the problem itself — I started with completely the wrong approach, and understanding **why** it was wrong is the real lesson.

The problem: given a list of strings, return the longest string that **every** string **starts with** (reading left to right). `["flower","flow","flight"] -> "fl"`. If there's no common prefix, return `""`.

The reframe that unlocked it: this is a **"read down the columns"** problem. Stack the words:

```
f l o w e r
f l o w
f l i g h t
```

Read top-to-bottom, column by column. Column 0: `f,f,f` match. Column 1: `l,l,l` match. Column 2: `o,o,i` — mismatch. Stop. Answer = the columns that matched = `"fl"`.

**Prefix = a POSITION problem (order + position matter), not a COUNTING problem.**

---

## My scoreboard

|#|My approach|Time|Space|Verdict|
|---|---|---|---|---|
|1|Hash map (char counts)|O(n·m)|O(k)|**WRONG** — throws away position & order|
|2|Vertical scan (columns)|O(n·m)|O(1)|**Correct & optimal**|

Where `n` = number of strings, `m` = length of the shortest string, `k` = distinct chars.

---

## 1. The hash map approach — why it FAILED (the important lesson)

```python
def long_prefix(strs):
    hash_map = dict()
    min_length = min(len(s) for s in strs)
    prefix = ""
    for i in range(len(strs)):
        for j in range(min_length):
            hash_map[strs[i][j]] = hash_map.get(strs[i][j], 0) + 1
    for i in hash_map:
        if hash_map[i] != len(strs):
            return prefix
        else:
            prefix += i
```

**Why I reached for this:** I'd just done Contains Duplicate, Two Sum, and Valid Anagram — three hash-map problems in a row. My brain pattern-matched "recent problems → hash map" and applied it. That's pattern recognition _working_ and misfiring on a problem from a different family 

**Why it's fundamentally broken:** a hash map counts _how many times_ each character appears. But a prefix is about _which character is at each position, in order_. Counting is inherently **orderless** — `{'a':4, 'b':4}` is identical whether the words were `"abab"`, `"baba"`, or `"aabb"`, but those have completely different prefixes. The moment I count, I've destroyed the exact information (position + order) the problem depends on.

Concrete failure — `["abab","abab"]` (answer should be `"abab"`):

- hash_map becomes `{'a': 4, 'b': 4}` (each letter appears twice per word, times 2 words).
- My check `if hash_map[i] != len(strs)` sees `4 != 2` → returns `""`. WRONG.

Three separate flaws, all rooted in "counting kills position":

1. **Position is gone** — `f` at column 0 and `f` at column 5 land in the same bucket, but a prefix cares deeply where a character sits.
2. **The count logic assumes each char appears at most once per word** — false. `["abab"]` breaks it immediately.
3. **Iterating `for i in hash_map` uses dict insertion order**, not prefix order — even the output order is wrong.

It only _looked_ like it worked on `["flower","flow","flight"]` by luck, because that prefix's characters (`f`, `l`) happen to appear exactly once per word.

**The transferable lesson — match the data structure to the shape of the question:**

- **Hash map / set** → _membership or counts, order doesn't matter_: "have I seen this?" (Contains Duplicate), "same letters regardless of arrangement?" (Anagram), "what's the complement I need?" (Two Sum).
- **Position-by-position scan** → _order and position matter_: "common prefix?", "palindrome?", "do these sequences match?".

LCP is a _position_ problem wearing clothes that made it look like a _counting_ problem. Recognizing "this is about order, not counts → different tool" is the actual skill here.

---

## 2. The vertical scan — correct & optimal

```python
def long_prefix_1(strs):
    prefix = ""
    min_length = min(len(s) for s in strs)   # can't be longer than the shortest word
    for cols in range(min_length):           # OUTER = column/position
        for word in strs:                    # INNER = every word at this column
            if word[cols] != strs[0][cols]:  # compare against the first word
                return prefix                # mismatch -> stop, return what matched
        prefix += strs[0][cols]              # all words agreed -> commit this column's char
    return prefix                            # ran out of columns -> whole shortest word matched
```

**The idea:** walk column by column. At each column, check that _every_ word has the same character as the first word. If all agree, that character is confirmed common → append it. The instant one word disagrees, stop — the prefix is everything confirmed so far.

**Why the nesting matters (a bug I fought):** the OUTER loop must be the **column**, the INNER loop the **words**. My first attempt had it backwards (word outer, column inner), which scanned each word fully against itself before checking the others — building the prefix from one word alone. A prefix is a _vertical_ property (all words at one position), so the position loop has to be on the outside.

**The two things that make it correct:**

1. **`min_length`** — the prefix can't exceed the shortest word, so bounding the column loop by `min_length` prevents any index-out-of-bounds crash. (This was my one good instinct in the first attempt.)
2. **Append after the inner loop finishes without returning** — a character is only confirmed common once _all_ words agreed on it. So the append lives outside the word loop, inside the column loop. I use `strs[0][cols]` as the clear reference (the confirmed common char).

---

## Complexity — and why it's already optimal

- **Time: O(n·m)** — `n` strings, `m` = shortest string length. Worst case (all strings identical) I touch every character of the prefix in every string. _This is NOT O(n²)_ — the inner loop iterates _strings_ (n), the outer iterates _characters_ (m); they're different quantities, so it's n·m, not n·n.
- **Space: O(1)** extra (just the prefix I return).

**Why O(n·m) is the theoretical floor:** to know the longest common prefix, any algorithm must at least _read_ the prefix characters in every string (e.g. when all strings are equal, you must read them fully to confirm). You can't determine the answer without looking at those ~n·m characters. So there is no faster asymptotic approach — I'm already at optimal.

**Knowing when to STOP optimizing is itself a skill.** I asked "can I do better than O(n²)?" — the correct response was: it's not O(n²), it's O(n·m), and O(n·m) is optimal, so stop.

---

## What I learned (bigger than this problem)

1. **Match the structure to the question.** Counting (hash map) destroys order; prefixes need order. A great tool aimed at the wrong question is still wrong.
2. **My hash-map reflex misfired because of recency** — I'd just done 3 hash-map problems. Recognizing "different family, different tool" is the skill.
3. **Loop nesting encodes the shape of the problem.** A prefix is vertical (position outer, words inner). Getting the nesting backwards silently produces the wrong logic.
4. **Return on every path** — my recurring bug. Handle both the early-exit path AND the "reached the end" path.
5. **Know when you've hit the optimal bound and stop.** O(n·m) here is the floor; chasing a faster algorithm would be wasted effort.
6. **Complexity needs the right variables.** "O(n²)" was wrong — with two different quantities (strings vs characters) it's O(n·m). Naming the variables correctly matters.

## The summary I want to be able to say out loud

> "It's a common-prefix problem, so I scan vertically: column by column, I check that every string has the same character as the first string; the moment one differs, or I run out of the shortest string, I stop and return what matched. That's O(n·m) time — n strings, m the shortest length — and it's optimal, because any algorithm has to read the prefix characters in every string at least once. A hash map doesn't work here because counting characters throws away position and order, which is exactly what a prefix depends on."