Auto Mode (.auto())
===================

Auto Mode allows structured natural-language instructions.

Example:

.. code-block:: python

   p.auto(
       "use iris.csv treat species as target train classification model"
   )

Auto Mode automatically:

- Loads data
- Detects task type
- Applies preprocessing
- Builds safe pipeline
- Trains model
- Evaluates results
- Generates reproducible execution plan