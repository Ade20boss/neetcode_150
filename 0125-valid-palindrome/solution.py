"""
LeetCode 125 — Valid Palindrome

A phrase is a palindrome if, after lowercasing and removing every non-alphanumeric
character, it reads the same forward and backward.

    "A man, a plan, a canal: Panama"  ->  "amanaplanacanalpanama"  ->  True
    "race a car"                      ->  "raceacar"               ->  False
    " "                               ->  ""                       ->  True

Two rules that are the whole problem:
  1. only letters and digits count      -> c.isalnum()
  2. case does not matter                -> c.lower()
"""


# ---------------------------------------------------------------------------
# APPROACH 0 — reverse, then read backwards (BROKEN, kept as a record)
# ---------------------------------------------------------------------------
# The idea was: reverse the string, then compare reversed[n-1-i] to s[i].
# It returns True for EVERYTHING, because reversed[n-1-i] IS s[i] — reversing
# and then indexing from the far end are two operations that cancel out. You end
# up comparing s[i] to s[i], which is always equal.
def is_palindrome_broken(s):
    rev = s[::-1]
    n = len(s)
    for i in range(n):
        if rev[n - 1 - i] != s[i]:  # rev[n-1-i] == s[i] ALWAYS -> tautology
            return False
    return True


# ---------------------------------------------------------------------------
# APPROACH 1 — two pointers, skip-in-place (OPTIMAL: O(n) time / O(1) space)
# ---------------------------------------------------------------------------
# One pointer at each end. Skip non-alphanumerics on each side independently,
# compare case-insensitively, walk inward until the pointers meet.
# No cleaned copy is ever built -> O(1) space.
def is_palindrome(s):
    left = 0
    right = len(s) - 1

    while left < right:
        if not s[left].isalnum():  # junk on the left -> ADVANCE, then retry
            left += 1
            continue
        if not s[right].isalnum():  # junk on the right -> ADVANCE, then retry
            right -= 1
            continue

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


# ---------------------------------------------------------------------------
# APPROACH 2 — clean, then compare to its reverse (O(n) time / O(n) space)
# ---------------------------------------------------------------------------
# Build a cleaned, lowercased string; compare to its slice-reverse.
# Readable and idiomatic, but allocates TWO extra strings (cleaned + reversed).
def is_palindrome_oneliner(s):
    cleaned = "".join(c for c in s if c.isalnum()).lower()
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    tests = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
        ("", True),
        (".,", True),  # all junk -> empty -> True
        ("0P", False),  # digit vs letter, case matters
        ("racecar", True),
        ("Was it a car or a cat I saw?", True),
        ("ab_a", True),  # '_' is NOT alnum -> skipped
    ]
    for s, expected in tests:
        a1 = is_palindrome(s)
        a2 = is_palindrome_oneliner(s)
        mark = "OK  " if a1 == a2 == expected else "FAIL"
        print(f"[{mark}] two-ptr={a1!s:<5} clean={a2!s:<5} exp={expected!s:<5} {s!r}")
