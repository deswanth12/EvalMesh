# EvalMesh Enterprise Security, Compliance & Governance Manual

**Document Version**: `1.0.0`  
**Classification**: PUBLIC / ENTERPRISE BRIEFING  
**Target Audience**: CISOs, VP of Engineering, Security Architects, and Enterprise Procurement.

---

## 📋 Executive Security Overview

EvalMesh is engineered from the ground up for zero-trust enterprise deployment. Operating as an in-line sidecar proxy, EvalMesh provides real-time security screening, automated PII/PHI redaction, role-based tool authorization, and tamper-proof SOC 2 audit logging.

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                       ENTERPRISE SECURITY & COMPLIANCE                      │
 ├───────────────────┬───────────────────┬─────────────────┬───────────────────┤
 │ SOC 2 TYPE II     │ GDPR              │ HIPAA           │ SSO & RBAC        │
 │ Audit Log Export  │ Anonymization     │ PHI Redaction   │ Okta / SAML 2.0   │
 └───────────────────┴───────────────────┴─────────────────┴───────────────────┘
```

---

## 🛡️ 1. SOC 2 Type II Compliance Roadmap & Audit Controls

EvalMesh aligns directly with AICPA SOC 2 Trust Services Criteria (Security, Availability, Confidentiality, and Privacy).

### Control Implementation Matrix

| SOC 2 Criterion | EvalMesh Enforcement Mechanism | Verification Endpoint |
| :--- | :--- | :--- |
| **CC6.1 (Access Control)** | API Keys (`em_live_...`) with sliding-window rate limiting & SAML 2.0 SSO | `POST /v1/auth/sso/validate` |
| **CC6.6 (Boundary Protection)**| In-line Prompt WAF Firewall blocking jailbreaks & context overrides | `POST /v1/chat/completions` (403 Block) |
| **CC6.8 (Data Transmission)** | Automatic PII (Emails, SSNs, Cards) & PHI masking before egress | `POST /v1/chat/completions` |
| **CC7.2 (Security Monitoring)** | SHA-256 Tamper-Proof Audit Trail Exporter | `GET /v1/compliance/soc2/audit-logs` |
| **CC8.1 (Change Management)** | Versioned Golden Dataset continuous CI/CD evaluation harness | `python -m evalmesh.ci_runner` |

---

## 🔒 2. GDPR Compliance & Data Privacy Statement

EvalMesh acts as a **Data Processor** under GDPR Article 28, ensuring that no unencrypted customer PII reaches third-party LLM vendors.

* **Data Minimization (Article 5)**: In-line PII DLP engine masks emails, phone numbers, IP addresses, and credit cards before request egress.
* **Right to be Forgotten (Article 17)**: Instant tenant-scoped log anonymization via `POST /v1/compliance/gdpr/forget`.
* **Zero Storage Data Retention Mode**: Telemetry logs store masked hashes without raw payload text when `ZERO_DATA_RETENTION=true`.

---

## 🏥 3. HIPAA & PHI Compliance Architecture

EvalMesh is **HIPAA BAA Ready** for healthcare enterprise deployments.

### Protected Health Information (PHI) Masking Engine

| Health Identifier | Regular Expression Pattern | Masking Token |
| :--- | :--- | :--- |
| **Medical Record Number (MRN)** | `\bMRN-\d{6,8}\b` | `[REDACTED_HIPAA_MRN]` |
| **ICD-10 Diagnosis Code** | `\bICD-10-[A-Z0-9.]{3,7}\b` | `[REDACTED_HIPAA_DIAGNOSIS]` |
| **RxNorm Prescription ID** | `\bRxNorm-\d{5,7}\b` | `[REDACTED_HIPAA_PRESCRIPTION]` |

---

## 🔑 4. Enterprise SSO & Multi-Tenant RBAC

### SAML 2.0 / Okta / Auth0 Integration

EvalMesh validates enterprise identity provider tokens on every request header:

```http
POST /v1/chat/completions HTTP/1.1
Host: gateway.evalmesh.internal
Authorization: Bearer sso_token_okta_992183
x-evalmesh-tenant-id: tenant_org_acme_corp
x-evalmesh-agent-role: support_agent
```

### Role-Based Access Control (RBAC) Matrix

| Agent Role | Permitted Tools | Forbidden Actions |
| :--- | :--- | :--- |
| `support_agent` | `search_faq`, `create_ticket` | `delete_user`, `run_query` |
| `developer_agent` | `read_repo`, `run_tests`, `build_image` | `deploy_production` |
| `admin_agent` | Full Tool Execution | None |

---

## ☸️ 5. Production Kubernetes Deployment Guide

Deploy EvalMesh as a high-availability Kubernetes gateway (min 3 replicas) using our official manifest:

```bash
kubectl apply -f k8s-deployment.yaml
```

**Manifest Features**:
* **Replica Count**: 3 pods across availability zones.
* **Autoscaling (HPA)**: Scales automatically up to 20 pods at 75% CPU load.
* **Liveness & Readiness Probes**: `/health` endpoint checks every 10 seconds.
* **Secrets Management**: Connects to Kubernetes Secret `llm-credentials`.
