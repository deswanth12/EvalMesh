# 📝 EvalMesh Changelog

All notable changes to the EvalMesh Enterprise AI Operations Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-07-29

### 🚀 Added
- **AI Reliability Score**: Signature 0-100 metric calculated across Accuracy, Hallucination, Safety WAF, Cost, Latency, and Tool Success.
- **Prompt Injection WAF**: Real-time jailbreak firewall blocking system overrides with `403 Forbidden`.
- **PII DLP Redactor**: Automated sanitization for Emails, Credit Cards, SSNs, IP Addresses, and Phone Numbers.
- **Sub-5ms Semantic Prompt Cache**: Hybrid In-Memory and Redis backend serving 80%+ similar prompts for $0.00 token cost.
- **Runaway Loop Breaker**: Circuit breaker terminating infinite agent loops at depth > 25 (`429 Circuit Breaker`).
- **HA Provider Failover**: Multi-provider fallback chain during upstream downtime (`OpenAI ➔ Anthropic ➔ DeepSeek ➔ Ollama`).
- **Multi-Approver Consensus Workflows**: Human approval intercepts requiring 2 admin sign-offs for $10,000+ operations.
- **Enterprise Compliance Engine**: SCIM v2.0 provisioning, SAML 2.0 / OIDC SSO, Data Residency controls, Data Retention purging, and SOC 2 / HIPAA CSV exporters.
- **Modular Monorepo Structure**: Clean separation across `frontend/`, `backend/`, `database/`, `docker/`, `kubernetes/`, `docs/`, `sdk/`, and `tests/`.
- **41-Module Double-Check Test Suite**: Automated verification suite maintaining 100% pass rate (`41/41 Modules Operational`).

---

## [0.9.0] - 2026-07-15
### 🚀 Added
- FastAPI reverse proxy server supporting OpenAI API protocol `/v1/chat/completions`.
- Linear & Vercel inspired dark mode Control Panel UI.
- OpenTelemetry trace exporter supporting Datadog, Grafana, and Jaeger formats.

---

## [0.8.0] - 2026-07-01
### 🚀 Added
- Initial core proxy architecture and Python Client SDK.
