Bayaml
======

.. raw:: html

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

----

Bayaml is a lightweight ML & AI orchestration framework designed for structured,
reproducible, and deployable machine learning workflows.

It features a deterministic execution engine and an intelligent Auto Mode
(``.auto()``) that interprets structured instructions using rule-based NLP,
without relying on external AI services. Your data remains completely local
and secure.

Auto Mode automatically manages:

- Data loading
- Safe preprocessing
- Task detection (classification or regression)
- Structured pipeline construction
- Model training
- Evaluation
- Deployment

Bayaml includes built-in AutoML capabilities such as model comparison,
cross-validation, leaderboard tracking, and best-model selection — all executed
within reproducible, hash-based execution plans.

It provides structured APIs across simple, fluent, and advanced orchestration
layers, along with natural-language-driven ML pipelines and export options
including REST deployment and ONNX.

Designed for engineers, researchers, startups, and ML teams.

----

Why Bayaml?
===========

Modern ML pipelines are often:

- Hard to reproduce
- Poorly structured
- Over-engineered
- Difficult to deploy

Bayaml provides a clean orchestration layer on top of scikit-learn to make ML:

- Reproducible
- Structured
- Deterministic
- Deployable

Without sacrificing flexibility.

----

Natural Language ML (.auto())
=============================

Train models using structured instructions:

.. code-block:: python

   from bayaml import Project

   p = Project()

   result = p.auto(
       "use https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv "
       "treat tip as target "
       "train regression model using linear regression"
   )

   print(result)

What Happens Automatically
--------------------------

- Dataset loading (CSV, URL, DataFrame)
- Target detection
- Task detection (classification/regression)
- Automatic categorical encoding
- Safe pipeline ordering
- Train-test split
- Model training
- Evaluation
- Deterministic plan hashing

This makes Bayaml a lightweight AutoML orchestration engine.

----

Execution Plan Preview
======================

Preview generated pipelines before execution:

.. code-block:: python

   plan = p.auto(
       "use data.csv treat price as target train regression model",
       preview=True
   )

   for step in plan.steps:
       print(step.name)

Bayaml builds a deterministic execution plan with hashing for reproducibility.

----

Core Capabilities
=================

- **Structured ML Orchestration**
  Layered architecture wrapping a deterministic execution engine.

- **Auto Encoding**
  Categorical columns automatically encoded before training.

- **Auto Task Detection**
  Classification vs regression inferred automatically.

- **AutoML Engine**
  Model comparison, leaderboard tracking, cross-validation.

- **Model Deployment**
  Export models for production use.

----

Deployment
==========

REST Deployment
---------------

.. code-block:: python

   p.auto(
       "use data.csv treat target as target "
       "train classification model "
       "deploy as rest"
   )

Generates a deployable REST bundle.

ONNX Export (Edge / C++ Ready)
------------------------------

.. code-block:: python

   p.auto(
       "use data.csv treat target as target "
       "train regression model "
       "deploy in c++"
   )

Exports model as ONNX.

----

Installation
============

.. code-block:: bash

   pip install bayaml

Dependencies:

- pandas
- numpy
- scikit-learn
- matplotlib
- pyyaml

----

API Layers
==========

Bayaml supports three levels of abstraction.

1. Simple API
-------------

.. code-block:: python

   from bayaml import quick_train

   metrics = quick_train(
       data="data.csv",
       target="Target",
       model="linear_regression"
   )

2. Fluent API
-------------

.. code-block:: python

   from bayaml import Bayaml

   metrics = (
       Baya("data.csv", target="Target")
       .train("logistic_regression")
       .evaluate()
   )

3. Advanced Orchestration API
-----------------------------

.. code-block:: python

   from bayaml import Project

   project = Project()
   project.data.load("data.csv")
   project.data.set_target("Target")
   project.split.train_test()
   project.model.create("linear_regression")
   project.model.train()
   project.evaluate.evaluate_regressor()

Full modular control.

----

AutoML
======

.. code-block:: python

   from bayaml import automl

   result = automl(
       data="data.csv",
       target="Target"
   )

   print(result["best_model"])
   print(result["best_score"])

Includes:

- Cross-validation
- Model comparison
- Leaderboard generation
- Best model selection
- Run tracking

----

Export System
=============

Export metrics, predictions, and reports:

- CSV
- JSON
- Excel (XLSX)
- PDF
- DOCX
- PNG / JPG

----

Output Modes
============

Bayaml supports multiple output rendering modes, allowing results to be displayed
in different formats depending on workflow, integration needs, or presentation style.

These modes control how model results, metrics, and execution details are formatted —
without affecting the underlying execution.

Available Output Modes
----------------------

1. ``pretty``      – Human-readable formatted output  
2. ``original``    – Raw native Bayaml execution result  
3. ``sklearn``     – scikit-learn compatible output format  
4. ``pandas``      – Pandas DataFrame structured output  
5. ``numpy``       – NumPy array structured output  
6. ``json``        – Machine-readable JSON output  
7. ``table``       – Clean tabular display format  
8. ``markdown``    – Markdown-rendered output  
9. ``latex``       – LaTeX formatted output  
10. ``diagnostic`` – Detailed execution diagnostics  

Example Usage
-------------

.. code-block:: python

   result = p.auto(
       "use iris.csv treat species as target train classification model",
       mode="pretty"
   )

   result = p.auto(
       "use iris.csv treat species as target train classification model",
       mode="json"
   )

Each mode adapts the output structure while keeping the execution deterministic
and reproducible.

Why This Matters
----------------

These output modes allow Bayaml to integrate seamlessly with:

- Research workflows (LaTeX, Markdown)
- Production systems (JSON, NumPy)
- Data pipelines (Pandas, sklearn)
- Debugging and diagnostics
- Human-readable reporting

This flexibility bridges experimentation, reporting, and deployment.

----

Architecture
============

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

----

Reproducibility
===============

Every ``.auto()`` run generates:

- Dataset hash
- Plan hash
- Ordered execution steps

Ensuring reproducible ML workflows.

----

Developer Setup
===============

.. code-block:: bash

   git clone https://github.com/adityassarode/bayaml
   cd bayaml
   pip install -e .[dev]
   pytest

----

Positioning
===========

Bayaml is ideal for:

- ML engineers building reproducible pipelines
- Startups needing fast ML deployment
- Data scientists wanting structured automation
- Teams needing deterministic ML workflows

----

License
=======

MIT License

----

Author
======

Bayaml is built and maintained by Aditya Sarode,
focused on scalable AI systems, ML architecture,
and production-ready engineering.

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   introduction
   installation
   quickstart
   automode
   automl
   deployment
   output_styles
   architecture
   cli
   api