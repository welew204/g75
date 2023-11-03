# NEET CODE SOLVE
class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.endOfWord = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word) -> None:
        pos = self.root
        for c in word:
            if c not in pos.children:
                pos.children[c] = TrieNode()
            pos = pos.children[c]
        pos.endOfWord = True  # marking end of word

    def search(self, word) -> bool:
        pos = self.root
        for c in word:
            if c not in pos.children:
                return False
            pos = pos.children[c]
        return pos.endOfWord

    def startsWith(self, prefix) -> bool:
        pos = self.root
        for c in prefix:
            if c not in pos.children:
                return False
            pos = pos.children[c]
        return True

    # my attempt with JUST a hash map...fails on test 15/16 tho I'm not sure why....


class TrieWB:

    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        pos = self.root
        i = 0
        while i < len(word):
            k = word[i]
            while k in pos and i < len(word):
                pos = pos[k]
                if i == len(word) - 1 and word not in pos:
                    pos[word] = None  # inserting the terminal signal!
                    return
                elif i == len(word) - 1 and word in pos:
                    return  # the whole word is already in the dict!
                i += 1
                k = word[i]
            pos[k] = {}
            pos = pos[k]
            i += 1
        pos[word] = None  # this is a signal that the WORD has been inserted
        return

    def search(self, word: str) -> bool:
        i = 0
        pos = self.root
        while i < len(word):
            k = word[i]
            if k not in pos:
                return False
            pos = pos[k]
            i += 1
        return True if word in pos else False

    def startsWith(self, prefix: str) -> bool:
        i = 0
        pos = self.root
        while i < len(prefix):
            k = prefix[i]
            if k not in pos:
                return False
            pos = pos[k]
            i += 1
        return True

        # Your Trie object will be instantiated and called as such:
        # obj = Trie()
        # obj.insert(word)
        # param_2 = obj.search(word)
        # param_3 = obj.startsWith(prefix)
test_array = ["Trie", "insert", "search",
              "search", "startsWith", "insert", "search"]
value_array = [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
result = []
for t in range(len(test_array)):
    q = value_array[t]
    if test_array[t] == 'Trie':
        trie = Trie()
        result.append([])
    elif test_array[t] == 'insert':
        q = q[0]
        trie.insert(q)
        result.append('null')
    elif test_array[t] == 'search':
        q = q[0]
        res = trie.search(q)
        result.append(res)
    elif test_array[t] == 'startsWith':
        q = q[0]
        res = trie.startsWith(q)
        result.append(res)
print(result)
