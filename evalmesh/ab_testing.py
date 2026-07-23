import random
from typing import Dict, Any, List

class MultiModelABEvaluator:
    """
    Multi-Model A/B Routing & Evaluation Engine.
    Splits prompt traffic across multiple model candidates (e.g., 80% GPT-4o / 20% DeepSeek R1).
    """

    def __init__(self, routes: Dict[str, float] = None):
        self.routes = routes or {
            "gpt-4o": 0.8,
            "deepseek-r1": 0.2
        }

    def select_model(self, requested_model: str = None) -> str:
        """
        Selects a target model candidate based on traffic split probability weights.
        """
        if requested_model and requested_model not in self.routes:
            return requested_model

        models = list(self.routes.keys())
        weights = list(self.routes.values())
        return random.choices(models, weights=weights, k=1)[0]
