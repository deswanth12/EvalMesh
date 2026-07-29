# 🛠️ EvalMesh Maintenance & Engineering Standards

This document outlines guidelines for bug fixing, performance optimization, complexity reduction, and documentation standards for the EvalMesh codebase.

---

## 1. 🐛 Bug Fixing Protocol
* **Root Cause Investigation**: Inspect raw stack trace logs before editing code logic.
* **Regression Prevention**: Every bug fix must include a corresponding test case in `tests/` or `verify_all.py`.
* **Zero Silent Swallowing**: Never swallow exceptions or return dummy fallbacks silently without structured logging.

---

## 2. ⚡ Performance Optimization Guidelines
* **Sub-15ms Gateway Latency**: Keep reverse proxy overhead under 15ms.
* **Sub-5ms Cache Lookups**: Use `SemanticPromptCache` vector indexing or Redis hash lookups.
* **Compiled Regex**: Pre-compile all PII DLP regex patterns during engine initialization.

---

## 3. 🧹 Complexity Reduction & Clean Architecture
* **Single Responsibility Principle**: Keep routers thin; delegate business logic to `backend/services/` and database persistence to `backend/repositories/`.
* **Zero TODO Placeholders**: Never ship `TODO` comments or stubbed placeholder functions.

---

## 4. 📖 Documentation Standards
* Maintain synchronized documentation across `README.md`, `DOCUMENTATION.md`, `docs/API.md`, `docs/SDK.md`, and `docs/BENCHMARKS.md`.
* Ensure all code symbols have clear docstrings and type hints (`Python 3.12+` and `TypeScript 5.3+`).
