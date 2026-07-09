# LeetCode 49 — Group Anagrams: My Notes

Group a list of strings so that anagrams are bucketed together.
`["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"],["tan","nat"],["bat"]]`.

The core idea: **give every word a "signature" that is identical for anagrams, then use that
signature as a hash-map key.** Words with the same signature land in the same bucket. The two
approaches differ only in *how they compute the signature.*

---

## The two approaches

### 1. Sort-based signature
```python
def group_anagrams_sort(array):
    hash_map = dict()
    for word in array:
        key = "".join(sorted(word))          # signature = sorted letters
        if hash_map.get(key, 0) == 0:
            hash_map[key] = [word]
        else:
            hash_map[key].append(word)
    return list(hash_map.values())
```
Signature = the word's letters sorted. `"eat"`, `"tea"`, `"ate"` all sort to `"aet"`, so they
share a key. The sorted string is hashable, so it works directly as a dict key.
- Time: **O(n · k log k)** — n words, each of length k, sorting each is k log k.
- Space: O(n · k).

### 2. Count-based signature
```python
def group_anagrams_count(array):
    hash_map = dict()
    for word in array:
        key = [0] * 26
        for char in word:
            key[ord(char) - ord("a")] += 1   # signature = letter counts
        key = tuple(key)                       # list isn't hashable; tuple is
        if hash_map.get(key, 0) == 0:
            hash_map[key] = [word]
        else:
            hash_map[key].append(word)
    return list(hash_map.values())
```
Signature = a 26-slot count of each letter. Anagrams have identical counts, so identical signatures. **Key detail: must convert the count `list` to a `tuple`** — a list is mutable and therefore *unhashable*, so it can't be a dict key; a tuple is immutable and hashable. (This connects to my Python internals notes: mutable = unhashable, immutable = hashable.)
- Time: **O(n · k)** — n words, each of length k, one pass to count. No log factor.
- Space: O(n · k).

---

## The interesting part: why "count" was SLOWER than "sort" on LeetCode (theory vs practice)

By **big-O, count should be faster**: O(n·k) beats O(n·k·log k) — counting has no log factor.
So I expected `group_anagrams_count` to win. But on LeetCode (and when I timed it locally),
**sort was actually faster.** I measured it: on 20,000 random words, sort ≈ 0.12s, count ≈
0.21s. Count was almost 2× SLOWER despite the better complexity. Why?

**The answer is constant factors and where the work runs:**
1. **Python-level loops are slow; C-level built-ins are fast.** `sorted()` and `"".join()`
   are implemented in C and run at C speed. My count approach uses an **explicit Python `for`
   loop** over every character (`for char in word: key[...] += 1`). Python-level loops have
   heavy per-iteration overhead (bytecode dispatch, object boxing). So even though count does
   *fewer operations* in theory, each operation is far more expensive because it runs in the
   Python interpreter instead of in C.
2. **k is tiny.** The words are short (k ≈ a handful of letters). `log k` for k=5 is ~2.3 —
   basically nothing. So the "advantage" of dropping the log factor is negligible, while the
   Python-loop overhead of the count approach is very real. When k is small, O(n·k·log k) and
   O(n·k) are practically the same, and the constant factor decides the race.
3. **Building a 26-element list + tuple per word** has its own overhead (allocating a list,
   filling 26 slots even for a 3-letter word, converting to tuple). Sort just makes one small
   sorted string.

**The lesson (this is the money insight):** *big-O tells you how something scales, not how
fast it is at a given size.* For large k, count's O(n·k) would eventually win. But for the
small k in this problem, the **constant factors** — C-speed built-ins vs Python-speed loops —
dominate, and sort wins in practice. **Asymptotic complexity and real-world speed are
different questions, and both matter.** The "theoretically better" algorithm lost because its
constant factor was worse at this scale.

(A faster count version would use `collections.Counter` or avoid the per-char Python loop —
pushing the work back into C. The slowness isn't inherent to counting; it's inherent to
doing the counting in an explicit Python loop.)

---

## Key details I hit
- **List → tuple for the key.** The count signature is a list, which is unhashable (mutable).
  Convert to `tuple` to use it as a dict key. Forgetting this throws `TypeError: unhashable
  type: 'list'`.
- **`hash_map.get(key, 0) == 0` to branch first-time vs append** — check if the bucket exists;
  create `[word]` if not, else `.append(word)`. (Could simplify with `dict.setdefault` or
  `collections.defaultdict(list)`, which removes the if/else entirely.)
- **`ord(char) - ord('a')`** — same letter-to-index trick as the 26-slot anagram solution.

## Lessons (bigger than this problem)
1. **Signature/canonical-key pattern:** to group "equivalent" things, map each to a canonical
   key and bucket by it. Reusable for tons of grouping problems.
2. **Big-O ≠ speed.** Count is asymptotically better but practically slower here, because
   constant factors (Python loop vs C built-in) dominate at small k. Measure, don't assume.
3. **C-level built-ins beat Python-level loops.** When performance matters in Python, push
   work into built-ins (`sorted`, `Counter`, `join`) instead of hand-rolled `for` loops.
4. **Mutable = unhashable.** A list can't be a dict key; a tuple can. Core Python internals.

## Say-it-out-loud summary
> "I give each word a signature that's identical for anagrams, then bucket by it in a hash
> map. Signature is either the sorted letters (O(n·k log k)) or a 26-count tuple (O(n·k)).
> Count is theoretically faster, but in practice sort won on LeetCode because k is tiny so the
> log factor is negligible, and `sorted` runs in C while my count loop runs in the Python
> interpreter — so constant factors dominated and the C built-in beat the hand-written loop."
