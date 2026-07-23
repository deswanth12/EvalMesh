from typing import Dict, Any, Tuple

class SmartCostRouter:
    """
    LLM Smart Cost Optimizer Engine.
    Analyzes prompt length & complexity. Automatically routes simple prompts to cheaper models 
    (e.g., gpt-4o-mini / deepseek-r1) to save up to 60% on API costs.
    """

    COST_MAP = {
        "gpt-4o": {"input": 0.0025, "output": 0.0100},       # Per 1k tokens
        "gpt-4o-mini": {"input": 0.00015, "output": 0.00060}, # 15x cheaper!
        "claude-3-5-sonnet": {"input": 0.0030, "output": 0.0150},
        "deepseek-r1": {"input": 0.00055, "output": 0.00219}
    }

    @classmethod
    def optimize_route(cls, requested_model: str, messages: list) -> Tuple[str, bool, str]:
        """
        Determines whether prompt can be safely downgraded to a cheaper model for cost savings.
        Returns: (selected_model, was_optimized, optimization_reason)
        """
        # Calculate prompt token complexity
        total_words = sum(len(str(m.get("content", "")).split()) for m in messages if isinstance(m, dict))
        
        # If user explicitly asks for complex reasoning or prompt > 1000 words, keep premium model
        has_complex_reasoning = any(
            kw in str(messages).lower() 
            for kw in ["refactor monolithic", "prove math theorem", "complex architectural design", "code audit"]
        )

        if requested_model == "gpt-4o" and total_words < 300 and not has_complex_reasoning:
            return "gpt-4o-mini", True, "SmartRoute: Automatically downgraded simple prompt from GPT-4o to GPT-4o-mini (Saved ~90% cost)."

        return requested_model, False, "Standard Model Route"
