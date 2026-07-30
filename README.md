# 🛡️ EvalMesh — The Control Plane for Production AI Applications

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/deswanth12/EvalMesh)
[![System Verification](https://img.shields.io/badge/suite-41%2F41%20passing-brightgreen.svg)](https://github.com/deswanth12/EvalMesh)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/deswanth12/EvalMesh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-SDK%20Available-3178C6)](https://www.typescriptlang.org/)

![EvalMesh Banner](assets/evalmesh_banner.svg)

> **EvalMesh is the control plane for production AI applications.**  
> It evaluates, secures, routes, monitors, and improves every AI request before it reaches your users — giving engineering teams the confidence to ship reliable AI systems faster while spending 90% less time on manual testing and troubleshooting.

```text
                        EvalMesh Continuous AI Control Plane Flywheel

     Build AI Apps  ➔  Evaluate Automatically  ➔  Secure & Govern  ➔  Monitor Production  ➔  Improve Continuously
```

📖 **[Read Complete Enterprise Documentation & Developer Guide](DOCUMENTATION.md)**

---

## 🎯 What Problem Does EvalMesh Solve?

Imagine a team building a production AI assistant. Every single day, engineers ask:
* *Is the AI still accurate after today's prompt edit?*
* *Did a provider model update introduce new hallucinations or regressions?*
* *Which AI model provider is faster, cheaper, and more reliable for this task?*
* *Are user prompts safe, or are attackers trying prompt injection attacks?*
* *Are we accidentally leaking sensitive customer PII to external API providers?*

Without EvalMesh, engineers spend **hours every week manually testing prompts in spreadsheets**.  
With EvalMesh, **the entire lifecycle is automated in real-time**.

```text
 ┌─────────────┐        ┌────────────────────────────────────────────────────────┐        ┌──────────────────┐
 │ Client App  │ ─────> │                 EvalMesh Control Plane                 │ ─────> │ Upstream Models  │
 │ (SDK / API) │        │ (Auth ➔ WAF ➔ PII ➔ Cache ➔ Router ➔ Evals ➔ Telemetry)│        │ OpenAI, Claude… │
 └─────────────┘        └────────────────────────────────────────────────────────┘        └──────────────────┘
```

---

## ⚡ 10-Step Request Processing Pipeline

Every request routed through EvalMesh passes through an automated 10-tier safety and evaluation pipeline:

```text
Client Request
      │
      ▼
 1. Authentication & Rate Limit (JWT, API Keys, PATs, Bucket Rate Limiter)
      │
      ▼
 2. Semantic Cache              (Sub-5ms Cache Response @ $0 Token Cost)
      │
      ▼
 3. Smart Cost Router           (Auto-Downgrades Simple Prompts to Cheaper Models)
      │
      ▼
 4. Circuit Breaker & Loop Check(Halts Infinite Agent Loops & Budget Spikes)
      │
      ▼
 5. WAF Security Firewall       (Prompt Injection & Jailbreak Defense)
      │
      ▼
 6. PII DLP Redactor            (Sanitizes Emails, Credit Cards, SSNs)
      │
      ▼
 7. Tool Permission (RBAC)      (Enforces Per-Agent-Role Tool Execution Limits)
      │
      ▼
 8. Upstream Provider Gateway   (Failover Engine: OpenAI, Anthropic, Gemini, DeepSeek, Ollama)
      │
      ▼
 9. Auto Evaluation             (Calculates Accuracy, Hallucination, & Reliability Index)
      │
      ▼
 10. Dashboard & Telemetry      (Streams OpenTelemetry Spans & Real-Time Alerts)
```

---

## ⏱️ ROI & Time Saved

| Capability | Without EvalMesh | With EvalMesh | Time / Cost Saved |
|---|---|---|---|
| **AI Prompt Evaluation** | Manual testing of 100+ cases across 2–4 hours | 1-Click Automated Evaluation Suite | **Hours saved per release** |
| **Multi-Model Comparison** | Copying outputs into spreadsheets across OpenAI, Anthropic, Gemini | Side-by-Side Model Benchmark Comparison | **30–60 mins per test run** |
| **Prompt Versioning** | Searching Git commit history for working prompts | Complete Prompt Registry linked to eval scores | **Instant prompt rollback** |
| **Security & PII Shield** | Vulnerabilities discovered by users in production | Real-Time WAF & PII Redactor block attacks inline | **Prevents costly security incidents** |
| **Drift Monitoring** | Customers report broken chatbot behavior first | Real-Time Drift & Regression Alerts | **Instant detection & diagnosis** |

---


## 🚀 Get Started with EvalMesh

### 1. Explore the Dashboard
Visit the live control panel: **[https://evalmesh.vercel.app](https://evalmesh.vercel.app)**  
Within your first minute, you can:
* View the signature **AI Reliability Score (94/100)**
* Monitor live request traffic and 6 core executive KPIs
* Inspect real-time WAF security metrics and agent health

### 2. Try the Interactive Playground
Test EvalMesh scenarios live in your browser:
* 🛡️ **Prompt Injection Protection**: Real-time jailbreak attack blocking (`403 Forbidden`).
* 🔒 **PII Redaction**: Redact credit cards, SSNs, and emails before LLM egress.
* ⚡ **Semantic Cache**: Sub-3ms prompt caching at $0 cost.
* 👤 **Tool RBAC**: Pauses unauthorized database operations for human approval.
* 📊 **Live Telemetry & Agent Timeline**: Visual interaction trace logging.

### 3. Protect an AI Agent in 1 Line of Code

**Python**:
```bash
pip install evalmesh
```
```python
from evalmesh.sdk import guardrail

@guardrail(agent_role="support_agent")
def run_agent(prompt: str):
    return llm.invoke(prompt)
```

**TypeScript**:
```bash
npm install @evalmesh/sdk
```
```typescript
import { EvalMeshClient } from "@evalmesh/sdk";
const client = new EvalMeshClient();
```

### 4. Automated Agent Monitoring
Once connected, EvalMesh automatically provides:
* AI Reliability Scorecard
* Prompt Injection Protection & PII DLP
* Sub-5ms Semantic Prompt Cache
* Tool Permission Enforcement & Human Approvals
* Live Telemetry & Session Replay Console
* Cost Analytics & Incident Detection

### 5. Enterprise Governance Controls
Organizations can easily enable:
* SAML 2.0 / OIDC & SCIM User Provisioning
* Tamper-Proof Audit Logs (SOC 2 / HIPAA)
* AES-256 Encrypted Secrets Vault
* Sovereign Data Residency & Data Retention Purging

### 6. Deploy Anywhere

**Local Run**:
```bash
git clone https://github.com/deswanth12/EvalMesh.git
cd EvalMesh
python evalmesh_start.py
```

**Cloud Deploy**:
* **Docker / Docker Compose**: `docker-compose up -d`
* **Kubernetes**: `kubectl apply -f kubernetes/`
* **PaaS**: Render, Railway, Vercel, AWS, GCP, Azure

### 7. Observability & API Probes
* Health Probes: `/health`, `/ready`, `/live`
* Metrics Probe: `/metrics` (Prometheus format)
* Streaming: `/ws` (WebSockets)
* REST API: `/api/v1/*`

### 8. System Architecture Blueprint
```text
Browser (React + TypeScript)
      │
      ▼ REST API / WebSockets
FastAPI Gateway Backend
      │
 ├── Security Engine (security.py, dlp.py)
 ├── Evaluation Engine (drift.py, dataset.py)
 ├── Agent Registry (backend/models/database.py)
 ├── Policy Engine (policy_engine.py)
 ├── Telemetry & Session Replay (otel.py, session_replay.py)
 └── Enterprise Governance (enterprise.py)
      │
      ▼
PostgreSQL 15 + Redis 7.2
```

---


## 🎨 New Linear & Vercel-Grade Enterprise UI

EvalMesh features a calm, high-trust B2B dark aesthetic inspired by **Linear**, **Vercel**, **Stripe**, **Datadog**, and **Grafana Labs**:

* **Clean 4-Color Accent System**: Blue (`#3b82f6`), Green (`#10b981`), Orange (`#f59e0b`), Red (`#ef4444`).
* **Uncluttered 6-KPI First Impression Screen**:
  - **AI Requests**: `1.2M` (↑ 12%)
  - **Blocked Attacks**: `189` (Today)
  - **Money Saved**: `$1,284` (This Month)
  - **Latency**: `12 ms` (Excellent)
  - **Success Rate**: `99.98%` (Healthy)
  - **Security Score**: `96/100` (Grade A+)

---

## 📊 Empirical Performance & Benchmark Results

> [!NOTE]
> Measured on local development hardware using a sequential benchmark of 1,000 requests. See **[BENCHMARKS.md](docs/BENCHMARKS.md)** for complete reproducible methodology.

| Benchmark Metric | Empirical Measured Result | Target SLA Target | Verification Status |
|---|---|---|---|
| **Average API Latency** | **1.66 ms** | < 15.0 ms | :white_check_mark: Verified |
| **Cache Lookup Latency** | **0.02 ms** | < 5.0 ms | :white_check_mark: Verified |
| **PII DLP Scanning** | **0.28 ms** | < 2.0 ms | :white_check_mark: Verified |
| **WAF Firewall Scanning**| **0.002 ms** | < 1.0 ms | :white_check_mark: Verified |
| **Sequential Throughput** | **604 req/sec** | > 200 req/sec | :white_check_mark: Measured |
| **Verification Suite** | **41 / 41 Checks** | 100% Pass Rate | :white_check_mark: 100% Operational |

---

## ⚡ 41 Verified Engine Modules


| Category | # | Module Name | Implementation File | Feature & Capability Overview |
|---|---|---|---|---|
| **Security & Guardrails** | 1 | **Prompt Injection WAF** | `security.py` | Blocks jailbreaks & system overrides (`403 Forbidden`). |
| | 2 | **PII Data Loss Prevention** | `dlp.py` | Redacts Emails, SSNs, Credit Cards, IPs, and Phone numbers. |
| | 3 | **Tool RBAC Enforcer** | `security.py` | Role-based tool permissions (e.g., support agent allowed search, blocked DB delete). |
| | 4 | **Declarative Policy Engine** | `policy_engine.py` | Dynamic IF/THEN rules engine (`If role == intern: block tool delete_database`). |
| | 5 | **Encrypted Secrets Vault** | `vault.py` | Encrypted store for OpenAI, Anthropic, Stripe, and Slack keys. |
| **Cost & Performance** | 6 | **Semantic Prompt Cache** | `cache.py` | Serves 80%+ similar prompts in <5ms for **$0 cost** (saving 60–90% on API bills). |
| | 7 | **Smart Cost Router** | `smart_router.py` | Auto-downgrades simple prompts to 15x cheaper `gpt-4o-mini`. |
| | 8 | **Runaway Loop Breaker** | `cost_breaker.py` | Halts infinite agent loops at depth > 25 (`429 Circuit Breaker`). |
| | 9 | **HA Model Failover** | `failover.py` | Auto-failover chain during OpenAI outages (`OpenAI ➔ Anthropic ➔ Gemini ➔ DeepSeek`). |
| **Observability & DevTools**| 10 | **AI Session Replay** | `session_replay.py` | **"Chrome DevTools for AI"**: Expandable tree trace (`Conversation ➔ System Prompt ➔ Memory ➔ Tool Calls ➔ Security Checks`). |
| | 11 | **Agent Graph Visualizer** | `agent_graph.py` | Visual node execution graph (`User ➔ Planner ➔ Retriever ➔ Memory ➔ Calculator ➔ CRM ➔ LLM ➔ Answer`). |
| | 12 | **AI Gateway Benchmark Lab**| `benchmark_lab.py` | Side-by-side prompt model benchmark comparing GPT-4o, Claude, Gemini, DeepSeek. |
| | 13 | **Auto-Healing Retry** | `auto_heal.py` | Micro-retry self-correction prompt engine repairing malformed JSON. |
| | 14 | **Output Drift Detector** | `drift.py` | Detects silent LLM provider updates, schema drift, and semantic regressions. |
| | 15 | **Golden Dataset Generator**| `dataset.py` | Auto-generates JSONL regression datasets from production traffic. |
| | 16 | **Multi-Model A/B Router** | `ab_testing.py` | Live performance benchmark comparing cost, latency, and accuracy. |
| | 17 | **OpenTelemetry Tracing** | `otel.py` | Generates standard OTel trace spans for Datadog, Grafana, and Jaeger. |
| | 18 | **Incident Event Timeline** | `incident_timeline.py` | GitHub-style chronological event log stream for operations teams. |
| **Governance & Multi-Tenancy**| 19 | **4-Tier RBAC Hierarchy** | `auth.py`, `db.py` | Super Admin, Organization Admin, Evaluator, Viewer roles. |
| | 20 | **Multi-Tenant Database** | `db.py` | SQLite persistence engine with strict tenant isolation. |
| | 21 | **Human Approval Workflows** | `human_approval.py` | Intercepts high-stakes agent operations ($10,000 refunds, DB drops) for admin approval. |
| | 22 | **Prompt Version Registry** | `prompt_registry.py` | "Git for Prompts" version history (`v1.0`, `v2.0`, `v3.1`) with 1-click rollback. |
| | 23 | **Enterprise Compliance** | `enterprise.py` | SOC 2 Type II audit logs, HIPAA PHI redactor, GDPR right-to-be-forgotten. |
| | 24 | **SAML 2.0 / SSO Validation**| `enterprise.py` | Validates Okta & Auth0 enterprise identity provider tokens. |
| | 25 | **AI Security Score Engine** | `security_score.py` | 0–100 Security Score Card (`96/100 Grade A+`). |
| | 26 | **Executive Risk Dashboard** | `risk_dashboard.py` | 5-dimension scorecard (Security 98, Reliability 95, Cost 82, Performance 91, Compliance 100). |
| | 27 | **AI Governance Reports** | `governance_reports.py` | Downloadable compliance, security, and audit report generator. |
| | 28 | **Plugin Marketplace** | `plugins.py` | 1-Click integration registry for Salesforce, SAP, Jira, Slack, Notion, ServiceNow. |
| | 29 | **Custom Model Adapter SDK** | `adapter_sdk.py` | `CustomModelAdapter` base class for self-hosted LLMs with zero vendor lock-in. |
| | 30 | **Predictive Cost Forecast** | `cost_forecasting.py` | Predicts next month spend based on growth rates (Current $1,200/mo ➔ Predicted $1,540/mo). |
| | 31 | **1-Click Incident Reports** | `incident_report.py` | Automated root-cause analysis post-mortem report generator. |
| **Tools & Infrastructure**| 32 | **FastAPI Reverse Proxy** | `proxy.py` | Gateway server running on port `8000`. |
| | 33 | **Web Control Dashboard** | `dashboard/index.html`| Linear/Vercel enterprise dashboard with Persona switcher. |
| | 34 | **Python & TS Client SDKs** | `sdk.py`, `sdk.ts` | `@evalmesh/sdk` for Python and TypeScript applications. |
| | 35 | **Command-Line CLI** | `cli.py` | CLI management utility (`evalmesh start`, `evalmesh keys`, `evalmesh verify`). |
| | 36 | **3-Min Live Investor Demo** | `live_demo.py` | Terminal walkthrough simulating WAF, Loop Breaker, Auto-Healing, & Telemetry. |
| | 37 | **Kubernetes Production Manifest**| `k8s-deployment.yaml`| 3-replica HA deployment with Horizontal Pod Autoscaler (HPA). |
| | 38 | **Enterprise Storage Adapters**| `db.py`, `cache.py` | Pluggable `BaseStorageAdapter` (SQLite & PostgreSQL) + Redis Cache backend. |
| | 39 | **Agent Framework Guardrails**| `sdk.py` | `EvalMeshAgentGuardrail` & `@guardrail` for LangGraph, CrewAI, AutoGen. |
| | 40 | **40-Check Verification Suite**| `verify_all.py` | Automated test harness validating system health & security rules. |

---


## 🚀 Quickstart & Installation (30 Seconds)

### Step 1: Clone & Launch Standalone Gateway
```bash
git clone https://github.com/deswanth12/EvalMesh.git
cd EvalMesh
python evalmesh_start.py
```
👉 Open **[http://localhost:8000](http://localhost:8000)** to launch the Linear/Vercel Web Control Panel Dashboard!

### Step 2: Route Requests via Python SDK
```python
from evalmesh.sdk import EvalMeshClient

client = EvalMeshClient(proxy_url="http://localhost:8000")

response = client.create_chat_completion(
    messages=[{"role": "user", "content": "My email is alice@company.com. Search FAQ."}],
    agent_role="support_agent",
    prompt_version="v1.5.0"
)

print(response["choices"][0]["message"]["content"])
```

### Step 3: Run System Double-Check Harness
```bash
python -m evalmesh.verify_all
```
Output:
```text
===============================================================
 [SUCCESS] System-Wide Double Check Complete: 38/38 Modules 100% Operational!
===============================================================
```

---

## 📜 License & Compliance
Distributed under the MIT License. Built for enterprise SOC 2, HIPAA, and GDPR compliance.
