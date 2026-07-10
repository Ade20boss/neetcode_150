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

**Solved:** 6 / 150

**Cold re-solve legend:** ✅ can reproduce from scratch · 🔁 needs another cold pass · ⬜ not yet re-solved

_(Problems are grouped below by NeetCode pattern for readability, but each lives in its own
root-level folder.)_

### Arrays & Hashing

| #   | Problem                                                    | Approaches                                                          | Optimal                                                | Cold re-solve |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------ | ------------- |
| 1   | [Two Sum](./0001-two-sum/)                                 | brute · one-pass hashmap                                            | O(n) time / O(n) space (hashmap)                       | ⬜            |
| 49  | [Group Anagrams](./0049-group-anagrams/)                   | sort-key · count-key                                                | O(n·k) time / O(n·k) space (sort-key wins in practice) | ⬜            |
| 217 | [Contains Duplicate](./0217-contains-duplicate/)           | brute · sort · dict · set                                           | O(n) time / O(n) space (set)                           | ⬜            |
| 242 | [Valid Anagram](./0242-valid-anagram/)                     | sort · Counter · 1-liner · build-dict · one-dict ±→0 · 26-slot list | O(n) time / O(1) space (26-slot list)                  | ⬜            |
| 347 | [Top K Frequent Elements](./0347-top-k-frequent-elements/) | max+delete · bucket sort                                            | O(n) time / O(n) space (bucket sort)                   | ⬜            |

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
