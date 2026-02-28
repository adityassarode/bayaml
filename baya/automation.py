from __future__ import annotations

import ast
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


@dataclass(frozen=True)
class PlanStep:
    name: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionPlan:
    steps: list[PlanStep]
    dataset_hash: str
    plan_hash: str
    model_name: str | None = None


def hash_dataframe(df: pd.DataFrame) -> str:
    hashed = pd.util.hash_pandas_object(df, index=True).values
    return hashlib.sha256(hashed.tobytes()).hexdigest()


class IntentParser:
    _URL = re.compile(r"(https?://\S+\.csv)", re.IGNORECASE)
    _PATH = re.compile(r"(?:use\s+)?([\w./-]+\.(?:csv|xlsx))", re.IGNORECASE)
    _MATRIX = re.compile(r"(\[\s*\[.*\]\s*\])", re.DOTALL)
    _FILL = re.compile(r"fill\s+([a-zA-Z_][\w]*)\s+with\s+([\w\.-]+)", re.IGNORECASE)
    _HIST = re.compile(r"plot\s+histogram\s+of\s+([a-zA-Z_][\w]*)", re.IGNORECASE)
    _SCATTER = re.compile(r"scatter\s+([a-zA-Z_][\w]*)\s+vs\s+([a-zA-Z_][\w]*)", re.IGNORECASE)
    _EXPORT = re.compile(r"(?:export|save)\s+([\w./-]+\.(?:pdf|csv|json|xlsx|onnx))", re.IGNORECASE)

    def parse(self, instruction: str) -> dict[str, Any]:
        text = " ".join(instruction.strip().split())
        lower = text.lower()

        intents: list[PlanStep] = []

        matrix_raw = self._search(self._MATRIX, text)
        dataset_url = self._search(self._URL, text)
        export_path = self._search(self._EXPORT, text)
        dataset_path = self._search(self._PATH, text)
        if dataset_path and export_path and dataset_path == export_path:
            dataset_path = None

        if matrix_raw:
            intents.append(
                PlanStep(
                    "load_matrix",
                    {
                        "matrix_raw": matrix_raw,
                        "last_column_target": "last column as target" in lower,
                    },
                )
            )
        elif dataset_url:
            intents.append(PlanStep("load_dataset", {"source": dataset_url}))
        elif dataset_path:
            intents.append(PlanStep("load_dataset", {"source": dataset_path}))

        if "remove null values" in lower or "drop nulls" in lower:
            intents.append(PlanStep("clean_drop_nulls", {}))
        if "drop duplicates" in lower:
            intents.append(PlanStep("clean_drop_duplicates", {}))

        for col, value in self._FILL.findall(text):
            intents.append(PlanStep("clean_fill", {"column": col, "value": value}))

        task = None
        if "train classification model" in lower:
            task = "classification"
        elif "train regression model" in lower or "train regression" in lower:
            task = "regression"

        model_name = None
        if "random forest" in lower:
            model_name = "random_forest_regressor" if task == "regression" else "random_forest_classifier"
        elif "logistic regression" in lower:
            task = task or "classification"
            model_name = "logistic_regression"
        elif "linear regression" in lower:
            task = task or "regression"
            model_name = "linear_regression"

        if "evaluate model" in lower or "evaluate with" in lower:
            intents.append(PlanStep("evaluate", {}))
        if "show confusion matrix" in lower:
            intents.append(PlanStep("plot_confusion_matrix", {}))

        for col in self._HIST.findall(text):
            intents.append(PlanStep("plot_histogram", {"column": col}))
        for x, y in self._SCATTER.findall(text):
            intents.append(PlanStep("plot_scatter", {"x": x, "y": y}))

        if export_path:
            intents.append(PlanStep("export", {"path": export_path}))

        if "deploy in c++" in lower:
            intents.append(PlanStep("deploy", {"mode": "onnx", "output": "model.onnx"}))
        elif "deploy as rest" in lower or "deploy model" in lower:
            intents.append(PlanStep("deploy", {"mode": "rest", "output": "deployment_bundle"}))

        if task:
            intents.append(PlanStep("set_task", {"task": task}))

        return {"steps": intents, "task": task, "model_name": model_name}

    @staticmethod
    def _search(pattern: re.Pattern[str], text: str) -> str | None:
        match = pattern.search(text)
        return match.group(1) if match else None


class PlanValidator:
    def validate(self, plan: ExecutionPlan) -> None:
        names = [s.name for s in plan.steps]

        if "train" in names and not any(n in names for n in ["load_dataset", "load_matrix", "use_existing_data"]):
            raise ValueError("Dataset must exist before training.")

        if names.count("split") > 1:
            raise ValueError("No double split allowed.")

        if "train" in names and "split" not in names:
            raise ValueError("Split must run before training.")

        if "evaluate" in names and "train" in names and names.index("evaluate") < names.index("train"):
            raise ValueError("Train before evaluate.")

        if "plot_confusion_matrix" in names and "evaluate" in names and names.index("plot_confusion_matrix") < names.index("evaluate"):
            raise ValueError("Evaluate before confusion matrix.")

        if "train" in names and "set_target" not in names and "set_target_last_column" not in names:
            # target may already exist in Project state and will be checked at execution time
            pass


def parse_matrix(matrix_raw: str) -> pd.DataFrame:
    try:
        payload = ast.literal_eval(matrix_raw)
    except (SyntaxError, ValueError) as exc:
        raise ValueError("Invalid matrix literal.") from exc

    if not isinstance(payload, list) or not payload or not all(isinstance(row, list) for row in payload):
        raise ValueError("Matrix must be a list of lists.")

    width = len(payload[0])
    for row in payload:
        if len(row) != width:
            raise ValueError("Matrix rows must have equal length.")
        for value in row:
            if not isinstance(value, (int, float, np.integer, np.floating)):
                raise ValueError("Matrix values must be numeric.")

    columns = [f"col_{i}" for i in range(width)]
    return pd.DataFrame(payload, columns=columns)


class ExecutionEngine:
    def __init__(self, project: Any) -> None:
        self.project = project
        self.exports: list[str] = []
        self.deployments: list[str] = []
        self.model_name: str | None = None
        self.task: str | None = None

    def execute(self, plan: ExecutionPlan) -> dict[str, Any]:
        allowed_calls = {
            "use_existing_data": self._use_existing_data,
            "load_dataset": self._load_dataset,
            "load_matrix": self._load_matrix,
            "set_target": self._set_target,
            "set_target_last_column": self._set_target_last_column,
            "clean_drop_nulls": self._clean_drop_nulls,
            "clean_drop_duplicates": self._clean_drop_duplicates,
            "clean_fill": self._clean_fill,
            "split": self._split,
            "train": self._train,
            "evaluate": self._evaluate,
            "plot_confusion_matrix": self._plot_confusion_matrix,
            "plot_histogram": self._plot_histogram,
            "plot_scatter": self._plot_scatter,
            "export": self._export,
            "deploy": self._deploy,
            "set_task": self._set_task,
        }

        for step in plan.steps:
            handler = allowed_calls.get(step.name)
            if handler is None:
                raise ValueError(f"Unsupported step: {step.name}")
            handler(step.params)

        return {
            "steps_executed": [s.name for s in plan.steps],
            "model_used": self.model_name,
            "exports_generated": self.exports,
            "deployment_status": self.deployments,
            "plan_hash": plan.plan_hash,
        }

    def _use_existing_data(self, _: dict[str, Any]) -> None:
        self.project.context.ensure_dataframe()

    def _load_dataset(self, params: dict[str, Any]) -> None:
        self.project.data.load(params["source"])

    def _load_matrix(self, params: dict[str, Any]) -> None:
        df = parse_matrix(params["matrix_raw"])
        self.project.data.load(df)
        if params.get("last_column_target"):
            self.project.context.set_target(df.columns[-1])

    def _set_target(self, params: dict[str, Any]) -> None:
        self.project.context.set_target(params["target"])

    def _set_target_last_column(self, _: dict[str, Any]) -> None:
        df = self.project.context.ensure_dataframe()
        self.project.context.set_target(df.columns[-1])

    def _clean_drop_nulls(self, _: dict[str, Any]) -> None:
        self.project.clean.drop_nulls()

    def _clean_drop_duplicates(self, _: dict[str, Any]) -> None:
        self.project.clean.drop_duplicates()

    def _clean_fill(self, params: dict[str, Any]) -> None:
        column = params["column"]
        raw = params["value"]
        if raw in {"mean", "median", "mode"}:
            self.project.clean.fill_missing(column, raw)
            return
        try:
            casted: Any = float(raw)
            if casted.is_integer():
                casted = int(casted)
        except ValueError:
            casted = raw
        self.project.clean.fill_missing(column, casted)

    def _split(self, _: dict[str, Any]) -> None:
        self.project.split.train_test(test_size=0.2)

    def _train(self, params: dict[str, Any]) -> None:
        self.model_name = params["model_name"]
        self.project.model.create(self.model_name)
        self.project.model.train()

    def _evaluate(self, _: dict[str, Any]) -> None:
        task = self.task or self.project.context.get_task_type()
        if task == "classification":
            self.project.evaluate.classification()
        else:
            self.project.evaluate.regression()

    def _plot_confusion_matrix(self, _: dict[str, Any]) -> None:
        _, _, _, y_true = self.project.context.get_split_data()
        y_pred = self.project.context.get_predictions()
        if y_pred is None:
            raise ValueError("Predictions missing for confusion matrix.")
        cm = confusion_matrix(y_true, y_pred)
        fig, ax = plt.subplots()
        ax.imshow(cm)
        ax.set_title("Confusion Matrix")
        self.project.context.set_last_figure(fig)

    def _plot_histogram(self, params: dict[str, Any]) -> None:
        self.project.graph.histogram(params["column"])

    def _plot_scatter(self, params: dict[str, Any]) -> None:
        df = self.project.context.ensure_dataframe()
        x = params["x"]
        y = params["y"]
        if x not in df.columns or y not in df.columns:
            raise ValueError(f"Columns '{x}' and/or '{y}' not found.")
        fig, ax = plt.subplots()
        ax.scatter(df[x], df[y])
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        self.project.context.set_last_figure(fig)

    def _export(self, params: dict[str, Any]) -> None:
        path = params["path"]
        out = self.project._export_by_path(path)
        self.exports.append(str(out))

    def _deploy(self, params: dict[str, Any]) -> None:
        mode = params["mode"]
        output = params["output"]
        deployed = self.project.deploy(mode=mode, output_dir=output)
        self.deployments.append(str(deployed))

    def _set_task(self, params: dict[str, Any]) -> None:
        self.task = params["task"]


class PlanBuilder:
    def build(self, parsed: dict[str, Any], project: Any) -> ExecutionPlan:
        steps: list[PlanStep] = []

        parsed_steps = parsed["steps"]
        source_steps = [s for s in parsed_steps if s.name in {"load_dataset", "load_matrix"}]
        if source_steps:
            steps.extend(source_steps)
        else:
            steps.append(PlanStep("use_existing_data", {}))

        if project.context.get_target() is not None:
            pass
        elif any(s.name == "load_matrix" and s.params.get("last_column_target") for s in source_steps):
            steps.append(PlanStep("set_target_last_column", {}))
        elif any(s.name == "load_dataset" for s in source_steps):
            steps.append(PlanStep("set_target_last_column", {}))

        for step in parsed_steps:
            if step.name.startswith("clean_"):
                steps.append(step)

        model_name = parsed.get("model_name")
        task = parsed.get("task") or project.context.get_task_type()
        if model_name is None:
            model_name = "linear_regression" if task == "regression" else "logistic_regression"

        steps.append(PlanStep("split", {}))
        steps.append(PlanStep("train", {"model_name": model_name}))
        steps.append(PlanStep("evaluate", {}))

        for step in parsed_steps:
            if step.name in {"plot_confusion_matrix", "plot_histogram", "plot_scatter", "export", "deploy", "set_task"}:
                steps.append(step)

        dataset_hash = self._dataset_hash_for_plan(project, source_steps)
        plan_hash = self._plan_hash(dataset_hash, steps)
        return ExecutionPlan(steps=steps, dataset_hash=dataset_hash, plan_hash=plan_hash, model_name=model_name)

    @staticmethod
    def _dataset_hash_for_plan(project: Any, source_steps: list[PlanStep]) -> str:
        if source_steps and source_steps[0].name == "load_matrix":
            df = parse_matrix(source_steps[0].params["matrix_raw"])
            return hash_dataframe(df)
        if project.context.get_dataframe() is not None:
            return hash_dataframe(project.context.ensure_dataframe())
        return hashlib.sha256(b"pending").hexdigest()

    @staticmethod
    def _plan_hash(dataset_hash: str, steps: list[PlanStep]) -> str:
        payload = dataset_hash + "|" + "|".join(
            f"{step.name}:{json.dumps(step.params, sort_keys=True, default=str)}" for step in steps
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
