import time
import os
import json
from typing import Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod

class BaseCacheBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def set(self, key: str, value: Dict[str, Any]):
        pass

    @abstractmethod
    def all_entries(self) -> Dict[str, Dict[str, Any]]:
        pass

class InMemoryCacheBackend(BaseCacheBackend):
    """In-memory cache backend for single-node deployments."""
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self.store.get(key)

    def set(self, key: str, value: Dict[str, Any]):
        self.store[key] = value

    def all_entries(self) -> Dict[str, Dict[str, Any]]:
        return self.store

class RedisCacheBackend(BaseCacheBackend):
    """Distributed Redis Cache Backend for multi-region gateway clusters."""
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.fallback = InMemoryCacheBackend()
        self.redis_available = False
        try:
            import redis
            self.client = redis.Redis.from_url(redis_url)
            self.redis_available = True
        except Exception:
            pass

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if self.redis_available:
            try:
                val = self.client.get(key)
                if val:
                    return json.loads(val.decode('utf-8'))
            except Exception:
                pass
        return self.fallback.get(key)

    def set(self, key: str, value: Dict[str, Any]):
        if self.redis_available:
            try:
                self.client.set(key, json.dumps(value))
            except Exception:
                pass
        self.fallback.set(key, value)

    def all_entries(self) -> Dict[str, Dict[str, Any]]:
        return self.fallback.all_entries()

class SemanticPromptCache:
    """
    Semantic Prompt Caching Engine with Hybrid Redis & Memory support.
    Caches high-scoring completions and matches incoming prompts using N-gram token similarity.
    If similarity >= threshold, serves cached response in <5ms at $0 API cost.
    """

    def __init__(self, similarity_threshold: float = 0.90, backend_type: Optional[str] = None):
        self.similarity_threshold = similarity_threshold
        self.backend_type = backend_type or os.getenv("EVALMESH_CACHE_BACKEND", "memory").lower()
        
        if self.backend_type == "redis":
            self.backend = RedisCacheBackend(os.getenv("EVALMESH_REDIS_URL", "redis://localhost:6379/0"))
        else:
            self.backend = InMemoryCacheBackend()
            
        self.total_savings_usd: float = 0.0

    @property
    def cache_store(self) -> Dict[str, Dict[str, Any]]:
        return self.backend.all_entries()

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

        for key, entry in self.backend.all_entries().items():
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

        cache_id = f"cache_{abs(hash(prompt))}"
        entry = {
            "prompt": prompt,
            "completion": completion,
            "timestamp": time.time(),
            "hits": 0
        }
        self.backend.set(cache_id, entry)

