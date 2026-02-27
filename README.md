# Baya

Structured, production-ready ML orchestration framework.

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

No branding is printed on import.
