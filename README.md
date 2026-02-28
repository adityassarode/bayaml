# Baya
<p align="center">  
  
<a href="https://pypi.org/project/baya/">  
  <img src="https://img.shields.io/pypi/v/baya?style=for-the-badge&color=blue&label=PyPI" />  
</a>  
  
<a href="https://github.com/adityassarode">  
  <img src="https://img.shields.io/badge/GitHub-adityassarode-black?style=for-the-badge&logo=github&logoColor=white" />  
</a>  
  
<a href="https://www.instagram.com/adityassarode">  
  <img src="https://img.shields.io/badge/Instagram-@adityassarode-E4405F?style=for-the-badge&logo=instagram&logoColor=white" />  
</a>  
  
<a href="https://www.buymeacoffee.com/adityassarode">  
  <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" />  
</a>  
  
<a href="https://ko-fi.com/adityassarode">  
  <img src="https://img.shields.io/badge/Ko--fi-Support-ff5e5b?style=for-the-badge&logo=ko-fi&logoColor=white" />  
</a>  
  
</p>  

---

🚀 Baya — Lightweight ML Orchestration & AutoML Framework

Baya is a structured Machine Learning orchestration framework for reproducible, automated, and production-ready ML workflows.

It combines:

AutoML

Natural language ML pipelines

Deterministic execution plans

Model deployment

Modular pipeline control


Designed for engineers, researchers, startups, and ML teams.


---

🔎 Why Baya?

Modern ML pipelines are often:

Hard to reproduce

Poorly structured

Over-engineered

Difficult to deploy


Baya provides a clean orchestration layer on top of scikit-learn to make ML:

Reproducible

Structured

Deterministic

Deployable


Without sacrificing flexibility.


---

🧠 Natural Language ML (.auto())

Train models using structured instructions:

```python
from baya import Project

p = Project()

result = p.auto(
    "use https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv "
    "treat tip as target "
    "train regression model using linear regression"
)

print(result)
```

What Happens Automatically

Dataset loading (CSV, URL, DataFrame)

Target detection

Task detection (classification/regression)

Automatic categorical encoding

Safe pipeline ordering

Train-test split

Model training

Evaluation

Deterministic plan hashing


This makes Baya a lightweight AutoML orchestration engine.


---

📊 Execution Plan Preview

Preview generated pipelines before execution:

```python
plan = p.auto(
    "use data.csv treat price as target train regression model",
    preview=True
)

for step in plan.steps:
    print(step.name)
```
Baya builds a deterministic execution plan with hashing for reproducibility.


---

⚙️ Core Capabilities

✔ Structured ML Orchestration

Layered architecture wrapping a deterministic execution engine.

✔ Auto Encoding

Categorical columns are automatically encoded before model training.

✔ Auto Task Detection

Classification vs regression inferred automatically.

✔ AutoML Engine

Model comparison, leaderboard tracking, cross-validation.

✔ Model Deployment

Export models for production use.


---

🚀 Deployment

### REST Deployment

```python
p.auto(
    "use data.csv treat target as target "
    "train classification model "
    "deploy as rest"
)
```

Generates a deployable REST bundle.


---

### ONNX Export (Edge / C++ Ready)

```python
p.auto(
    "use data.csv treat target as target "
    "train regression model "
    "deploy in c++"
)
```

Exports model as ONNX.


---

📦 Installation

```bash
pip install baya
```

Dependencies:

*   pandas
*   numpy
*   scikit-learn
*   matplotlib
*   pyyaml


---

🧩 API Layers

Baya supports three levels of abstraction.


---

### 1️⃣ Simple API

```python
from baya import quick_train

metrics = quick_train(
    data="data.csv",
    target="Target",
    model="linear_regression"
)
```

---

### 2️⃣ Fluent API

```python
from baya import Baya

metrics = (
    Baya("data.csv", target="Target")
    .train("logistic_regression")
    .evaluate()
)
```

---

### 3️⃣ Advanced Orchestration API

```python
from baya import Project

project = Project()
project.data.load("data.csv")
project.data.set_target("Target")
project.split.train_test()
project.model.create("linear_regression")
project.model.train()
project.evaluate.evaluate_regressor()
```
Full modular control.


---

🤖 AutoML

```python
from baya import automl

result = automl(
    data="data.csv",
    target="Target"
)

print(result["best_model"])
print(result["best_score"])
```

Includes:

*   Cross-validation
*   Model comparison
*   Leaderboard generation
*   Best model selection
*   Run tracking


---

📤 Export System

Export metrics, predictions, and reports:

*   CSV
*   JSON
*   Excel (XLSX)
*   PDF
*   DOCX
*   PNG / JPG


---

🏗 Architecture

Core Engine
↓
Execution Plan Builder
↓
Deterministic Plan Hashing
↓
Project API
↓
AutoML / CLI / Simple API

All APIs wrap the same deterministic engine.

No duplicated logic.


---

🔐 Reproducibility

Every `.auto()` run generates:

*   Dataset hash
*   Plan hash
*   Ordered execution steps

Ensuring reproducible ML workflows.


---

👨‍💻 Developer Setup

```bash
git clone https://github.com/adityassarode/baya
cd baya
pip install -e .[dev]
pytest
```

---

📈 Positioning

Baya is ideal for:

*   ML engineers building reproducible pipelines
*   Startups needing fast ML deployment
*   Data scientists wanting structured automation
*   Teams needing deterministic ML workflows


---

📄 License

MIT License


---

👤 Author

Baya is built and maintained by Aditya Sarode, focused on scalable AI systems, ML architecture, and production-ready engineering.
It combines:

AutoML

Natural language ML pipelines

Deterministic execution plans

Model deployment

Modular pipeline control


Designed for engineers, researchers, startups, and ML teams.


---

🔎 Why Baya?

Modern ML pipelines are often:

Hard to reproduce

Poorly structured

Over-engineered

Difficult to deploy


Baya provides a clean orchestration layer on top of scikit-learn to make ML:

Reproducible

Structured

Deterministic

Deployable


Without sacrificing flexibility.


---

🧠 Natural Language ML (.auto())

Train models using structured instructions:

from baya import Project

p = Project()

result = p.auto(
    "use https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv "
    "treat tip as target "
    "train regression model using linear regression"
)

print(result)

What Happens Automatically

Dataset loading (CSV, URL, DataFrame)

Target detection

Task detection (classification/regression)

Automatic categorical encoding

Safe pipeline ordering

Train-test split

Model training

Evaluation

Deterministic plan hashing


This makes Baya a lightweight AutoML orchestration engine.


---

📊 Execution Plan Preview

Preview generated pipelines before execution:

plan = p.auto(
    "use data.csv treat price as target train regression model",
    preview=True
)

for step in plan.steps:
    print(step.name)

Baya builds a deterministic execution plan with hashing for reproducibility.


---

⚙️ Core Capabilities

✔ Structured ML Orchestration

Layered architecture wrapping a deterministic execution engine.

✔ Auto Encoding

Categorical columns are automatically encoded before model training.

✔ Auto Task Detection

Classification vs regression inferred automatically.

✔ AutoML Engine

Model comparison, leaderboard tracking, cross-validation.

✔ Model Deployment

Export models for production use.


---

🚀 Deployment

REST Deployment

p.auto(
    "use data.csv treat target as target "
    "train classification model "
    "deploy as rest"
)

Generates a deployable REST bundle.


---

ONNX Export (Edge / C++ Ready)

p.auto(
    "use data.csv treat target as target "
    "train regression model "
    "deploy in c++"
)

Exports model as ONNX.


---

📦 Installation

pip install baya

Dependencies:

pandas

numpy

scikit-learn

matplotlib

pyyaml



---

🧩 API Layers

Baya supports three levels of abstraction.


---

1️⃣ Simple API

from baya import quick_train

metrics = quick_train(
    data="data.csv",
    target="Target",
    model="linear_regression"
)


---

2️⃣ Fluent API

from baya import Baya

metrics = (
    Baya("data.csv", target="Target")
    .train("logistic_regression")
    .evaluate()
)


---

3️⃣ Advanced Orchestration API

from baya import Project

project = Project()
project.data.load("data.csv")
project.data.set_target("Target")
project.split.train_test()
project.model.create("linear_regression")
project.model.train()
project.evaluate.evaluate_regressor()

Full modular control.


---

🤖 AutoML

from baya import automl

result = automl(
    data="data.csv",
    target="Target"
)

print(result["best_model"])
print(result["best_score"])

Includes:

Cross-validation

Model comparison

Leaderboard generation

Best model selection

Run tracking



---

📤 Export System

Export metrics, predictions, and reports:

CSV

JSON

Excel (XLSX)

PDF

DOCX

PNG / JPG



---

🏗 Architecture

Core Engine
↓
Execution Plan Builder
↓
Deterministic Plan Hashing
↓
Project API
↓
AutoML / CLI / Simple API

All APIs wrap the same deterministic engine.

No duplicated logic.


---

🔐 Reproducibility

Every .auto() run generates:

Dataset hash

Plan hash

Ordered execution steps


Ensuring reproducible ML workflows.


---

👨‍💻 Developer Setup

git clone https://github.com/adityassarode/baya
cd baya
pip install -e .[dev]
pytest


---

📈 Positioning

Baya is ideal for:

ML engineers building reproducible pipelines

Startups needing fast ML deployment

Data scientists wanting structured automation

Teams needing deterministic ML workflows



---

📄 License

MIT License


---

👤 Author

Baya is built and maintained by Aditya Sarode, focused on scalable AI systems, ML architecture, and production-ready engineering.
