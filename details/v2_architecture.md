# Baya v2 — Minimal, Stable, Backend-Agnostic Orchestration Engine

## 1) Architecture Diagram (Text)

```text
User API
  ├─ Flat Project API
  │   ├─ project.data
  │   ├─ project.model
  │   ├─ project.plot
  │   ├─ project.backend
  │   ├─ project.evaluate(...)
  │   ├─ project.export(...)
  │   ├─ project.deploy(...)
  │   ├─ project.guardian()
  │   └─ project.auto(...)
  │
  └─ High-level helpers
      ├─ quick_train(...)
      └─ Bayaml(...).train(...).evaluate()

Core Engine (deterministic, safety-first)
  ├─ Context / State
  ├─ Data Safety Layer
  ├─ Backend Abstraction Layer
  ├─ Evaluation Engine
  ├─ Plot Manager (matplotlib)
  ├─ Unified Export Router
  ├─ Guardian Engine
  └─ Tracking / Reproducibility

Automation Layer (structured intent)
  ├─ IntentParser
  ├─ PlanBuilder
  ├─ PlanValidator
  ├─ ExecutionEngine
  └─ PlanLogger

Plugin/Extension Layer
  ├─ Backend Plugins
  ├─ Model Registry Plugins
  └─ Deployment Scaffold Providers
```

---

## 2) New Project Class (Flat API Contract)

```python
class Project:
    def __init__(self, data, target: str, backend: str = "sklearn", seed: int = 42, workspace: str | None = None): ...

    # flat subsystems
    data: DataModule
    model: ModelModule
    plot: PlotManager
    backend: BackendHandle
    gpu: GPUControl

    # flat operations
    def evaluate(self, mode: str = "dict"): ...
    def export(self, path: str): ...
    def auto(self, intent_or_config, *, preview: bool = False, auto_confirm: bool = False, mode: str = "safe", explain: bool = False): ...
    def guardian(self): ...
    def deploy(self, target: str): ...

    # short-chain helpers
    def train(self, model_name: str, **params): ...
    def run(self, model_name: str, **params): ...
```

### Design Rules
- Flat API only; avoid deep chains (`project.export("x.csv")` not nested exporter trees).
- Always keep full raw access.
- Never hide state transitions.

---

## 3) BaseBackend + SklearnBackend

```python
class BaseBackend:
    name: str
    version: str

    def create_model(self, name: str, **params): ...
    def train(self, model, X_train, y_train, **kwargs): ...
    def predict(self, model, X): ...
    def raw_model(self, model): ...
```

```python
class SklearnBackend(BaseBackend):
    name = "sklearn"
    version = "v1"

    # model catalog + deterministic random_state handling
    # create_model/train/predict implemented with sklearn estimators
```

### Backend requirements
- deterministic training with explicit seed handling
- task compatibility checks (classifier vs regressor)
- no global hidden state

---

## 4) TensorFlowBackend Skeleton

```python
class TensorFlowBackend(BaseBackend):
    name = "tensorflow"
    version = "skeleton-v1"

    def create_model(self, name: str, **params):
        raise NotImplementedError("TensorFlow backend skeleton. Provide concrete model factory.")

    def train(self, model, X_train, y_train, **kwargs):
        raise NotImplementedError

    def predict(self, model, X):
        raise NotImplementedError

    def raw_model(self, model):
        return model
```

---

## 5) PlotManager Implementation Contract (matplotlib-only)

```python
class PlotManager:
    def histogram(self, col: str, save: str | None = None): ...
    def scatter(self, x: str, y: str, save: str | None = None): ...
    def box(self, col: str, save: str | None = None): ...
    def correlation(self, save: str | None = None): ...
    def confusion_matrix(self, save: str | None = None): ...
```

### Rules
- always produce matplotlib figure
- persist `last_figure` in context
- if `save` passed, auto-save via extension router (png/jpg)
- explicit errors when required preconditions not met

---

## 6) Unified Export System

`project.export(path)` routes by extension:
- tabular: `csv`, `json`, `xlsx`
- reports: `pdf`, `docx`
- figure: `png`, `jpg`
- model artifact: `onnx`

### Resolution precedence
1. If extension is image and last figure exists -> export figure
2. If extension is tabular and dataframe exists -> export dataframe
3. If extension is model artifact and model exists -> export model
4. If extension is report and metrics exist -> export metrics/report
5. else explicit error

No nested exporters, no hidden fallback.

---

## 7) EvaluateModule Rewrite Contract

`project.evaluate(mode="pretty" | "dict" | "full")`

### Task autodetection
- classification if target dtype in `{bool, int-like categorical, object/category}`
- regression otherwise

### Classification metrics
- accuracy, precision, recall, f1
- confusion matrix
- classification report
- average strategy:
  - binary -> `binary`
  - multiclass -> `weighted`

### Regression metrics
- r2, mse, rmse, mae

### Modes
- `pretty`: print readable summary + warnings
- `dict`: return compact metrics dict
- `full`: return metrics + artifacts + metadata

No duplicated eval logic across APIs.

---

## 8) Data Safety Layer

`project.data.validate()` checks:
- schema presence and target existence
- dtype sanity
- NaN ratio thresholds
- overflow/inf detection
- sample-feature ratio warnings

### Mutation policy
- default copy-on-write
- `inplace=True` explicitly required for in-place updates
- preserve float64 where possible
- detect and block corruption patterns

---

## 9) Guardian Intelligence Engine

`project.guardian()` returns structured warnings.

### Components
- `DataInspector`
- `LeakageDetector`
- `OverfitDetector`
- `StabilityAnalyzer`
- `CollinearityAnalyzer`
- `RiskScorer`

### Checks
- leakage risk
- imbalance risk
- overfitting risk
- high multicollinearity
- low sample/feature ratio
- instability under resampling

### Output
```json
{
  "risk_level": "low|medium|high",
  "stability_score": 0.81,
  "warnings": ["..."],
  "signals": {...}
}
```

---

## 10) baya.auto() Structured Automation Engine

### Core Principle
Never execute free-form AI code.

### Pipeline
1. `IntentParser`
2. `PlanBuilder`
3. `PlanValidator`
4. `ExecutionEngine`
5. `PlanLogger`

### API
```python
project.auto(intent_or_config, preview=True, auto_confirm=False, mode="safe", explain=False)
```

### Modes
- `safe`: strict ordering + checks
- `fast`: minimal extras
- `teach`: explain steps/decisions
- `production`: include guardian + export-ready bundle checks

### Plan preview
- deterministic numbered steps
- user confirmation required unless `auto_confirm=True`

### Interactive plan editing (design contract)
```python
plan = project.auto("train classification model", preview=True)
plan.modify(step=3, params={"model": "random_forest_classifier"})
plan.execute()
```

---

## 11) Internal DSL for Plan Representation

```python
@dataclass(frozen=True)
class PlanStep:
    id: str
    op: str                 # e.g., "clean.fill_missing", "split.train_test", "model.train"
    params: dict
    depends_on: tuple[str, ...] = ()
    safety_level: str = "strict"

@dataclass(frozen=True)
class ExecutionPlan:
    version: str
    steps: tuple[PlanStep, ...]
    metadata: dict          # dataset_hash, seed, mode, intent_hash
```

### Deterministic mapping rules
- same intent + same config + same schema -> same plan hash
- no unordered dict iteration in rendering/hashing

---

## 12) IntentParser Architecture

### Subcomponents
- `Tokenizer`
- `IntentClassifier`
- `EntityExtractor`
- `IntentMapper`

### IntentGraph
```python
@dataclass
class IntentGraph:
    cleaning: list
    features: list
    modeling: list
    evaluation: list
    plotting: list
    exporting: list
    guardian: list
    deployment: list
```

### Deterministic NLP->Plan mapping
- explicit phrase-to-intent mapping tables
- explicit column/model/metric entity extraction
- unknown/ambiguous intents produce validation error, not execution guess

---

## 13) Backend Plugin System Spec

### Registration
```python
register_backend(name: str, backend_cls: type[BaseBackend])
get_backend(name: str) -> BaseBackend
list_backends() -> list[str]
```

### Contract checks at registration
- required methods implemented
- version string present
- deterministic capability declaration

### Plugin lifecycle
- register during startup/bootstrap
- immutable registry snapshot for each run (hashable)

---

## 14) Deployment Scaffold Generator Architecture

`project.deploy("cpp"|"java"|"rest")`

### Output bundle
- serialized model artifact (onnx when available)
- preprocessing schema contract
- feature order metadata
- minimal inference scaffold for chosen target

### Components
- `SchemaFreezer`
- `ArtifactExporter`
- `ScaffoldGenerator`
- `BundleWriter`

If full target support missing, raise explicit `NotImplementedError`; never fake success.

---

## 15) Stability Scoring Formula (Mathematical)

Given metric values across `k` folds and `s` seed repeats:
- let `m_ij` be metric for fold `i`, seed `j`
- global mean: `mu = mean(m_ij)`
- global std: `sigma = std(m_ij)`
- coefficient of variation: `cv = sigma / (|mu| + eps)`

Proposed stability score:

```text
stability_score = max(0, 1 - min(1, cv / tau))
```

Where:
- `eps = 1e-8`
- `tau` is tolerance (default `0.15`)

Interpretation:
- `>= 0.85`: high stability
- `0.65 - 0.85`: moderate
- `< 0.65`: unstable

---

## 16) Plan Hashing & Reproducibility Protocol

### Inputs to hash
- canonicalized plan JSON
- dataset hash (stable schema+content hash)
- config hash
- backend snapshot hash
- seed

### Canonicalization rules
- sorted keys
- UTF-8 encoding
- float normalization where feasible
- explicit versioned schema for plan payload

### Hash
```text
plan_hash = sha256(canonical_payload)
```

### Stored for each run
- run_id
- plan_hash
- dataset_hash
- config_hash
- backend_hash
- code_version
- timestamp (UTC)
- executed steps and durations

---

## 17) Example Short Usage

```python
from baya import quick_train

metrics = quick_train(data="train.csv", target="Outcome", model="logistic_regression")
print(metrics)
```

## 18) Example Advanced Usage

```python
from baya import Project

p = Project("train.csv", target="Outcome", backend="sklearn")
p.data.validate()
p.model.create("random_forest_classifier", n_estimators=200)
p.model.train()       # auto-predict may run when safe
report = p.evaluate(mode="full")
warnings = p.guardian()
p.export("model.onnx")
```

## 19) Migration Guide (v1 -> v2)

### Keep working
- `quick_train(...)`
- `Baya(...).train(...).evaluate()`
- `Project.from_config(...)`
- CLI `run` flow

### Prefer in v2
- flat `project.export("...")` (single entry)
- flat `project.evaluate(mode=...)`
- `project.auto(...)` with preview/validation
- `project.guardian()` post-training checks

### Deprecated patterns
- deep nested exporter chains
- implicit unsafe order operations
- opaque auto execution without plan preview

---

## 20) Stability, Determinism, Safety, Transparency Checklist

- Stability first: deterministic step execution
- Determinism first: seeded operations + plan hash
- Safety first: validation before execution
- Transparency first: explain/preview/log everything
- Flat API: no deep facades
- Minimal surface area: explicit modules, no hidden magic
