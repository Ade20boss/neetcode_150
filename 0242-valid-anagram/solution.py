from collections import Counter


def is_anagram_optimal(s: str, t: str):
    if len(s) != len(t):
        return False
    s_freq = Counter(s)
    t_freq = Counter(t)
    for i in s:
        if s_freq[i] != t_freq[i]:
            return False
    return True


def is_anagram_optimal_one_liner(s: str, t: str):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)


def is_anagram_naive(s: str, t: str):
    return sorted(t) == sorted(s)


def is_anagram_build_dict(s: str, t: str):
    if len(s) != len(t):
        return False
    s_freq = dict()
    t_freq = dict()

    for i in range(len(s)):
        s_freq[s[i]] = s_freq.get(s[i], 0) + 1
        t_freq[t[i]] = t_freq.get(t[i], 0) + 1

    return s_freq == t_freq


def is_anagram_one_dict(s: str, t: str):
    if len(s) != len(t):
        return False

    s_freq = dict()

    for i in range(len(s)):
        s_freq[s[i]] = s_freq.get(s[i], 0) + 1
        s_freq[t[i]] = s_freq.get(t[i], 0) - 1

    for j in s_freq:
        if s_freq[j] != 0:
            return False
    return True


def is_anagram_char_list(s: str, t: str):
    if len(s) != len(t):
        return False

    s_list = [0] * 26
    t_list = [0] * 26

    for i in range(len(s)):
        s_list[ord(s[i]) - ord("a")] += 1
        t_list[ord(t[i]) - ord("a")] += 1

    return s_list == t_list
