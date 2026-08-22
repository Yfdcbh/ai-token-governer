import hashlib
import json
import time

class TokenGovernor:
    def __init__(self, daily_budget_tokens=50000, cost_per_1k_tokens={"fast": 0.0005, "smart": 0.005}):
        self.daily_budget = daily_budget_tokens
        self.used_tokens = 0
        self.pricing = cost_per_1k_tokens
        self.cache = {}
        self.logs = []

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimate: ~4 chars per token"""
        return max(1, len(text) // 4)

    def _get_cache_key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.strip().lower().encode()).hexdigest()

    def route_request(self, prompt: str) -> str:
        """Determines whether to route to lightweight or high-reasoning model."""
        tokens = self._estimate_tokens(prompt)
        complex_keywords = ["analyze", "architecture", "algorithm", "derive", "optimize", "compare deeply"]
        
        is_complex = any(kw in prompt.lower() for kw in complex_keywords) or tokens > 300
        return "smart-model" if is_complex else "fast-model"

    def execute_prompt(self, prompt: str):
        cache_key = self._get_cache_key(prompt)
        
        # 1. Check Cache
        if cache_key in self.cache:
            return {
                "source": "CACHE (0 Tokens Billed)",
                "model_used": "none",
                "tokens_consumed": 0,
                "response": self.cache[cache_key]
            }

        # 2. Check Token Budget
        estimated_input_tokens = self._estimate_tokens(prompt)
        if self.used_tokens + estimated_input_tokens > self.daily_budget:
            raise Exception("Daily Token Budget Exceeded. Request Blocked by TokenGovernor.")

        # 3. Smart Model Routing
        target_model = self.route_request(prompt)
        model_tier = "smart" if "smart" in target_model else "fast"
        
        # Simulated LLM execution
        simulated_response = f"[Simulated Output via {target_model}] Processed query: '{prompt[:40]}...'"
        output_tokens = self._estimate_tokens(simulated_response)
        total_request_tokens = estimated_input_tokens + output_tokens

        # 4. Update state & cache
        self.used_tokens += total_request_tokens
        self.cache[cache_key] = simulated_response
        cost = (total_request_tokens / 1000) * self.pricing[model_tier]

        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": target_model,
            "tokens": total_request_tokens,
            "cost_usd": round(cost, 6)
        }
        self.logs.append(log_entry)

        return {
            "source": "API_EXECUTION",
            "model_used": target_model,
            "tokens_consumed": total_request_tokens,
            "cost_usd": f"${cost:.6f}",
            "response": simulated_response
        }

    def get_summary(self):
        total_cost = sum(log["cost_usd"] for log in self.logs)
        return {
            "total_tokens_used": self.used_tokens,
            "daily_budget_tokens": self.daily_budget,
            "remaining_budget": self.daily_budget - self.used_tokens,
            "total_estimated_cost_usd": f"${total_cost:.6f}",
            "cache_entries": len(self.cache),
            "total_requests": len(self.logs)
        }

if __name__ == "__main__":
    governor = TokenGovernor(daily_budget_tokens=10000)
    
    queries = [
        "What is 2 + 2?",
        "Analyze the system architecture of distributed fault-tolerant databases.",
        "What is 2 + 2?",  # Should hit cache
    ]

    print("=== AI TOKEN GOVERNOR RUNTIME ===")
    for q in queries:
        print(f"\nPrompt: '{q}'")
        res = governor.execute_prompt(q)
        print(json.dumps(res, indent=2))

    print("\n=== SYSTEM METRICS ===")
    print(json.dumps(governor.get_summary(), indent=2))
