from collections import defaultdict

# ────────────────────────────────
#          TRIE for Autocomplete
# ────────────────────────────────

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word

    def insert_all(self, words):
        for w in words:
            if w.strip():
                self.insert(w)

    def get_prefix_matches(self, prefix: str, limit=6) -> list[str]:
        node = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        result = []
        def dfs(n: TrieNode, current: str):
            if len(result) >= limit:
                return
            if n.is_end_of_word:
                result.append(current)
            for ch in sorted(n.children):
                dfs(n.children[ch], current + ch)

        dfs(node, prefix)
        return result[:limit]


# ────────────────────────────────
#     SPELL SUGGESTER (Levenshtein)
# ────────────────────────────────

def levenshtein(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current = [i + 1]
        for j, c2 in enumerate(s2):
            ins = previous[j + 1] + 1
            dele = current[j] + 1
            sub = previous[j] + (c1 != c2)
            current.append(min(ins, dele, sub))
        previous = current
    return previous[-1]


class SpellSuggester:
    def __init__(self, vocabulary: list[str], max_dist=2):
        self.vocab = set(w.lower() for w in vocabulary if w.strip())
        self.max_dist = max_dist
        self.len_buckets = defaultdict(list)
        for w in self.vocab:
            self.len_buckets[len(w)].append(w)

    def suggest(self, word: str, top_k=3) -> list[str]:
        word = word.lower().strip()
        if not word or word in self.vocab:
            return []
        candidates = []
        wlen = len(word)
        for length in range(max(1, wlen - 1), wlen + 2):
            if length not in self.len_buckets:
                continue
            for term in self.len_buckets[length]:
                if term and term[0] != word[0]:
                    continue
                dist = levenshtein(word, term)
                if dist <= self.max_dist:
                    candidates.append((dist, term))
        candidates.sort(key=lambda x: (x[0], x[1]))
        return [term for _, term in candidates][:top_k]


# ────────────────────────────────
#          COMBINED HANDLER
# ────────────────────────────────

def handle_input(text: str, trie: Trie, suggester: SpellSuggester):
    text = text.strip()
    if not text:
        return

    # Split into words → work on the LAST one (most common UX)
    words = text.split()
    last_word = words[-1] if words else ""

    # 1. Autocomplete on the current (last) word/prefix
    auto_suggestions = trie.get_prefix_matches(last_word, limit=6)

    # 2. Spell suggestion only if it looks like a finished word
    #    (≥ 3 chars, and not obviously still typing i.e. doesn't end with space)
    spell_suggestions = []
    if len(last_word) >= 3 and (not text or text[-1] != " "):
        spell_suggestions = suggester.suggest(last_word, top_k=3)

    # Print nice output
    print(f"\n→ You typed: {text!r}")
    
    if auto_suggestions:
        print("Autocomplete:")
        for i, sug in enumerate(auto_suggestions, 1):
            print(f"  {i}. {sug}")
    
    if spell_suggestions:
        print("Did you mean?")
        for i, sug in enumerate(spell_suggestions, 1):
            print(f"  {i}. {sug}")
    
    if not auto_suggestions and not spell_suggestions:
        print("  (no suggestions)")


# ────────────────────────────────
#               MAIN
# ────────────────────────────────

if __name__ == "__main__":
    # Replace with YOUR real words when ready
    sample_vocabulary = [
        "machine", "learning", "macbook", "neural", "network", "neuron",
        "natural", "language", "processing", "marine", "medicine", "marching",
        "model", "deep", "learning", "data", "science", "algorithm"
    ]

    print("Building index...")
    trie = Trie()
    trie.insert_all(sample_vocabulary)

    spell = SpellSuggester(sample_vocabulary, max_dist=2)

    print("\nType something (or 'quit' to exit):")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break
        handle_input(user_input, trie, spell)