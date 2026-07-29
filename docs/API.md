# 📡 EvalMesh REST API & WebSockets Documentation

EvalMesh provides a high-throughput, OpenAI-compatible FastAPI backend supporting REST API endpoints and real-time WebSockets.

---

## 🛠️ Core API Endpoints

### 1. Health Check
`GET /api/health` or `GET /health`
```json
{
  "status": "ok",
  "service": "EvalMesh AI Agent Control Plane",
  "version": "1.0.0 (FastAPI, WebSockets, PostgreSQL & Redis Enabled)"
}
```

### 2. Signature AI Reliability Score
`GET /api/reliability`
```json
{
  "score": 94,
  "accuracy": 98.4,
  "hallucination": 99.8,
  "safety_waf": 100.0,
  "cost_score": 92.0,
  "latency_score": 95.0,
  "tool_success": 100.0,
  "status": "Grade A+ Enterprise"
}
```

### 3. Active Incident Center
`GET /api/incidents`
```json
[
  {
    "id": "INC-104",
    "severity": "HIGH",
    "description": "Jailbreak prompt injection attempt on Sales Agent v2",
    "root_cause": "System override pattern matched in user egress prompt",
    "owner": "@sarah_dev",
    "status": "Mitigated by WAF"
  }
]
```

### 4. Registered AI Agents
`GET /api/agents`
```json
[
  {"name": "Support Bot v2", "environment": "Production", "model": "GPT-4o", "status": "Active"},
  {"name": "Financial Agent", "environment": "Staging", "model": "Claude 3.5 Sonnet", "status": "Human Approval Req"}
]
```

### 5. File Upload (Dataset CSV/JSON)
`POST /api/upload`
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@benchmark_dataset.jsonl"
```

### 6. OpenAI Proxy Chat Completion
`POST /v1/chat/completions`
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer em_live_12345" \
  -H "x-evalmesh-agent-role: support_agent" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "What is our return policy?"}]
  }'
```

---

## ⚡ Real-Time WebSocket Telemetry
`WS ws://localhost:8000/ws`

Pushes live latency and request volume telemetry frames every 2 seconds:
```json
{
  "latency_ms": 12,
  "requests_per_min": 5200,
  "blocked_today": 189,
  "reliability_score": 94,
  "timestamp": 1722238400.0
}
```
