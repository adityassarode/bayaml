# Quickstart

```python
import baya as by
p = by.Project("data.csv", target="label")
p.split.train_test()
p.model.create("random_forest_classifier")
p.model.train()
p.model.predict()
print(p.evaluate.classification())
```
