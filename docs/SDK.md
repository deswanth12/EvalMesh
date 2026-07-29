# 💻 EvalMesh SDK & Developer Guide

EvalMesh provides 1-line agent guardrails for Python (`pip install evalmesh`) and TypeScript (`npm install @evalmesh/sdk`).

---

## 🐍 Python SDK Integration

### 1. Simple Client Usage
```python
from evalmesh.sdk import EvalMeshClient

client = EvalMeshClient(proxy_url="http://localhost:8000", api_key="em_live_12345")

response = client.create_chat_completion(
    messages=[{"role": "user", "content": "My email is alice@acme.com. Search FAQ."}],
    agent_role="support_agent",
    prompt_version="v3.1.0"
)

print(response["choices"][0]["message"]["content"])
```

### 2. Agent Framework Guardrail Decorator
Integrates with **LangGraph**, **CrewAI**, **AutoGen**, and **LlamaIndex**:

```python
from evalmesh.sdk import guardrail

@guardrail(agent_role="support_agent", max_depth=25)
def execute_agent_step(prompt: str, tool_name: str = "search"):
    # Automatic WAF firewall, PII redaction, tool RBAC & circuit breaker checks
    return f"Executing {tool_name} for prompt: {prompt}"

# Execution:
res = execute_agent_step(prompt="Search return policy", tool_name="faq_search")
print(res)
```

---

## 📘 TypeScript / JavaScript SDK Integration

```typescript
import { EvalMeshClient } from '@evalmesh/sdk';

const client = new EvalMeshClient({
  proxyUrl: 'http://localhost:8000',
  apiKey: 'em_live_12345'
});

async function run() {
  const response = await client.createChatCompletion({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'What is the shipping time?' }],
    agentRole: 'support_agent'
  });

  console.log(response);
}

run();
```
