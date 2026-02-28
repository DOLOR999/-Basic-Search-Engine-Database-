class TrieNode:
    def __init__(self):
        self.children = {}           # char → TrieNode
        self.is_end_of_word = False
        self.word = None             # we'll store the full word here

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        word = word.lower()          # make everything lowercase
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word             # remember the full word

    def insert_all(self, words):
        for w in words:
            self.insert(w)

    def get_prefix_matches(self, prefix: str, limit=8) -> list[str]:
        """Return up to 'limit' words that start with the given prefix"""
        node = self.root
        prefix = prefix.lower()

        # Walk to the end of the prefix
        for char in prefix:
            if char not in node.children:
                return []               # prefix doesn't exist
            node = node.children[char]

        # Now collect all complete words in this subtree
        result = []
        
        def dfs(current_node, current_word_so_far):
            if len(result) >= limit:
                return
            if current_node.is_end_of_word:
                result.append(current_word_so_far)
            # Visit children in alphabetical order (nicer output)
            for char in sorted(current_node.children.keys()):
                dfs(current_node.children[char], current_word_so_far + char)

        dfs(node, prefix)
        return result[:limit]


# ────────────────────────────────────────────────
#          Now actually use it (the part you want)
# ────────────────────────────────────────────────

# Create the Trie
trie = Trie()

# Insert the example words
words_to_insert = ["machine", "learning", "macbook", "neural"]
trie.insert_all(words_to_insert)

# Test different prefixes
print("Words starting with 'mac':")
print(trie.get_prefix_matches("mac"))          # should show machine & macbook

print("\nWords starting with 'neu':")
print(trie.get_prefix_matches("neu"))

print("\nWords starting with 'learn':")
print(trie.get_prefix_matches("learn"))

print("\nWords starting with 'xyz' (should be empty):")
print(trie.get_prefix_matches("xyz"))

# Add more words
trie.insert_all(["macarena", "macintosh", "neuron", "network"])

print("\nAfter adding more words:")
print(trie.get_prefix_matches("mac", limit=5))   # now more results
print(trie.get_prefix_matches("neuro", limit=3))