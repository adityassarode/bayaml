# Baya

Structured, production-ready ML orchestration + AutoML experiment framework.

## Installation

```bash
pip install baya
```

## Simple API (one call)

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

## Advanced API

```python
from baya import Project

project = Project.from_config("workflow.yaml")
metrics = project.run()
print(metrics)
```

## AutoML

```python
import pandas as pd
from baya import baya

result = baya(pd.read_csv("data.csv"), target="Target")
print(result["best_model"], result["best_score"])
```

Returned structure:

```python
{
  "run_id": "...",
  "task": "classification|regression",
  "best_model": "...",
  "best_score": 0.0,
  "leaderboard": [...],
  "cv_results": {...}
}
```

## Cross-validation

- Enabled by default inside AutoML.
- Uses `StratifiedKFold` for classification.
- Uses `KFold` for regression.

## Hyperparameter tuning

- Grid search + random search (small search spaces by design).
- AutoML runs HPO when `param_grids` are provided.

## Model registry

```python
from sklearn.tree import DecisionTreeClassifier
from baya import register_model, list_models

register_model("decision_tree_classifier", DecisionTreeClassifier)
print(list_models())
```

## Leaderboard persistence

AutoML appends run results to:

```text
baya_runs/leaderboard.json
```

## Visualization

```python
from baya.visualize import plot_leaderboard, plot_metric_history

plot_leaderboard()
plot_metric_history("<run_id>")
```

## CLI

```bash
baya --banner
baya run workflow.yaml
baya automl workflow.yaml
baya leaderboard
baya visualize leaderboard
baya registry list-models
baya info
```

No branding is printed on import.
