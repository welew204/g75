def wordBreak(string, wordDict):
    memo = [False] * (len(string) + 1)
    memo[len(string)] = True
    for i in range(len(string)-1, -1, -1):
        for w in wordDict:
            if i+len(w) <= len(string) and string[i:i + len(w)] == w:
                memo[i] = memo[i + len(w)]
                # ^ this is how we check thru to the end of the string beig True
            if memo[i]:
                # then we don't have to check for more words (if this one IS true, then answer will be the same)
                break

    return memo[0]

    """while ri < len(string):
        current_ss = string[li:ri+1]
        if current_ss in wordDict:
            if current_ss not in memo:
                memo[current_ss] = True
            li = ri+1
            ri += 2
        else:
            ri += 1

    def dfs(li, ri, wordsSeg):
        if ri+1 == len(str):
            # end of string!
            if str[li:] in wordDict:
                # assumes that the only way to have proceeded this far
                # in tree is that previous substrings were in dict
                return True
            else:
                return
        if str[li:ri+1] in wordDict:
            newWordSeg = wordsSeg[:]
            newWordSeg.append(str[li:ri+1])
            dfs(ri+1, ri+2, newWordSeg)
        dfs(li, ri+1, wordsSeg)

    return dfs(0, 1, [])"""


testStr1 = "applepenapple"
testWordDict1 = ["apple", "pen"]
print(wordBreak(testStr1, testWordDict1))
