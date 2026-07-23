import math
from typing import Dict, Any, List

class OutputDriftDetector:
    """
    Detects semantic output drift over time when LLM providers update models under the hood.
    Calculates Jaccard & Token Overlap Drift metrics between baseline responses and current outputs.
    """

    @staticmethod
    def calculate_token_set(text: str) -> set:
        if not text:
            return set()
        clean = ''.join(c.lower() if c.isalnum() else ' ' for c in text)
        return set(clean.split())

    @classmethod
    def compute_semantic_drift(cls, baseline_text: str, current_text: str) -> Dict[str, Any]:
        """
        Compares baseline gold text against current model output.
        Returns similarity score (0.0 to 1.0) and drift percentage (0% to 100%).
        """
        set1 = cls.calculate_token_set(baseline_text)
        set2 = cls.calculate_token_set(current_text)

        if not set1 or not set2:
            return {"similarity": 0.0, "drift_percent": 100.0, "status": "CRITICAL_DRIFT"}

        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        jaccard_similarity = len(intersection) / len(union) if union else 1.0
        drift_percent = (1.0 - jaccard_similarity) * 100.0

        status = "STABLE"
        if drift_percent > 35.0:
            status = "MODERATE_DRIFT"
        if drift_percent > 65.0:
            status = "HIGH_DRIFT"

        return {
            "similarity": round(jaccard_similarity, 4),
            "drift_percent": round(drift_percent, 2),
            "status": status
        }
