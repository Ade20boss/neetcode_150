# LeetCode 271 -- Encode and Decode Strings: My Notes (Built From The Ground Up)

My own notes, written so that reading this cold -- next week, next year, whenever -- rebuilds the full understanding from nothing. This problem is a DIFFERENT KIND of problem from the ones before it: not an algorithm-optimization problem, but a PROTOCOL / SERIALIZATION DESIGN problem. That distinction matters and is explained below.

## The problem, stated plainly

Design two functions:

- `encode(list_of_strings) -> one_string` -- packs a list of strings into a single string.
- `decode(one_string) -> list_of_strings` -- unpacks it back into the original list.

Requirement: `decode(encode(strs)) == strs` for ANY list of strings -- including strings that contain weird characters, empty strings, or strings that contain whatever delimiter you choose to use internally.

## Why this is NOT a "pattern" problem (and why that's worth noticing)

Every problem before this one (Two Sum, Group Anagrams, Product Except Self, Valid Sudoku) had an underlying ALGORITHMIC pattern -- hash-map lookup, prefix accumulation, 2D-to-1D flattening. This problem has none of that. There is no clever trick that makes it faster; the "hard part" is entirely about DESIGN and PRECISE IMPLEMENTATION: can you invent an unambiguous format for packing variable-length data into a flat string, and can you correctly track your position while parsing your own format back out? This is the same skill CS:APP's networking chapter calls a PROTOCOL's "syntax" component -- an agreed-upon byte layout that both sides (encoder and decoder) trust completely. Recognizing "this problem doesn't fit my usual pattern list" was itself the right call -- not every problem is a DSA-pattern problem; some are precision/design problems.

---

# PART 1 -- Why the obvious first idea (join with a delimiter) breaks

The naive instinct: pick a separator character (say `,`), and do `",".join(strs)` to encode, `.split(",")` to decode. This breaks the moment ANY string in the list already contains a `,` -- the decoder has no way to tell "this comma was YOUR delimiter" from "this comma was part of someone's actual word." The delimiter and the content share the same character space, so there's inherent ambiguity. Any fixed "reserved character" approach has this exact flaw, no matter what character you pick -- someone's string could always contain it.

## The fix: length-prefixing (a self-describing format)

Instead of relying on a delimiter to say "the word ends HERE," tell the decoder, up front, EXACTLY how many characters to read: `<length>#<content>`. The decoder never has to guess where a word ends -- it reads a length, then blindly consumes EXACTLY that many characters, no matter what those characters are (even if they include `#` or digits that would otherwise look like another length-prefix). This is why it's safe even for a word like `"5#weird#stuff"` -- the decoder already knows (from the length) exactly how many characters belong to this word, so it never tries to interpret the `#` or digits INSIDE the content as anything special.

The `#` here is NOT playing the same fragile role as the naive delimiter -- it's only ever used to separate the length DIGITS from the content, and the decoder never searches for it inside content it's already committed to reading a fixed number of characters from.

---

# PART 2 -- The `encode` function

## First version (correct, but hiding a real inefficiency)

```python
def encode(array):
    encoded_str = ""
    for word in array:
        word_length = len(word)
        encoded_string = str(word_length) + "#" + word
        encoded_str += encoded_string
    return encoded_str
```

For each word: compute its length, build `"<length>#<word>"`, and append that to the running output string. Correct -- verified against empty strings, strings containing `#` and digits, and empty lists.

**The hidden cost: `encoded_str += encoded_string` inside a loop is secretly O(n^2), not O(n).** Strings are IMMUTABLE (connects directly to the Python-internals quiz) -- every `+=` does NOT modify the existing string in place. It builds a BRAND NEW string object, and to do that it must COPY every character that was already accumulated, plus the new piece, into that new object. So on the k-th word, the `+=` doesn't just add the new piece cheaply -- it RE-COPIES all `k-1` previously-accumulated pieces into a fresh object. Summed across the whole loop, that's `1 + 2 + 3 + ... + n` units of copy-work, which sums to roughly `n^2 / 2`. **The naive version is O(n^2) in the total output length, even though it "only loops once" -- the hidden cost is inside the `+=`, not visible in the loop structure itself.**

## Optimized version: build a list, join once at the end

```python
def encode(array):
    encoded_str = []
    for word in array:
        word_length = len(word)
        encoded_string = str(word_length) + "#" + word
        encoded_str.append(encoded_string)
    return "".join(encoded_str)
```

**Why this is genuinely O(n), not O(n^2) -- the precise mechanism:**

- `list.append(...)` does NOT have the immutable-string problem. Lists are MUTABLE, so appending is amortized O(1) per call -- the list occasionally has to resize/over-allocate under the hood (exactly the over-allocation behavior from the Python-quiz notes: reserving extra POINTER slots ahead of need), but that resizing is rare and cheap RELATIVE to the growing content -- it is NOT "copy everything accumulated so far" on every single append, unlike string `+=`. Building the whole `encoded_str` list costs O(n) total, not O(n^2).
- `"".join(encoded_str)` does the expensive string-assembly work exactly ONCE, at the very end, instead of once per iteration. Because `join` is handed the COMPLETE list of pieces up front, it can calculate the total final length in one pass and allocate exactly ONE string object of the right size, then copy each piece into it exactly once. That's O(n) total for the join step.
- **Total: O(n) for building the list + O(n) for the single join = O(n) overall**, instead of the original's O(n^2).

**The general lesson (a real, widely-used Python idiom, not just specific to this problem):** NEVER repeatedly `+=` onto a string inside a loop if the loop could run many times or the pieces could be large -- collect the pieces in a LIST instead, and call `"".join(...)` once at the end. This is the exact same underlying principle as understanding WHY list over-allocation exists (mutability enables cheap incremental growth) contrasted with WHY tuples/strings can't do that (immutability means "changing" is definitionally "making an entirely new object"). Recognizing "this loop has a hidden O(n^2) cost buried inside an innocent-looking `+=`" is a genuinely valuable pattern-recognition skill, and it transfers to every language with immutable strings, not just Python.

**Practical calibration:** for LeetCode-scale inputs, this difference is very unlikely to be measurable (same caveat as the Sudoku single-pass-vs-three-pass discussion) -- but the HABIT of reaching for list-then-join over repeated string concatenation matters a lot once inputs get large in real systems work, and the underlying reasoning (mutable vs immutable growth cost) is worth having cold, not just "trust me, it's faster."

---

# PART 3 -- The `decode` function, one invariant at a time

```python
def decode(enc):
    if enc == "":
        return []
    array = []
    i = 0
    while True:
        current_pos = i
        digits_stop = enc.find("#", i)
        digits_range = digits_stop - current_pos
        word_length = ""
        for j in range(digits_range):
            word_length += enc[current_pos + j]
        word_length = int(word_length)
        word = ""
        for k in range(word_length):
            word += enc[digits_stop + k + 1]
        array.append(word)
        i += digits_range + 1 + word_length
        if i == len(enc):
            return array
```

## The core invariant that makes this whole function work

**At the TOP of every loop iteration, `i` is guaranteed to be sitting at the START of a length-prefix -- never mid-word, never at a `#`, never anywhere else.** This is not an accident -- it's ENGINEERED, entirely by how `i` gets advanced at the bottom of each iteration:

```python
i += digits_range + 1 + word_length
#      ^skip digits  ^skip "#"  ^skip exactly the content
```

Because `encode` writes EXACTLY `word_length` characters of content (no more, no less), this jump lands EXACTLY on the boundary where the NEXT length-prefix begins. The whole function's correctness rests on this single invariant being upheld every iteration -- it's the same idea as a network protocol: both sides (encoder and decoder) trust an agreed-upon layout completely, and if either side ever violated it (e.g. encode adding a stray trailing space "for readability"), decode would break immediately and non-obviously.

## Step-by-step, what each line does

1. **`current_pos = i`** -- save where THIS word's length-prefix starts, before anything moves.
2. **`digits_stop = enc.find("#", i)`** -- find the next `#`, starting the SEARCH from `i` (not from the beginning of the string -- this is what keeps the whole decode O(N) instead of accidentally rescanning from position 0 every time).
3. **`digits_range = digits_stop - current_pos`** -- how many digit characters make up the length (the gap between where we started and where the `#` was found).
4. **The digit-extraction loop** (`for j in range(digits_range): word_length += enc[current_pos + j]`) -- walk forward `digits_range` characters STARTING FROM `current_pos`, building up the length as a string of digits, one character at a time.
5. **`word_length = int(word_length)`** -- convert the digit-string into an actual usable integer count.
6. **The character-extraction loop** (`for k in range(word_length): word += enc[digits_stop + k + 1]`) -- the word's content starts right after the `#` (`digits_stop + 1`), and walks forward `k` steps from there, reading exactly `word_length` characters.
7. **`array.append(word)`** -- save the fully decoded word.
8. **`i += digits_range + 1 + word_length`** -- advance `i` past (digits + `#` + content), landing exactly at the start of the next length-prefix -- restoring the invariant for the next loop.
9. **`if i == len(enc): return array`** -- stop once every character of the encoded string has been consumed.

## Bugs I actually hit, and why each one happened (worth remembering the SHAPE of these)

**Bug 1 -- variable collision.** My first attempt used the SAME name (`i`) for both the outer "current position" tracker AND an inner loop's counter (`for i in range(digits_range)`). The inner loop silently overwrote the outer `i`, destroying my position tracker. Fix: give inner loops their OWN distinct names (`j`, `k`) so they can never collide with a variable something else depends on. **General lesson: any time a loop variable shares a name with something used outside that loop, that's a landmine, even if it looks fine at a glance.**

**Bug 2 -- index doesn't use the loop variable.** `word += enc[digits_stop + 1]` inside `for k in range(word_length)` -- `k` counts correctly (0 through word_length-1) but is never actually REFERENCED in the index expression, so the same character gets read repeatedly instead of advancing. Fix: `enc[digits_stop + 1 + k]`. **General lesson: having the RIGHT NUMBER of loop iterations doesn't guarantee correctness -- the loop variable must actually be used inside the loop body for anything to change between iterations.**

**Bug 3 -- index doesn't account for current position.** The digit-extraction loop read `enc[j]` instead of `enc[current_pos + j]` -- meaning it ALWAYS read starting from the very beginning of the whole string, regardless of which word was currently being decoded. Worked correctly for the FIRST word (where current_pos happens to be 0) and silently produced wrong results for every word after that. **General lesson: a bug that only shows up on the SECOND iteration of an outer loop (not the first) is a strong signal that some value which should depend on "where am I right now" is instead hardcoded to "the very beginning."** This bug also didn't crash where it happened -- it crashed several steps LATER (an IndexError from reading too far, once the wrong length caused an out-of-bounds read). **A crash's location is not always where the actual mistake was made -- trace upstream.**

**Bug 4 -- missing edge case: the empty container itself.** `decode("")` (from `encode([])`) crashed, because `enc.find("#", 0)` returns `-1` when nothing is found (not an error, just a sentinel value), which corrupted the downstream arithmetic. I had already correctly handled empty STRINGS mixed into a non-empty list (`["", "a", ""]`) -- the harder case -- but missed the empty LIST case entirely. Fix: an explicit guard, `if enc == "": return []`, before the loop. **General lesson: there are TWO different axes of edge case -- "weird content inside an element" (which I handled well) and "the container itself being empty/trivial" (which I initially missed). Checking one doesn't guarantee the other is covered.**

---

# PART 4 -- Complexity

Let N = total length of the encoded string (roughly the sum of all original word lengths, plus a little for the length-prefixes and `#` separators).

**`encode` is O(N) with the list-and-join version; the naive `+=` version is actually O(N^2)** (see Part 2 for the precise reasoning) -- each word's characters get copied into the growing output exactly once with `append`+`join`, versus repeatedly re-copied with naive string `+=`.

**`decode` is O(N), NOT O(N^2):** the key reason is that `enc.find("#", i)` is always told to start searching FROM the current position `i`, never from the beginning. Combined with the fact that every character-extraction loop only ever reads forward from where it currently is, every single character in the encoded string gets visited EXACTLY ONCE across the entire decode process -- there is no backtracking, no rescanning from the start. (A naive implementation that searched for `#` starting from index 0 every time WOULD risk degrading toward O(N^2) territory -- the "continue from where you left off, never restart the scan" discipline is what keeps this linear.)

---

# The one-paragraph version (for instant recall)

> Encode/Decode Strings is a protocol-design problem, not an algorithm-pattern problem: a naive delimiter-join breaks because a word could contain the delimiter itself, so the fix is LENGTH-PREFIXING -- `<length>#<content>` -- a self-describing format where the decoder never needs to guess where a word ends, it just reads a length and then blindly consumes exactly that many characters, whatever they are. The decoder's entire correctness rests on ONE invariant, engineered by the advance step `i += digits_range + 1 + word_length`: at the top of every loop iteration, the current position `i` is guaranteed to sit exactly at the start of the next length-prefix, because the encoder wrote exactly `word_length` characters of content and the decoder skips exactly that many. The real difficulty in this problem isn't conceptual -- it's precise index bookkeeping: making sure inner loop variables never collide with outer position trackers, making sure a loop variable is actually USED inside the index expression it's supposed to advance, making sure every index is computed relative to the CURRENT word's position rather than the start of the whole string, and remembering to guard the "empty container" edge case (not just "empty element inside a container") before entering the main loop. Because `find()` is always told to search starting from the current position rather than from the beginning, and every extraction loop only reads forward, the whole decode runs in O(N) -- every character of the encoded string gets visited exactly once, never revisited.