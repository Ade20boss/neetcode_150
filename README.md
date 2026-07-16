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
│   ├── solution.py              # all approaches
│   └── solution_breakdown.md    # my breakdown, in my own words
├── 0217-contains-duplicate/
│   ├── solution.py
│   └── solution_breakdown.md
├── 0242-valid-anagram/
│   ├── solution.py
│   └── solution_breakdown.md
└── ...
```

Each `solution_breakdown.md` follows the same shape: the approaches I tried, a complexity
scoreboard, what tripped me up, the optimal choice, and the "say it out loud" interview summary.

---

## Progress

**Solved:** 10 / 150

**Cold re-solve legend:** ✅ can reproduce from scratch · 🔁 needs another cold pass · ⬜ not yet re-solved

_(Problems are grouped below by NeetCode pattern for readability, but each lives in its own
root-level folder.)_

---

## Patterns I keep seeing

A running list of the reusable ideas that recur across problems. I add to this as they show up
again — the point is to notice the _same idea in different disguises_, which is how a solution
goes from "I did it once" to "I recognize this instantly."

- **Hash map for O(1) lookup / "have I seen this?"** — the workhorse of Arrays & Hashing. Membership
  (Contains Duplicate), complement lookup (Two Sum), counting (Valid Anagram, Top K Frequent),
  grouping by a key (Group Anagrams), existence probes for chain-walking (Longest Consecutive
  Sequence). If the question is "does X exist / how many / group by," reach for a dict or set.
- **Value-as-index** — when values are small and bounded, use the value itself as an array index
  instead of hashing. `ord(c)-'a'` -> 26-slot list (Valid Anagram); frequency -> bucket index (Top K
  Frequent bucket sort). Faster than a hash map, O(1) space when the range is fixed.
- **Prefix / running accumulation** — build each entry from the _previous_ one with O(1) work
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
- **Only start work from the ANCHOR** — when work naturally partitions the data into disjoint
  groups, guard the outer loop so work only begins at each group's _entry point_, and skip
  everything else in O(1). Longest Consecutive Sequence: only walk a chain from a number with no
  predecessor (`i - 1 not in num_set`). Without the guard you re-walk every chain from every one
  of its members = O(n^2); with it, every element is visited exactly once across all walks = O(n).
  **The guard IS the algorithm.** Ask: "what makes something the _start_ of its group?"
- **Walk by VALUE, not by POSITION** — once a set exists, the input array is dead weight. A
  consecutive chain generates itself from its start value (`i+1`, `i+2`, ...); asking the array
  _where_ a value lives (`array.index`) is an O(n) scan that throws away the entire reason you
  built the set. Longest Consecutive Sequence.
- **append vs indexed assignment** — `append` builds in _walk order_ and grows the list; `arr[i] = x`
  builds in _position order_ but needs the slot to already exist (pre-size the list). Use indexed
  assignment when walk direction != storage order. (Product Except Self right-pass.)
- **List-then-join over repeated string `+=`** — string `+=` in a loop is secretly O(n^2) (every
  concatenation re-copies everything accumulated so far, since strings are immutable). Collect
  pieces in a list (cheap, amortized O(1) appends) and `"".join(...)` once at the end for O(n).

### Complexity-reasoning lessons

- **Big-O != speed.** Constant factors matter at small sizes — C built-ins (`sorted`) beat Python-loop
  counting even when the loop is asymptotically better (Group Anagrams).
- **Nested loops are NOT always O(n^2).** Sum the _total_ inner executions, don't multiply outer x
  inner. A loop over a partition of the data (each item in exactly one inner pass) is O(n) (bucket
  sort, Longest Consecutive Sequence). Sequential passes ADD (O(n)); nested passes MULTIPLY (O(n^2)).
- **"While inside for" tells you NOTHING by itself.** The shape isn't the complexity. What matters
  is whether the inner work _shrinks as the outer advances_. Longest Consecutive Sequence's inner
  walk fires only n times **in total** across the whole run (partition) = O(n). Contrast a
  matrix-multiply's inner loop, which does full work for every outer step — that one really is
  cubic. **To tell them apart, count total inner executions on a small concrete input.**
- **Fencepost family.** length vs last-index; need `n+1` slots for indices `0..n`; counting **edges**
  (hops between items) vs **nodes** (the items themselves). Recurs everywhere.
- **Space-time tradeoffs are real, but not everywhere.** Fewer memory passes vs. less peak memory
  used (Valid Sudoku's one-pass vs three-pass) is a genuine tradeoff. So is set-vs-sort in Longest
  Consecutive Sequence (O(n) time + O(n) space, vs O(n log n) time + O(1) space). Not every "spend
  space to save time" situation is a dial, though — PEP 393 spends space to _preserve a fixed
  guarantee_ (O(1) string indexing), which isn't the same thing as a tunable tradeoff.

### Debugging lessons

- **Python has no `-Wall`.** In C the compiler is my first reviewer; in Python, **running the code
  against edge cases IS the compiler.** The standing checklist that would have caught _every_ bug
  in Longest Consecutive Sequence: **empty · single element · all singletons · duplicates ·
  negatives · reverse-sorted input.**
- **If every fix reveals a new bug, the IDEA is wrong, not the code.** Longest Consecutive
  Sequence's first approach needed front-extension, then merging, then merging-of-merges — that
  parade was the signal to stop patching and re-read what was actually being asked.
- **Don't build what you weren't asked for.** If the question wants a _measurement_, don't
  construct the _structure_. Every piece of structure you build is a new bug surface. (LCS asks
  for a length; I built lists of sequences.)
- **Check a pattern's prerequisites before reaching for it.** Counter-with-reset needs adjacency
  in the input to _mean_ something. In LCS the array is an unordered bag, so the pattern was
  meaningless there — until sorting made it valid.
- **Make the bug unwriteable, don't just fix it.** `while True` + a hand-placed `break` is what
  _allows_ the exit to be attached to the wrong condition. `while <condition>` removes the
  possibility entirely. Prefer restructuring over patching.
- **A better structure can delete an edge case.** Rewriting LCS for O(1) space turned
  "`max([])` crashes on empty input" into "`return 0`" for free — no special branch needed.

---

### Arrays & Hashing

| #   | Problem                                                              | Approaches                                                                                                                     | Optimal                                                                                      | Cold re-solve |
| --- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------- |
| 1   | [Two Sum](./0001-two-sum/)                                           | brute · one-pass hashmap                                                                                                       | O(n) time / O(n) space (hashmap)                                                             | ⬜            |
| 36  | [Valid Sudoku](./0036-valid-sudoku/)                                 | three-pass (row/col/box) · single-pass (3 sets per cell)                                                                       | O(1) time (fixed 9x9 board) — single-pass trades more peak memory for fewer memory passes    | ⬜            |
| 49  | [Group Anagrams](./0049-group-anagrams/)                             | sort-key · count-key                                                                                                           | O(n·k) time / O(n·k) space (sort-key wins in practice)                                       | ⬜            |
| 128 | [Longest Consecutive Sequence](./0128-longest-consecutive-sequence/) | build-sequences (broken) · counter over array order (broken) · hop by index (broken) · sort+scan · **set + chain-start guard** | O(n) time / O(n) space (set + chain-start guard) — sort+scan is O(n log n) time / O(1) space | ⬜            |
| 217 | [Contains Duplicate](./0217-contains-duplicate/)                     | brute · sort · dict · set                                                                                                      | O(n) time / O(n) space (set)                                                                 | ⬜            |
| 238 | [Product of Array Except Self](./0238-product-of-array-except-self/) | brute (del/insert) · prefix products (2 arrays) · in-place                                                                     | O(n) time / O(1) extra space (in-place prefix products)                                      | ⬜            |
| 242 | [Valid Anagram](./0242-valid-anagram/)                               | sort · Counter · 1-liner · build-dict · one-dict ±→0 · 26-slot list                                                            | O(n) time / O(1) space (26-slot list)                                                        | ⬜            |
| 271 | [Encode and Decode Strings](./0271-encode-decode-strings/)           | naive delimiter (broken) · length-prefixing                                                                                    | O(n) time / O(n) space (length-prefixed, list+join for encode)                               | ⬜            |
| 347 | [Top K Frequent Elements](./0347-top-k-frequent-elements/)           | max+delete · bucket sort                                                                                                       | O(n) time / O(n) space (bucket sort)                                                         | ⬜            |

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
| --- | ------------------------------------------------------ | -------------------------------- | ---------------------------------------- | ------------- |
| 14  | [Longest Common Prefix](./0014-longest-common-prefix/) | hashmap (failed) · vertical scan | O(n·m) time / O(1) space (vertical scan) | ⬜            |

---

## Why this repo exists

Anyone can collect green checkmarks. This repo is proof of something rarer: that for each
problem I can write multiple correct solutions, reason about their time/space tradeoffs,
choose the optimal one deliberately, and explain all of it clearly. That reasoning — not the
accepted submission — is what actually transfers to an interview and to real engineering.

**Principle:** understand it completely, or it doesn't count.
