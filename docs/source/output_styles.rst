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