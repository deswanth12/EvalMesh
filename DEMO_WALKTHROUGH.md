# 🎥 EvalMesh 3-Minute Demo Video Walkthrough Script

This script provides a step-by-step recording guide for presenting EvalMesh to investors, engineering leads, and enterprise clients.

---

## ⏱️ Video Timeline & Scene Breakdown

### 0:00 - 0:45 | Scene 1: Executive Dashboard & AI Reliability Score
* **Visual**: Open `https://evalmesh.vercel.app`.
* **Voiceover**:
  > *"Welcome to EvalMesh—the operating system for AI agent reliability and security. Here on our linear-inspired executive control plane, engineering leads see one signature metric: the **AI Reliability Score (94/100)**, calculated across accuracy, hallucination rate, WAF protection, latency, cost, and tool success."*

---

### 0:45 - 1:45 | Scene 2: Live Gateway Interactive Playground
* **Visual**: Navigate to **Live Interactive Playground**. Click **`Test WAF Attack`**, then **`Test PII Redaction`**, then **`Test Semantic Cache`**.
* **Voiceover**:
  > *"Let's test EvalMesh in action. First, a prompt injection jailbreak attempt—watch how our WAF instantly blocks it with a 403 Forbidden. Next, a prompt containing emails and credit cards—our DLP scanner redacts the sensitive tokens before they ever reach third-party LLMs. Finally, a duplicate prompt—serviced in sub-3ms from our semantic cache at $0 token cost."*

---

### 1:45 - 2:30 | Scene 3: Session Replay Console & Incident Center
* **Visual**: Open **Pillar 3: Observability & DevTools** trace tree, then **Incident Center**.
* **Voiceover**:
  > *"Think of EvalMesh as 'Chrome DevTools for AI Agents.' Our session replay console provides an expandable trace tree showing prompt egress, DLP redactions, tool RBAC permissions, and execution node graphs. When an anomaly occurs, it's logged to our GitHub-style incident stream for 1-click post-mortem analysis."*

---

### 2:30 - 3:00 | Scene 4: Enterprise Compliance & 1-Line SDK
* **Visual**: Open **Pillar 4: Enterprise & Governance**, click **`Export SOC 2 Audit Report CSV`**, and show `@guardrail` code snippet in VS Code.
* **Voiceover**:
  > *"For enterprise security, EvalMesh supports SAML 2.0, SCIM provisioning, data residency controls, and 1-click SOC 2 Type II audit exports. Best of all, developers can protect any LangGraph or CrewAI agent in 1 line of Python code using `@guardrail`. Try it today at evalmesh.vercel.app or on GitHub!"*
