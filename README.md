# ⚡ AI Token Governor

An intelligent LLM orchestration layer designed to control API costs, prevent rate-limit spikes, cache repetitive prompts, and dynamically route queries based on workload complexity.

## 🚀 Key Features
- **Smart Dynamic Routing:** Automatically routes simple queries to lightweight models and deep reasoning tasks to flagship models.
- **Deduplication & Cache Layer:** SHA-256 hashed prompt caching eliminates duplicate API calls (100% token savings on repeated requests).
- **Budget & Quota Management:** Strict token tracking per request and per day to prevent unexpected cloud billing spikes.
- **Cost Metrics & Logging:** Built-in cost accounting per request based on model pricing tiers.

## 💻 Quick Start
1. Clone the repository:
   ```bash
   git clone [https://github.com/Yfdcbh/ai-token-governer.git](https://github.com/Yfdcbh/ai-token-governer.git)
   cd ai-token-governer
