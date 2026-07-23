import time
from typing import Dict, Any, Optional, Tuple

class SemanticPromptCache:
    """
    Semantic Prompt Caching Engine.
    Caches high-scoring completions and matches incoming prompts using N-gram token similarity.
    If similarity >= threshold, serves cached response in <5ms at $0 API cost.
    """

    def __init__(self, similarity_threshold: float = 0.90):
        self.similarity_threshold = similarity_threshold
        # In-memory prompt cache store: {prompt_hash: {prompt, completion, timestamp, hits}}
        self.cache_store: Dict[str, Dict[str, Any]] = {}
        self.total_savings_usd: float = 0.0

    @staticmethod
    def _tokenize(text: str) -> set:
        clean = ''.join(c.lower() if c.isalnum() else ' ' for c in text)
        return set(clean.split())

    def compute_similarity(self, text1: str, text2: str) -> float:
        set1 = self._tokenize(text1)
        set2 = self._tokenize(text2)
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        # Dice similarity coefficient: (2 * |A ∩ B|) / (|A| + |B|)
        dice_score = (2.0 * len(intersection)) / (len(set1) + len(set2))
        return dice_score

    def get(self, prompt: str) -> Tuple[Optional[str], float]:
        """
        Looks up prompt in semantic cache.
        Returns: (cached_completion, similarity_score)
        """
        if not prompt:
            return None, 0.0

        best_match = None
        highest_score = 0.0

        for key, entry in self.cache_store.items():
            score = self.compute_similarity(prompt, entry["prompt"])
            if score > highest_score:
                highest_score = score
                best_match = entry

        if highest_score >= self.similarity_threshold and best_match:
            best_match["hits"] += 1
            self.total_savings_usd += 0.03 # Estimated $0.03 saved per LLM call
            return best_match["completion"], round(highest_score, 4)

        return None, 0.0

    def set(self, prompt: str, completion: str):
        """
        Stores prompt and completion in semantic cache.
        """
        if not prompt or not completion:
            return

        cache_id = f"cache_{hash(prompt)}"
        self.cache_store[cache_id] = {
            "prompt": prompt,
            "completion": completion,
            "timestamp": time.time(),
            "hits": 0
        }
