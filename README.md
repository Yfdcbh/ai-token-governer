# ai-token-governer
Smart LLM request router, rate limiter, caching layer, and token budget manager for AI APIs.
# ⚡ AI Token Governor

An intelligent LLM orchestration layer designed to control API costs, prevent rate-limit spikes, cache repetitive prompts, and dynamically route queries based on workload complexity.

## 🚀 Key Features

- **Smart Dynamic Routing:** Automatically classifies query complexity and routes requests to cost-effective lightweight models or high-reasoning flagship models.
- **Deduplication & Cache Layer:** SHA-256 hashed prompt caching eliminates duplicate API calls, resulting in 100% token savings for repeated queries.
- **Budget & Quota Management:** Strict token tracking per request and per day to prevent unexpected cloud billing spikes.
- **Cost Metrics & Logging:** Built-in cost accounting per request based on model pricing tiers.

---

## 🛠️ Architecture


User Prompt ──► [Token Governor]
│
├─► Check Cache ──────► Return Cached Response (0 Cost)
│
├─► Budget Check ─────► Block if Limit Exceeded
│
└─► Complexity Router ─┬─► Lightweight Model (Low Cost)
└─► Deep Reasoning Model (High Tier)
