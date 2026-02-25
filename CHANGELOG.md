# Changelog

All notable changes to this project will be documented in this file.

The format is based on:
Keep a Changelog (https://keepachangelog.com/en/1.0.0/)

This project adheres to:
Semantic Versioning (https://semver.org/)

---

## [0.1.0] - 2026-02-17

### Added
- Initial project structure
- Core ML project manager API
- Data loading (CSV, Excel, JSON, SQL)
- Data cleaning utilities
- Encoding utilities
- Scaling utilities
- Train/Test split
- Model training (classification, regression, neural networks)
- Evaluation metrics
- Visualization module
- Export system (CSV, Excel, JSON, PDF, DOCX, PNG, JPG)
- Pipeline orchestration engine (DAG-based)
- Hook system
- Middleware system
- Experiment tracker (local JSON-based)
- YAML config-driven workflows
- Plugin architecture (entry-point discovery)
- CLI interface
- State manager
- Logging system
- Validation system
- Metrics module
- Integration backends (sklearn, tensorflow, pytorch, scipy, statsmodels)
- Type support (`py.typed`)
- PyPI-ready packaging

---

## [0.2.0] - Unreleased

### Planned
- Parallel pipeline execution
- Advanced experiment metadata tracking
- Model registry support
- Plugin marketplace specification
- Distributed execution support
- REST API layer
- Web dashboard prototype
- Cloud storage integration

---

## [1.0.0] - Future

### Planned
- Stable public API
- Enterprise plugin SDK
- Remote experiment tracking server
- Model deployment utilities
- Production monitoring tools
- Full documentation portal

---

# Versioning Strategy

- MAJOR version when incompatible API changes are made
- MINOR version when functionality is added in a backward compatible manner
- PATCH version when backward compatible bug fixes are made

Example:

1.2.3
│ │ └── Patch
│ └──── Minor
└────── Major

---

# Notes

- Versions prior to 1.0.0 are considered experimental.
- API may change until stable release.
