AutoML
======

Bayaml includes built-in AutoML:

- Model comparison
- Cross-validation
- Leaderboard tracking
- Best-model selection

Example:

.. code-block:: python

   from bayaml import automl

   result = automl("iris.csv", target="species")