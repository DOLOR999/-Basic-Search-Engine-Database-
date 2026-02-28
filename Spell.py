from collections import defaultdict

def levenshtein(s1: str, s2: str) -> int:
    """Simple Levenshtein (edit) distance — how many changes to turn s1 into s2"""
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
        
        # Group words by length → much faster candidate generation
        self.len_buckets = defaultdict(list)
        for word in self.vocab:
            self.len_buckets[len(word)].append(word)

    def suggest(self, word: str, top_k=3) -> list[str]:
        word = word.lower().strip()
        if not word or word in self.vocab:
            return []  # correct or empty → no suggestions
        
        candidates = []
        wlen = len(word)
        
        # Only look at words of very similar length (±1 or same)
        for length in range(max(1, wlen - 1), wlen + 2):
            if length not in self.len_buckets:
                continue
            for term in self.len_buckets[length]:
                # Quick filter: same first letter → huge speedup
                if term and term[0] != word[0]:
                    continue
                dist = levenshtein(word, term)
                if dist <= self.max_dist:
                    candidates.append((dist, term))
        
        # Sort: smallest distance first, then alphabetical
        candidates.sort(key=lambda x: (x[0], x[1]))
        return [term for dist, term in candidates][:top_k]


# ────────────────────────────────────────────────
#               Quick test right here
# ────────────────────────────────────────────────

if __name__ == "__main__":
    # Same sample words as before
    words = [
        "machine", "learning", "macbook", "neural", "network",
        "neuron", "natural", "marine", "medicine", "marching"
    ]
    
    spell = SpellSuggester(words, max_dist=2)
    
    tests = [
        "mahcine",    # should → machine, maybe marine/medicine
        "neurla",     # should → neural
        "machin",     # should → machine (delete 1)
        "learing",    # should → learning
        "netwok",     # should → network
        "hello",      # probably nothing or far away words
        "machine",    # correct → empty list
    ]
    
    for wrong in tests:
        suggestions = spell.suggest(wrong)
        print(f"'{wrong}' → {suggestions}")