# 📚 EvalMesh — Complete Enterprise Documentation & Developer Guide

Welcome to the official developer and enterprise documentation for **EvalMesh** — the Control Plane for Production AI Applications.

> *"EvalMesh is the control plane for production AI applications. It evaluates, secures, routes, monitors, and improves every AI request before it reaches your users."*

---

## 📑 Table of Contents

1. [Architecture & Data Flow Diagrams](#1-architecture--data-flow-diagrams)
2. [API Reference](#2-api-reference)
3. [SDK Integration Examples](#3-sdk-integration-examples)
4. [Kubernetes & Production Deployment Guide](#4-kubernetes--production-deployment-guide)
5. [Security & Compliance Guide](#5-security--compliance-guide)
6. [Migration Guide (From OpenAI / LangChain / LiteLLM)](#6-migration-guide)
7. [Troubleshooting & Diagnostics](#7-troubleshooting--diagnostics)
8. [Frequently Asked Questions (FAQ)](#8-frequently-asked-questions-faq)

---

## 1. Architecture & Data Flow Diagrams

EvalMesh acts as a zero-trust sidecar reverse proxy gateway positioned between your client applications and upstream LLM providers (OpenAI, Anthropic, Google Gemini, DeepSeek).

### 📐 System Pipeline Architecture
```text
  Client App (Python / TypeScript / REST)
                   │
                   ▼
       ┌───────────────────────────────┐
       │   EvalMesh Proxy Gateway      │ (Port 8000, Latency <15ms)
       └───────────────┬───────────────┘
                       │
  ┌────────────────────┼────────────────────┐
  │ 1. PII Redactor    │ 2. WAF Firewall    │ 3. Policy Engine
  │ (Hides Emails/SSN) │ (Blocks Jailbreak) │ (Evaluates Rules)
  └────────────────────┼────────────────────┘
                       │
  ┌────────────────────┼────────────────────┐
  │ 4. Semantic Cache  │ 5. Loop Breaker    │ 6. Smart Router
  │ (Sub-5ms @ $0 cost)│ (Halts Spikes)     │ (Auto-Downgrades)
  └────────────────────┴────────────────────┘
                       │
                       ▼
      Upstream Providers (OpenAI / Claude / Gemini / DeepSeek)
                       │
                       ▼
            Validated Response Egress
```

---

## 2. API Reference

All API requests pass through `http://localhost:8000` (or your domain endpoint).

### 🔹 `POST /v1/chat/completions`
Main proxy endpoint compatible with OpenAI API schema.

* **Headers**:
  - `Authorization: Bearer <API_KEY_OR_JWT>`
  - `x-evalmesh-agent-role: support_agent`
  - `x-evalmesh-prompt-version: v2.0`
* **Request Body**:
  ```json
  {
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a customer support agent."},
      {"role": "user", "content": "Summarize this contract and search FAQ."}
    ],
    "tools": [
      {"type": "function", "function": {"name": "search_faq"}}
    ]
  }
  ```
* **Response (200 OK)**:
  ```json
  {
    "id": "chatcmpl-evalmesh-99120",
    "object": "chat.completion",
    "model": "gpt-4o",
    "choices": [{
      "message": {"role": "assistant", "content": "Here is the summary..."}
    }]
  }
  ```

### 🔹 `POST /v1/policies/evaluate`
Evaluates custom context against the Declarative Policy Engine.

### 🔹 `GET /v1/sessions/replay/{session_id}`
Returns Chrome DevTools-style step execution trace array (`User` ➔ `System` ➔ `Memory` ➔ `Tools` ➔ `Security`).

### 🔹 `POST /v1/benchmark/run`
Runs side-by-side prompt benchmarking across GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, and DeepSeek R1.

### 🔹 `GET /v1/risk/scorecard`
Returns 5-dimension executive risk scorecard (Security 98, Reliability 95, Cost 82, Performance 91, Compliance 100).

---

## 3. SDK Integration Examples

### 🐍 Python SDK (`evalmesh/sdk.py`)
```python
from evalmesh.sdk import EvalMeshClient

client = EvalMeshClient(proxy_url="http://localhost:8000", api_key="em_live_key_991823")

response = client.create_chat_completion(
    messages=[{"role": "user", "content": "Check refund eligibility for user john@company.com"}],
    model="gpt-4o",
    agent_role="support_agent",
    prompt_version="v2.1.0"
)

print("AI Response:", response["choices"][0]["message"]["content"])
```

### 🟨 TypeScript / Node.js SDK (`evalmesh/sdk.ts`)
```typescript
import { EvalMeshClient } from './evalmesh/sdk';

const client = new EvalMeshClient({ baseUrl: 'http://localhost:8000', apiKey: 'em_live_key_991823' });

const response = await client.createChatCompletion({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Summarize user request' }],
  agentRole: 'support_agent'
});

console.log(response.choices[0].message.content);
```

### ⚙️ Custom Model Adapter SDK (`evalmesh/adapter_sdk.py`)
Connect self-hosted/proprietary LLMs (Ollama, vLLM) with zero vendor lock-in:
```python
from evalmesh.adapter_sdk import CustomModelAdapter

class MyCompanyLocalLLM(CustomModelAdapter):
    def invoke(self, prompt: str, temperature: float = 0.7):
        # Custom logic to query local Ollama or vLLM server
        return {"model": "MyCompanyLocalLLM", "completion": "Local LLM Response"}
```

---

## 4. Kubernetes & Production Deployment Guide

### Deploy via Kubernetes (`k8s-deployment.yaml`)
EvalMesh includes a production-ready HA manifest with 3 replicas, Horizontal Pod Autoscaler (HPA), and zero-downtime rolling updates:

```bash
kubectl apply -f k8s-deployment.yaml
```

### Deploy via Docker Compose
```bash
docker-compose up -d
```

---

## 5. Security & Compliance Guide

* **Prompt WAF**: Real-time regex & signature matcher stopping prompt overrides and system instruction disclosures (`403 Forbidden`).
* **PII Redaction**: Redacts Emails (`[REDACTED_EMAIL]`), SSNs (`[REDACTED_SSN]`), Credit Cards (`[REDACTED_PCI]`), and IPs before sending requests to external APIs.
* **SOC 2 Type II Compliance**: SHA-256 tamper-proof audit trail logs for all governance events.
* **HIPAA Compliance**: PHI Masking for Medical Record Numbers (MRN) and ICD-10 diagnostic codes.
* **GDPR Compliance**: Right-to-be-forgotten log purger for user data erasure.

---

## 6. Migration Guide

### Migrating from OpenAI SDK to EvalMesh
Change 1 line of code: set `base_url` to `http://localhost:8000/v1`!

```python
# BEFORE (Direct to OpenAI)
from openai import OpenAI
client = OpenAI(api_key="sk-proj-...")

# AFTER (Routed through EvalMesh Proxy)
from openai import OpenAI
client = OpenAI(
    api_key="sk-proj-...",
    base_url="http://localhost:8000/v1" # Simply point base_url to EvalMesh!
)
```

---

## 7. Troubleshooting & Diagnostics

| Symptom / Error Code | Root Cause | Resolution |
|---|---|---|
| **HTTP 403 Forbidden** | Prompt Injection signature matched or unauthorized tool executed. | Inspect session log or adjust policy rule in `policy_engine.py`. |
| **HTTP 429 Circuit Breaker**| Session message depth > 25 (agent loop detected). | Review agent recursive loop logic or increase max message limit. |
| **HTTP 504 Provider Timeout**| Primary LLM provider failed or timed out. | Automatic failover to Anthropic/Gemini will trigger automatically. |

---

## 8. Frequently Asked Questions (FAQ)

### Q1: How much latency does EvalMesh add?
**A**: Under **15 milliseconds** average proxy latency overhead. Caching responds in <5ms.

### Q2: Does EvalMesh store my raw API keys?
**A**: No. API keys are encrypted in-memory using the Encrypted Secrets Vault (`vault.py`) or passed securely via environment variables.

### Q3: Can I self-host EvalMesh on-premise?
**A**: Yes! EvalMesh can be deployed as a single Docker container or Kubernetes pod inside your VPC.

---

🔗 **Repository**: [https://github.com/deswanth12/EvalMesh](https://github.com/deswanth12/EvalMesh)
