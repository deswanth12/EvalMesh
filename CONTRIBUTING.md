# Contributing to EvalMesh

Thank you for your interest in contributing to **EvalMesh**! We welcome contributions from developers, security researchers, and AI engineers across the globe.

---

## 🚀 How to Get Started

### 1. Fork & Clone the Repository
```bash
git clone https://github.com/your-username/EvalMesh.git
cd EvalMesh
```

### 2. Set Up Development Environment
Create a Python 3.12 virtual environment and install dependencies:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r evalmesh/requirements.txt
```

### 3. Run the Verification Test Suite
Before making any changes, ensure all 16 core engine modules pass locally:
```bash
python -m evalmesh.verify_all
```

---

## 🛠️ Contribution Workflow

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Implement Your Changes**:
   * Keep functions modular and maintain strict type hints.
   * Add unit tests to `evalmesh/verify_all.py`.
3. **Run Code Verification**:
   ```bash
   python -m evalmesh.verify_all
   ```
4. **Commit & Push**:
   ```bash
   git commit -m "feat(waf): add new jailbreak signature detection"
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request**: Submit a PR to `main` and complete the PR template checklist.

---

## 📜 Code of Conduct
We enforce a welcoming, inclusive, and harassment-free community environment. Respect fellow contributors and maintain professional standards in all issue discussions and PR reviews.
