from bayaml import Project
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"

ALL_MODES = [
    "dict",
    "original",
    "pretty",
    "full",
    "sklearn",
    "table",
    "pandas",
    "numpy",
    "json",
    "markdown",
    "latex",
    "diagnostic",
]


# =========================================================
# MANUAL REGRESSION
# =========================================================
print("\n==============================")
print("        MANUAL REGRESSION")
print("==============================")

manual = Project()
manual.data.load(DATA_URL)
manual.data.set_target("tip")

# Encode features (target is numeric so safe)
df = manual.context.ensure_dataframe()
target = manual.context.get_target()
feature_cols = [c for c in df.columns if c != target]
df_encoded = pd.get_dummies(df, columns=feature_cols, drop_first=False)

manual.data.load(df_encoded)
manual.context.set_target("tip")

manual.split.train_test(test_size=0.2)
manual.model.create("linear_regression")
manual.model.train()

for mode in ALL_MODES:
    print(f"\n---- Regression Mode: {mode.upper()} ----")
    manual.evaluate.regression(mode=mode)


# =========================================================
# MANUAL CLASSIFICATION
# =========================================================
print("\n==============================")
print("        MANUAL CLASSIFICATION")
print("==============================")

manual_cls = Project()
manual_cls.data.load(DATA_URL)
manual_cls.data.set_target("sex")

# Encode only features, not target
df = manual_cls.context.ensure_dataframe()
target = manual_cls.context.get_target()
feature_cols = [c for c in df.columns if c != target]
df_encoded = pd.get_dummies(df, columns=feature_cols, drop_first=False)

manual_cls.data.load(df_encoded)
manual_cls.context.set_target("sex")

manual_cls.split.train_test(test_size=0.2)
manual_cls.model.create("logistic_regression")
manual_cls.model.train()

for mode in ALL_MODES:
    print(f"\n---- Classification Mode: {mode.upper()} ----")
    manual_cls.evaluate.classification(mode=mode)


# =========================================================
# AUTO REGRESSION
# =========================================================
print("\n==============================")
print("        AUTO REGRESSION")
print("==============================")

for mode in ALL_MODES:
    print(f"\n---- AUTO Regression Mode: {mode.upper()} ----")

    auto = Project()

    auto.auto(
        f"use {DATA_URL} "
        "treat tip as target "
        "train regression model using linear regression "
        f"evaluate model {mode}"
    )


# =========================================================
# AUTO CLASSIFICATION
# =========================================================
print("\n==============================")
print("        AUTO CLASSIFICATION")
print("==============================")

for mode in ALL_MODES:
    print(f"\n---- AUTO Classification Mode: {mode.upper()} ----")

    auto_cls = Project()

    auto_cls.auto(
        f"use {DATA_URL} "
        "treat sex as target "
        "train classification model using logistic regression "
        f"evaluate model {mode}"
    )


print("\n==============================")
print("        ALL TESTS COMPLETED")
print("==============================")
