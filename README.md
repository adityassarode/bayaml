# Baya

Structured, production-ready ML orchestration framework.


## Installation

```bash
pip install baya
```

## Simple API (one call)

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
from baya import quick_train

metrics = quick_train(
    data="data.csv",
    target="Target",
    model="linear_regression",
)
print(metrics)
```

## Fluent API (reduced lines)

```python
from baya import Baya

metrics = (
    Baya("data.csv", target="Target")
    .train("linear_regression")
    .evaluate()
)
print(metrics)
```

## Advanced API (full control)

```python
from baya import Project

project = Project.from_config("workflow.json")
metrics = project.run()
print(metrics)
```

`Project.from_config(...)` supports:
- JSON file path string
- YAML file path string
- `pathlib.Path`
- dictionary config
- internal `ConfigSchema`


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

