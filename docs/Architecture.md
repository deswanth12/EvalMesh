# 🏗️ EvalMesh Architecture Overview

EvalMesh is engineered as an enterprise-grade AI Agent Control Plane & Reverse Proxy Gateway ("Cloudflare + Datadog for AI Agents").

---

## 📐 System Architecture Blueprint

```text
  Internet Egress
        │
        │ HTTPS / WebSockets
        ▼
  EvalMesh Gateway (FastAPI Proxy / Sub-15ms Latency)
        │
        ├── WAF Prompt Injection Firewall (security.py)
        ├── PII Data Loss Prevention (dlp.py)
        ├── Tool RBAC Policy Engine (policy_engine.py)
        ├── Semantic Prompt Cache (cache.py / Redis)
        ├── HA Provider Failover Chain (failover.py)
        └── Session Replay & Telemetry Logger (db.py / PostgreSQL)
        │
        ▼
  Upstream LLM Providers (OpenAI / Anthropic / Gemini / DeepSeek / Ollama)
```

---

## 📁 Repository & Directory Layout

```text
evalmesh/
│
├── backend/
│   ├── proxy.py              # FastAPI reverse proxy server & REST/WebSocket routes
│   ├── auth.py               # Enterprise 4-tier RBAC & JWT token issuance
│   ├── enterprise.py         # SAML 2.0, SCIM v2.0, HIPAA PHI, GDPR, SOC 2
│   ├── policy_engine.py      # Declarative policy rules engine
│   ├── db.py                 # Pluggable storage adapters (SQLite & PostgreSQL)
│   ├── cache.py              # Pluggable semantic cache backends (Memory & Redis)
│   ├── failover.py           # HA multi-provider fallback chain
│   ├── human_approval.py     # Multi-approver thresholding queue
│   └── sdk.py                # Python Client SDK & @guardrail decorator
│
├── frontend/
│   └── dashboard/
│       └── index.html        # Clean 4-Pillar Linear/Vercel enterprise control panel
│
├── database/
│   ├── evalmesh.db           # SQLite development persistence
│   └── schema.sql            # PostgreSQL enterprise schema
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml    # FastAPI + PostgreSQL + Redis stack
│
├── kubernetes/
│   └── deployment.yaml       # 3-replica HA production deployment manifest
│
└── docs/
    ├── API.md
    ├── SDK.md
    └── Architecture.md
```
