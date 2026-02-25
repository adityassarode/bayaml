

# 📄 CONTRIBUTING.md

````markdown
# Contributing to Baya

First of all, thank you for considering contributing to Baya.

Baya is designed to be a serious ML orchestration framework.  
We welcome improvements in performance, architecture, documentation, integrations, and testing.

---

# Code of Conduct

By participating in this project, you agree to maintain a respectful and professional environment.

- Be constructive
- Be respectful
- Focus on technical discussion
- No harassment or toxic behavior

---

# How to Contribute

There are multiple ways to contribute:

• Reporting bugs  
• Suggesting features  
• Improving documentation  
• Writing tests  
• Submitting pull requests  
• Creating plugins  

---

# Development Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/baya.git
cd baya
````

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

## 3️⃣ Install in Editable Mode

```bash
pip install -e .
pip install -r requirements-dev.txt
```

---

# Running Tests

We use pytest.

```bash
pytest
```

To run with coverage:

```bash
pytest --cov=baya
```

---

# Code Style Guidelines

We follow:

* PEP 8
* Type hints required for public APIs
* Docstrings for all public classes and methods
* Clean architecture separation
* No business logic inside CLI layer
* No side-effects inside import statements

---

# Formatting

Use:

```bash
black .
ruff .
```

All PRs must pass formatting checks.

---

# Branch Strategy

* main → stable branch
* dev → active development
* feature/* → feature branches
* fix/* → bug fixes

Never commit directly to main.

---

# Pull Request Process

1. Fork repository
2. Create new branch from `dev`
3. Make changes
4. Add tests
5. Ensure all tests pass
6. Submit pull request

PR must include:

* Clear description
* What problem it solves
* Why it is needed
* Any breaking changes

---

# Architecture Contribution Rules

Baya follows layered architecture:

core → orchestration → tracking → plugins → cli

Rules:

* Do not couple modules tightly
* Do not import CLI inside core
* Plugins must extend BasePlugin
* Integrations must use BaseBackend
* Orchestration must remain framework-agnostic

---

# Adding a New Integration

Example: Adding XGBoost

1. Create folder:

```
baya/integrations/xgboost/
```

2. Implement backend inheriting from BaseBackend

3. Register inside model_registry.py

4. Add tests

5. Update documentation

---

# Adding a New Plugin

1. Create external package:

```
baya-myplugin/
```

2. Implement BasePlugin

3. Expose entry point in pyproject.toml:

```toml
[project.entry-points."baya.plugins"]
myplugin = "baya_myplugin.plugin:MyPlugin"
```

---

# Documentation Contributions

Docs are in:

```
docs/
```

Keep:

* Clear examples
* No marketing tone
* Technical accuracy

---

# Testing Requirements

All new features must include:

* Unit tests
* Edge case tests
* Failure case tests

Do not merge without tests.

---

# Performance Contributions

If optimizing:

* Provide benchmark comparison
* Explain trade-offs
* Avoid premature optimization

---

# Security

If you discover a security issue:

DO NOT open a public issue.

Instead email:

[security@baya-framework.org](mailto:security@baya-framework.org)

---

# Versioning

We follow Semantic Versioning.

* Major → breaking change
* Minor → new feature
* Patch → bug fix

---

# Maintainer Guidelines

Core maintainers:

* Review PRs
* Ensure architectural consistency
* Maintain backward compatibility
* Enforce documentation and tests

---

# License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

---

# Thank You

Baya aims to become a serious ML orchestration ecosystem.

Your contribution helps move it forward.

