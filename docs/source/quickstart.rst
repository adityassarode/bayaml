Quick Start
===========

Basic usage:

.. code-block:: python

   from bayaml import Project

   p = Project("iris.csv", target="species")
   p.split.train_test()
   p.model.create("logistic_regression")
   p.run()