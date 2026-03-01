# Bayaml
<p align="center">  
  
<a href="https://pypi.org/project/bayaml/">  
  <img src="https://img.shields.io/pypi/v/bayaml?style=for-the-badge&color=blue&label=PyPI" />  
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

Bayaml is a lightweight ML & AI orchestration framework designed for structured, reproducible, and deployable machine learning workflows.

It features a deterministic execution engine and an intelligent Auto Mode (.auto()) that interprets structured instructions using rule-based NLP, without relying on external AI services, ensuring your data remains completely local and secure.

Auto Mode automatically manages data loading, safe preprocessing, task detection (classification or regression), structured pipeline construction, model training, evaluation, and deployment.

Bayaml includes built-in AutoML capabilities such as model comparison, cross-validation, leaderboard tracking, and best-model selection, all executed within reproducible, hash-based execution plans.

It provides structured APIs across simple, fluent, and advanced orchestration layers, along with natural-language-driven ML pipelines and export options including REST deployment and ONNX.

Bayaml is built to bring automation, structure, reproducibility, and privacy to modern ML systems.

It combines:

AutoML

Natural language ML pipelines

Deterministic execution plans

Model deployment

Modular pipeline control


Designed for engineers, researchers, startups, and ML teams.


---

🔎 Why Bayaml?

Modern ML pipelines are often:

Hard to reproduce

Poorly structured

Over-engineered

Difficult to deploy


Bayaml provides a clean orchestration layer on top of scikit-learn to make ML:

Reproducible

Structured

Deterministic

Deployable


Without sacrificing flexibility.


---

🧠 Natural Language ML (.auto())

Train models using structured instructions:

```python
from bayaml import Project

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


This makes Bayaml a lightweight AutoML orchestration engine.


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
Bayaml builds a deterministic execution plan with hashing for reproducibility.


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
pip install bayaml
```

Dependencies:

*   pandas
*   numpy
*   scikit-learn
*   matplotlib
*   pyyaml


---

🧩 API Layers

Bayaml supports three levels of abstraction.


---

### 1️⃣ Simple API

```python
from bayaml import quick_train

metrics = quick_train(
    data="data.csv",
    target="Target",
    model="linear_regression"
)
```

---

### 2️⃣ Fluent API

```python
from bayaml import Bayaml

metrics = (
    Baya("data.csv", target="Target")
    .train("logistic_regression")
    .evaluate()
)
```

---

### 3️⃣ Advanced Orchestration API

```python
from bayaml import Project

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
from bayaml import automl

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
git clone https://github.com/adityassarode/bayaml
cd bayaml
pip install -e .[dev]
pytest
```

---

📈 Positioning

Bayaml is ideal for:

*   ML engineers building reproducible pipelines
*   Startups needing fast ML deployment
*   Data scientists wanting structured automation
*   Teams needing deterministic ML workflows


---

📄 License

MIT License


---

👤 Author

Bayaml is built and maintained by Aditya Sarode, focused on scalable AI systems, ML architecture, and production-ready engineering.
