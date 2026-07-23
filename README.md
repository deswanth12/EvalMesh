# 🛡️ EvalMesh — AI Gateway for Secure & Reliable Agent Deployment

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/deswanth12/EvalMesh)
[![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)](https://github.com/deswanth12/EvalMesh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-SDK%20Available-3178C6)](https://www.typescriptlang.org/)

> **Cloudflare for AI Agents.**  
> An ultra-low-latency (<15ms) reverse proxy gateway, real-time prompt injection WAF, PII DLP redactor, semantic prompt cache, and automated CI/CD evaluation harness for LLM workflows.

---

## 📋 Quick Links
* 📄 **[Technical Documentation](DOCUMENTATION.md)**
* 💡 **[Non-Technical Plain English Guide](NON_TECHNICAL_GUIDE.md)**
* 🌐 **Interactive Control Panel Dashboard**: `http://localhost:8000`

---

## ⚡ Quickstart

### 1. Launch Standalone Gateway & Web Dashboard
```bash
python evalmesh_start.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

### 2. Python SDK Usage
```python
from evalmesh.sdk import EvalMeshClient

client = EvalMeshClient(proxy_url="http://localhost:8000", api_key="em_live_demo_123456789")

response = client.create_chat_completion(
    messages=[{"role": "user", "content": "My email is test@example.com. Search FAQ."}],
    agent_role="support_agent",
    prompt_version="v1.5.0"
)

print(response["choices"][0]["message"]["content"])
```

### 3. TypeScript SDK Usage
```typescript
import { EvalMeshClient } from './evalmesh/sdk';

const client = new EvalMeshClient({ baseUrl: 'http://localhost:8000' });

const response = await client.createChatCompletion({
  messages: [{ role: 'user', content: 'What is your return policy?' }],
  agentRole: 'support_agent',
  promptVersion: 'v1.5.0'
});

console.log(response.choices[0].message.content);
```

---

## 🧪 System Verification
To verify all 15 core engine modules:
```bash
python -m evalmesh.verify_all
```
