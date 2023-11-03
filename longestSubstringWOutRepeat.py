from collections import defaultdict


def lengthOfLongestSubstring(s):
    if len(s) < 2:
        return len(s)
    j, k = 0, 1
    letters = defaultdict(int)
    letters[s[j]] += 1
    res = 1
    while k < len(s):
        if s[k] in letters:
            while True:
                if s[j] != s[k]:
                    letters.pop(s[j])
                    j += 1
                else:
                    letters.pop(s[j])
                    j += 1
                    break
        letters[s[k]] += 1
        k += 1
        res = max(res, len(letters))
    return res


test1 = "abcabcbb"
test2 = "bbbbb"
test3 = "pwwkew"
test4 = "au"
test5 = "dvdf"
test6 = "qrsvbspk"

if __name__ == "__main__":
    print(lengthOfLongestSubstring(test6))
