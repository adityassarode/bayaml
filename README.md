# Baya

Structured, production-ready ML orchestration framework.

## Highlights

- Unified `Project` API
- Deterministic context/state lifecycle
- DAG-based pipeline orchestration
- Working sklearn backend + model registry
- Built-in metrics, tracking, export, hooks, and CLI
- Minimal extension-ready subsystems for deployment, plugins, governance, security, optimization, monitoring

## Installation

```bash
pip install -e .
```

## Quickstart

```python
import baya as by

p = by.Project("data.csv", target="label", seed=42)
p.clean.fill_missing("feature1", "median")
p.split.train_test(test_size=0.2)
p.model.create("random_forest_classifier", n_estimators=100)
p.model.train()
p.model.predict()
metrics = p.evaluate.classification()
p.tracker.log_metrics(metrics)
p.tracker.finalize()
```

## CLI

```bash
baya --banner
baya registry list-models
baya run workflow.yaml
baya info
```

## Branding

```python
import baya
baya.info()                  # metadata only
baya.info(open_website=True) # optional website open
```

## Website

- https://baya-ml.dev
- Buy Me a Coffee: https://buymeacoffee.com/adityasarode
