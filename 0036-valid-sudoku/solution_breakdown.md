# LeetCode 36 — Valid Sudoku: My Notes (Built From The Ground Up)

My own notes, written so that reading this cold — next week, next year, whenever — rebuilds the
full understanding from nothing. Every idea here is built on the one before it. If any piece ever
feels shaky again, start from the top and walk down; don't skip ahead.

## The problem, stated plainly

You're given a 9x9 grid (`board`), partially filled with digits `1`-`9` and empty cells marked
`"."`. Determine whether the CURRENTLY FILLED cells obey the three Sudoku rules -- you are NOT
being asked to solve the puzzle (fill in the blanks), only to check that what's already there
doesn't break any rule. The three rules:

1. Each **row** contains no repeated digit.
2. Each **column** contains no repeated digit.
3. Each of the nine **3x3 sub-boxes** contains no repeated digit.

If any rule is broken anywhere, the board is invalid. If nothing is broken, it's valid (even if
mostly empty).

---

# PART 1 -- The straightforward approach: three separate passes

## The core tool: a "seen it before" notepad (a `set`)

To check "no repeats in this row," the simplest tool is: walk the row left to right, and for each
digit, ask "have I already written this digit down somewhere earlier in this same row?" If yes --
duplicate, invalid. If no -- write it down, keep going.

"Write it down and check later" is exactly what a `set` is for in code. A set is like a notepad:
`my_set.add(x)` writes `x` on the notepad, and `x in my_set` asks "is `x` already written on this
notepad?" -- both operations are fast (essentially instant, regardless of how many things are
already written down).

## Pass 1 -- check every ROW

```python
for row in board:                 # walk each of the 9 rows, one at a time
    hash_set = set()               # a FRESH, empty notepad for THIS row
    for value in row:               # walk every cell in this row, left to right
        if value == ".":
            continue                # empty cell -- nothing to check, skip it
        if value in hash_set:
            return False             # already saw this digit in this row -- invalid!
        else:
            hash_set.add(value)      # first time seeing it -- write it down
```

Notice: `hash_set = set()` is placed INSIDE the outer loop (`for row in board`) -- a fresh, EMPTY
notepad is created at the start of every single row, and thrown away at the end of it. This is
safe and correct because **a row's own numbers must never be confused with a different row's
numbers** -- row 0 having a "5" and row 1 also having a "5" is perfectly legal, so each row needs
its own private, wiped-clean notepad.

## Pass 2 -- check every COLUMN

Same exact idea, but walking column by column instead of row by row:

```python
for col_index in range(9):          # for each of the 9 columns...
    hash_set = set()                 # fresh notepad for THIS column
    for row in board:                 # walk every row, but only look at THIS column's cell
        value = row[col_index]
        if value == ".":
            continue
        if value in hash_set:
            return False
        else:
            hash_set.add(value)
```

The only difference from Pass 1: instead of walking `for value in row` (every cell of one row),
we walk `for row in board` and pick out `row[col_index]` each time (one specific column, across
every row). Same check-then-remember logic, just aimed at a different "unit" (column instead of
row).

## Pass 3 -- check every 3x3 BOX (this is where it gets genuinely new)

This needs its own explanation -- see PART 2 below for the full derivation of the box math. The
short version: there are 9 boxes, and for box number `b` (0 through 8), its top-left corner cell
sits at row `(b // 3) * 3` and column `(b % 3) * 3`. Walk a 3x3 block starting from that corner:

```python
for b in range(9):
    row_start = (b // 3) * 3
    col_start = (b % 3) * 3
    hash_set = set()
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            value = board[r][c]
            if value == ".":
                continue
            if value in hash_set:
                return False
            else:
                hash_set.add(value)
return True
```

**This three-pass version is correct and complete.** It walks the board three separate times --
once organized by row, once by column, once by box -- and each time, because the "unit" being
checked matches the walk's own organization, a single reusable notepad (reset at the start of
each unit) is enough.

---

# PART 2 -- Deriving the box-index math from first principles

This was the hard part, and it deserves the full derivation, because the formula is meaningless
without the picture behind it.

## Step 1 -- see the 9 boxes as their own tiny 3x3 grid

A 9x9 Sudoku board, when you look at the bold dividing lines printed on any real Sudoku puzzle,
splits into a 3x3 arrangement of fat squares (each fat square = one 3x3 box):

```
+-------+-------+-------+
| box A | box B | box C |      <- top band of boxes
+-------+-------+-------+
| box D | box E | box F |      <- middle band of boxes
+-------+-------+-------+
| box G | box H | box I |      <- bottom band of boxes
+-------+-------+-------+
```

There are 9 boxes total, arranged in their OWN 3x3 grid (a grid of boxes, not of cells). This
tiny grid has row-bands (top/middle/bottom) and column-bands (left/middle/right), exactly like
the big board has rows and columns -- just at a coarser scale.

## Step 2 -- figure out which BAND a given row or column falls into

Rows 0, 1, 2 belong to the TOP band of boxes. Rows 3, 4, 5 belong to the MIDDLE band. Rows 6, 7, 8
belong to the BOTTOM band. Same idea for columns: 0,1,2 = left band; 3,4,5 = middle band; 6,7,8 =
right band.

**The math trick: dividing by 3 and throwing away the remainder (integer division, `//` in
Python) turns any row number into its band number.**

```
0 // 3 = 0     1 // 3 = 0     2 // 3 = 0      <- all band 0 (top)
3 // 3 = 1     4 // 3 = 1     5 // 3 = 1      <- all band 1 (middle)
6 // 3 = 2     7 // 3 = 2     8 // 3 = 2      <- all band 2 (bottom)
```

So: **`row // 3` = which row-band (0, 1, or 2) a given row belongs to.** Same formula for columns:
**`col // 3` = which column-band.**

Concretely: cell `(4, 7)` -> `row_band = 4 // 3 = 1` (middle), `col_band = 7 // 3 = 2` (right).

## Step 3 -- flatten the 2D band-coordinate into a single box number 0-8

Now you have a coordinate INSIDE the tiny 3x3 box-grid: `(row_band, col_band)`. We want to number
the nine boxes 0 through 8, reading left-to-right, top-to-bottom, like numbering pages in a book:

```
(0,0)=0   (0,1)=1   (0,2)=2
(1,0)=3   (1,1)=4   (1,2)=5
(2,0)=6   (2,1)=7   (2,2)=8
```

**Hand-count the pattern:** starting at `(0,0)=0`, moving along a row adds 1 each time
(`(0,1)=1`, `(0,2)=2`). But when you WRAP to the next row-band, the count doesn't reset to 0 --
it CONTINUES from where it left off (`(1,0)=3`, not 0), because we're numbering ALL nine boxes in
one continuous sequence, not restarting per row-band.

**Why does row-band 1 start at 3, and row-band 2 start at 6?** Because each row-band holds
EXACTLY 3 boxes. To reach row-band 1, you must first pass all 3 boxes of row-band 0. To reach
row-band 2, you must pass all 3+3=6 boxes of row-bands 0 and 1. So: **skipping one whole
row-band costs exactly 3 in the count.**

This gives the formula:

```
box_number = (row_band x 3) + col_band
```

"Skip 3 for every full row-band already passed, then add how far along the CURRENT row-band you
are."

**Verify EVERY one of the nine by hand, so nothing is taken on faith:**

```
(0,0): 0x3 + 0 = 0   OK
(0,1): 0x3 + 1 = 1   OK
(0,2): 0x3 + 2 = 2   OK
(1,0): 1x3 + 0 = 3   OK
(1,1): 1x3 + 1 = 4   OK
(1,2): 1x3 + 2 = 5   OK
(2,0): 2x3 + 0 = 6   OK
(2,1): 2x3 + 1 = 7   OK
(2,2): 2x3 + 2 = 8   OK
```

Every one matches the hand-count from Step 3's opening picture. The formula is not magic -- it's
a shortcut for "count whole row-bands skipped (x3 each) plus how far into this row-band."

**A physical anchor if this ever goes fuzzy again:** a bookshelf with 3 books per shelf, books
numbered continuously 0-8 across all shelves. To find "shelf 1, 2nd book along": skip all of
shelf 0 entirely (3 books) to even REACH shelf 1, then walk 2 more books along shelf 1. Skip a
whole shelf = x3. Walk along the current shelf = +position. Identical structure to the box math.

## Step 4 -- putting steps 2 and 3 together: cell -> box, in one formula

Combining "shrink a cell coordinate into a band coordinate" (Step 2) with "flatten a band
coordinate into a box number" (Step 3):

```
box_index = (row // 3) * 3 + (col // 3)
             \________/        \________/
            row_band          col_band
        (Step 2 shrink)    (Step 2 shrink)
             \_________ Step 3 flatten _________/
```

**Full worked example, cell `(4, 7)`:**

- `row // 3 = 4 // 3 = 1` -> row-band 1 (middle band)
- `col // 3 = 7 // 3 = 2` -> col-band 2 (right band)
- `box_index = 1 * 3 + 2 = 5`

Check against the picture: middle row-band, right column-band -> that's the box labeled "F" in
Step 1's picture (6th one, reading left-right-top-bottom, counting from 0 as the 5th index) --
matches.

**Second worked example, cell `(0, 0)`** (top-left corner of the whole board):

- `row // 3 = 0`, `col // 3 = 0`
- `box_index = 0*3 + 0 = 0` -- the very first box, top-left. Matches intuition exactly (the
  top-left cell of the whole board is obviously in the top-left box).

---

# PART 3 -- The single-pass version (checking all three rules while walking the board ONCE)

## The idea: don't walk the board three times -- walk it once, checking three things per cell

Instead of three separate loops (one per rule), walk the board with ONE nested loop
(`for row: for col:`), and at EVERY cell, check all three rules simultaneously, using three
SEPARATE sets of notepads:

- **9 row-notepads** (but see the optimization below -- really just 1, reused)
- **9 column-notepads** (`cols = [set() for _ in range(9)]`)
- **9 box-notepads** (`boxes = [set() for _ in range(9)]`)

## Why you need MULTIPLE separate notepads per unit-type (not just one shared notepad)

Every unit (a specific row, a specific column, a specific box) has its OWN independent rule --
row 0's "already seen a 5" must never be confused with row 1's, and the same is true across
columns and boxes. If everything shared ONE notepad, a legitimate "5" in row 1 would incorrectly
look like a duplicate of the legitimate "5" already seen in row 0. So each unit needs its own
memory, kept completely separate from every other unit's memory -- hence 9 separate notepads per
unit-type.

## Why ROWS can get away with just ONE reusable notepad, but columns and boxes cannot

Walking the board with `for row in range(9): for col in range(9):` means: finish ALL of row 0's
cells (columns 0 through 8), THEN move to row 1. **A row is entirely finished before the walk
ever moves to the next row.** So it's safe to use ONE notepad for rows, wiping it clean at the
START of every row's inner loop -- by the time you'd need row 0's data again, you never do,
because row 0 is permanently done.

**Columns and boxes are different.** Walking row-by-row means you touch column 0 at `(0,0)`, then
DON'T touch column 0 again until `(1,0)` -- nine cells later, after touching all 8 OTHER columns
in between. **No column is ever "finished" until the very last row of the whole board.** All 9
columns are simultaneously "in progress" the entire time. The same is true for boxes -- you're
partway through several boxes at once throughout the whole walk. Because they're never finished
one-at-a-time, you cannot safely reset a shared notepad for columns or boxes -- you need 9
independent, permanently-alive notepads for each, existing simultaneously for the whole walk.

**The underlying rule: you may only reset-and-reuse a notepad for a unit-type whose units
finish completely, one at a time, in the order you're walking. Units that interleave with the
walk order need their own permanently-separate notepads.**

## The full single-pass code

```python
def valid_sudoku_onepass(board):
    cols  = [set() for _ in range(9)]   # 9 independent column notepads, alive the whole time
    boxes = [set() for _ in range(9)]   # 9 independent box notepads, alive the whole time

    for i in range(len(board)):          # walk each row
        rows = set()                      # ONE row notepad, freshly WIPED at the start of each row
        for j in range(len(board[i])):     # walk each column within this row
            box = ((i // 3) * 3) + (j // 3)   # which box this cell belongs to (Part 2's formula)
            value = board[i][j]

            if value == ".":
                continue                        # empty cell, nothing to check

            if value in rows or value in cols[j] or value in boxes[box]:
                return False                      # duplicate found in ANY of the 3 units -- invalid

            rows.add(value)                        # remember it in THIS row's notepad
            cols[j].add(value)                      # remember it in column j's notepad
            boxes[box].add(value)                    # remember it in this box's notepad
    return True
```

**The bug I actually hit when first writing this:** I wrote the CHECK (`if value in rows or ...`)
but forgot the three `.add(...)` lines entirely. Without writing anything down, the notepads stay
empty forever, so the "have I seen this?" check can never be true, and the function always falls
through to `return True` -- even for boards with obvious duplicates. **Lesson: "check, then
remember" is two separate steps, and it's easy to implement only the check half while focused on
getting the harder math (the box formula) right.** Always verify both halves are present.

---

# PART 4 -- Is the single-pass version actually better? (Space-time tradeoff)

## Same Big-O complexity class

Both versions touch a fixed 81-cell board a constant number of times: 3x for the three-pass
version (243 total cell-visits), 1x for the single-pass version (81 total cell-visits). Since the
board size never changes (always exactly 9x9), both are technically **O(1)** -- or, described more
conventionally in terms of the board's dimension n=9, both are **O(n^2)**. The BIG-O CATEGORY is
identical for both versions.

## But the CONSTANT FACTOR differs -- and this is a genuine, textbook space-time tradeoff

- **Three-pass:** touches memory 3x as much (243 cell-reads instead of 81) -- MORE time-ish work,
  but only ever needs 1 notepad alive at once (reused/reset for each pass) -- LESS peak memory.
- **Single-pass:** touches memory only once (81 cell-reads) -- LESS time-ish work -- but needs up
  to 19 notepads alive SIMULTANEOUSLY (1 reusable row notepad + 9 permanent column notepads + 9
  permanent box notepads) -- MORE peak memory.

This is a genuine space-time tradeoff (unlike, for example, PEP 393's string storage, which
SPENDS space to PRESERVE a fixed time guarantee rather than letting you dial between two
strategies) -- here, BOTH strategies are legitimate, complete solutions, and the choice is a real
dial: fewer memory touches vs. less peak memory used. Neither is "more correct" than the other.

**Honest caveat on "which is actually faster":** for a fixed, tiny 9x9 board, the real-world
timing difference between 81 and 243 memory reads is almost certainly unmeasurable -- both
finish long before you could notice a difference, and the whole board likely sits in cache
either way. The concept (fewer total memory passes tends to be faster, especially once cache
effects matter) is real and worth knowing, but it would only become an ACTUALLY measurable
difference on much larger data (imagine a 9000x9000 grid instead of 9x9).

---

# PART 5 -- Connection to Kestrel: the SAME 2D->1D flattening idea, twice

## The box-index formula IS the same operation as Kestrel's MAT_POS

Kestrel's matrix macro:

```c
#define MAT_POS(m, r, c) ((m).es[(r) * (m).stride + (c)])
```

This turns a 2D coordinate `(r, c)` into a single 1D index into a flat underlying array, using
`row * stride + col`.

The Sudoku box formula:

```python
box_index = (row // 3) * 3 + (col // 3)
```

This turns a 2D box-BAND-coordinate `(row_band, col_band)` into a single 1D index (0-8) into a
flat list of 9 box-notepads, using the exact same shape: `row_component * width + col_component`.

**Both exist for the identical underlying reason: the thing being described is naturally 2D (a
row-and-column position), but the thing being INDEXED INTO is a flat, 1D structure (a flat float
array in Kestrel's case; a flat list of 9 sets in the Sudoku case).** Whenever a 2D idea needs to
address into a 1D structure, this same "row-component x width + col-component" flattening shows
up. It's a completely general pattern, not a coincidence.

## When can you SKIP this math and just loop the raw 1D array directly?

I tested this directly (with real C code) and confirmed: you can ONLY skip the row/col math and
loop a flat array plainly (`for i in range(rows*cols): es[i] = value`) when the matrix/array-view
has NO GAPS -- i.e., when `cols == stride` (every row butts up directly against the next, nothing
skipped). The moment you have a "view" onto part of a bigger structure (like Kestrel's
`row_matricize`, or a sub-selection of only some columns) where `cols < stride`, naively looping
the raw flat array WILL corrupt memory that belongs to OTHER parts of the parent structure -- I
proved this with a real test where a naive flat-loop fill bled into a neighboring row's columns
that were never supposed to be touched. This is exactly why matrix operations always use the
stride-aware `MAT_POS` math unconditionally, even in the common case where it isn't strictly
necessary: it's the only version that's correct for BOTH whole-array views and sliced/limited
views, and a function can't always know in advance which kind of view it'll be given.

---

# The one-paragraph version (for instant recall)

> Valid Sudoku needs three separate checks -- no repeats in any row, column, or 3x3 box -- each
> done with a "seen it before" set (a notepad): check if a value is already in the set, and if
> not, add it. The straightforward solution does three separate passes over the board, one per
> rule, each pass able to reuse a single notepad because the "unit" being checked matches the
> walk's own order. The box-checking pass needs a formula to turn a cell's (row, col) into which
> box it belongs to: `(row // 3) * 3 + (col // 3)` -- first SHRINK the cell coordinate into a band
> coordinate (which third of the rows, which third of the columns) via integer division, then
> FLATTEN that 2D band coordinate into a single 0-8 index via "row_band x 3 + col_band" (skip 3
> for every whole row-band already passed, since each row-band holds 3 boxes, then add how far
> into the current row-band you are) -- this is the EXACT same 2D-to-1D flattening idea as
> Kestrel's `row * stride + col`, just applied to a 3x3 grid of boxes instead of a matrix of
> floats. The single-pass version walks the board only once, checking row/column/box
> simultaneously at every cell, but needs separate, permanently-alive notepads for columns and
> boxes (because they interleave with the row-major walk order and never "finish" one at a time)
> while rows can use just one reusable notepad (because a row IS fully finished before the walk
> moves to the next one) -- this is a genuine space-time tradeoff: fewer total memory touches at
> the cost of more peak memory alive at once, same Big-O complexity class either way.
