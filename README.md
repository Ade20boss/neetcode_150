# NeetCode 150 — Solved in Depth

My working repository for the [NeetCode 150](https://neetcode.io/practice). This is not a
place to dump accepted submissions — it's a study log. For each problem I solve it **several
ways**, compare the approaches, identify the optimal one, and write notes in my own words
explaining _why_. The goal is **depth, not breadth**: I'd rather understand one problem
completely than skim ten.

Every problem earns its own folder in the repo root, containing the implementation(s) and a
notes file.

---

## Method

For each problem I work through the same loop:

1. **Solve it myself first** — before watching any solution.
2. **Solve it multiple ways** — brute force, then progressively better approaches.
3. **Compare and rank them** — time complexity, space complexity, and the tradeoffs.
4. **Identify the optimal** — and be able to justify the choice out loud.
5. **Write notes in my own voice** — what confused me, what clicked, what I learned.
6. **Push to GitHub** — one problem a day.

### Sunday cold re-solves

Every Sunday I re-solve a handful of earlier problems **from a blank file, without notes**.
If I can't reproduce a solution cold, that's a gap — and that problem gets revisited. This
is how a solution goes from "I did it once" to "I own it."

---

## Repo structure

Each problem is its own folder at the repo root:

```
neetcode-150/
├── README.md
├── 0001-two-sum/
│   ├── solution.py        # all approaches
│   └── notes.md           # my breakdown, in my own words
├── 0217-contains-duplicate/
│   ├── solution.py
│   └── notes.md
├── 0242-valid-anagram/
│   ├── solution.py
│   └── notes.md
└── ...
```

Each `notes.md` follows the same shape: the approaches I tried, a complexity scoreboard,
what tripped me up, the optimal choice, and the "say it out loud" interview summary.

---

## Progress

**Solved:** 9 / 150

**Cold re-solve legend:** ✅ can reproduce from scratch · 🔁 needs another cold pass · ⬜ not yet re-solved

_(Problems are grouped below by NeetCode pattern for readability, but each lives in its own
root-level folder.)_

---

## Patterns I keep seeing

A running list of the reusable ideas that recur across problems. I add to this as they show up
again — the point is to notice the *same idea in different disguises*, which is how a solution
goes from "I did it once" to "I recognize this instantly."

- **Hash map for O(1) lookup / "have I seen this?"** — the workhorse of Arrays & Hashing. Membership
  (Contains Duplicate), complement lookup (Two Sum), counting (Valid Anagram, Top K Frequent),
  grouping by a key (Group Anagrams). If the question is "does X exist / how many / group by,"
  reach for a dict or set.
- **Value-as-index** — when values are small and bounded, use the value itself as an array index
  instead of hashing. `ord(c)-'a'` -> 26-slot list (Valid Anagram); frequency -> bucket index (Top K
  Frequent bucket sort). Faster than a hash map, O(1) space when the range is fixed.
- **Prefix / running accumulation** — build each entry from the *previous* one with O(1) work
  instead of re-scanning from scratch. Turns an O(n^2) "look at everything before me" into O(n).
  Product Except Self (prefix products). Seed of dynamic programming.
- **Canonical signature -> bucket** — to group "equivalent" things, map each to a canonical key and
  bucket by it. Group Anagrams (sorted letters, or count tuple, as the key).
- **2D-to-1D flattening (`row * width + col`)** — whenever a naturally 2D idea needs to address
  into a flat 1D structure. Valid Sudoku's box index `(row//3)*3 + (col//3)` is this exact pattern
  applied to a 3x3 grid of boxes — same shape as a matrix's `row * stride + col`.
- **Length-prefixing / self-describing formats** — instead of relying on a delimiter that could
  collide with real content, prefix data with its own length so the reader never has to guess
  where it ends. Encode and Decode Strings. A protocol-design pattern, not a DSA pattern.
- **append vs indexed assignment** — `append` builds in *walk order* and grows the list; `arr[i] = x`
  builds in *position order* but needs the slot to already exist (pre-size the list). Use indexed
  assignment when walk direction != storage order. (Product Except Self right-pass.)
- **List-then-join over repeated string `+=`** — string `+=` in a loop is secretly O(n^2) (every
  concatenation re-copies everything accumulated so far, since strings are immutable). Collect
  pieces in a list (cheap, amortized O(1) appends) and `"".join(...)` once at the end for O(n).

### Complexity-reasoning lessons
- **Big-O != speed.** Constant factors matter at small sizes — C built-ins (`sorted`) beat Python-loop
  counting even when the loop is asymptotically better (Group Anagrams).
- **Nested loops are NOT always O(n^2).** Sum the *total* inner executions, don't multiply outer x
  inner. A loop over a partition of the data (each item in exactly one inner pass) is O(n) (bucket
  sort). Sequential passes ADD (O(n)); nested passes MULTIPLY (O(n^2)).
- **Fencepost family.** length vs last-index; need `n+1` slots for indices `0..n`. Recurs everywhere.
- **Space-time tradeoffs are real, but not everywhere.** Fewer memory passes vs. less peak memory
  used (Valid Sudoku's one-pass vs three-pass) is a genuine tradeoff. Not every "spend space to
  save time" situation is a dial, though — PEP 393 spends space to *preserve a fixed guarantee*
  (O(1) string indexing), which isn't the same thing as a tunable tradeoff.

---

### Arrays & Hashing

| #   | Problem                                                              | Approaches                                                          | Optimal                                                                                    | Cold re-solve |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------- |
| 1   | [Two Sum](./0001-two-sum/)                                           | brute · one-pass hashmap                                                | O(n) time / O(n) space (hashmap)                                                               | ⬜            |
| 36  | [Valid Sudoku](./0036-valid-sudoku/)                                 | three-pass (row/col/box) · single-pass (3 sets per cell)                | O(1) time (fixed 9x9 board) — single-pass trades more peak memory for fewer memory passes      | ⬜            |
| 49  | [Group Anagrams](./0049-group-anagrams/)                             | sort-key · count-key                                                    | O(n·k) time / O(n·k) space (sort-key wins in practice)                                        | ⬜            |
| 217 | [Contains Duplicate](./0217-contains-duplicate/)                     | brute · sort · dict · set                                               | O(n) time / O(n) space (set)                                                                   | ⬜            |
| 238 | [Product of Array Except Self](./0238-product-of-array-except-self/) | brute (del/insert) · prefix products (2 arrays) · in-place              | O(n) time / O(1) extra space (in-place prefix products)                                        | ⬜            |
| 242 | [Valid Anagram](./0242-valid-anagram/)                               | sort · Counter · 1-liner · build-dict · one-dict ±→0 · 26-slot list      | O(n) time / O(1) space (26-slot list)                                                          | ⬜            |
| 271 | [Encode and Decode Strings](./0271-encode-and-decode-strings/)       | naive delimiter (broken) · length-prefixing                             | O(n) time / O(n) space (length-prefixed, list+join for encode)                                 | ⬜            |
| 347 | [Top K Frequent Elements](./0347-top-k-frequent-elements/)           | max+delete · bucket sort                                                | O(n) time / O(n) space (bucket sort)                                                            | ⬜            |

### Two Pointers

_— not started —_

### Sliding Window

_— not started —_

### Stack

_— not started —_

### Binary Search

_— not started —_

### Linked List

_— not started —_

### Trees

_— not started —_

### Tries

_— not started —_

### Heap / Priority Queue

_— not started —_

### Backtracking

_— not started —_

### Graphs

_— not started —_

### 1-D Dynamic Programming

_— not started —_

### 2-D Dynamic Programming

_— not started —_

### Greedy

_— not started —_

### Intervals

_— not started —_

### Math & Geometry

_— not started —_

### Bit Manipulation

_— not started —_

---

## Strings

| #   | Problem                                                | Approaches                       | Optimal                                  | Cold re-solve |
| --- | ------------------------------------------------------ | --------------------------------- | ----------------------------------------- | ------------- |
| 14  | [Longest Common Prefix](./0014-longest-common-prefix/) | hashmap (failed) · vertical scan | O(n·m) time / O(1) space (vertical scan)  | ⬜            |

---

## Why this repo exists

Anyone can collect green checkmarks. This repo is proof of something rarer: that for each
problem I can write multiple correct solutions, reason about their time/space tradeoffs,
choose the optimal one deliberately, and explain all of it clearly. That reasoning — not the
accepted submission — is what actually transfers to an interview and to real engineering.

**Principle:** understand it completely, or it doesn't count.
