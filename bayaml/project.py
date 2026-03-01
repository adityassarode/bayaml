from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Optional, Union

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, r2_score

from .automation import ExecutionEngine, ExecutionPlan, IntentParser, PlanBuilder, PlanValidator
from .config import ConfigSchema, load_config, validate_config
from .context import Context
from .core import (
    CleanModule,
    DataModule,
    EncodeModule,
    EvaluateModule,
    ModelModule,
    ScaleModule,
    SplitModule,
    TransformModule,
)
from .deployment import export_production_bundle
from .export import (
    CSVExporter,
    DOCXExporter,
    ExcelExporter,
    GraphExporter,
    ImageExporter,
    JSONExporter,
    ONNXExporter,
    PDFExporter,
)
from .hooks import HookManager
from .integrations import bootstrap_integrations
from .logging import create_logger
from .orchestration import Pipeline
from .tracking import Tracker
from .visualization.graph_manager import GraphManager

ConfigInput = Union[ConfigSchema, Mapping[str, Any], str, Path]


class Project:
    """
    Main orchestration class for Bayaml.

    Handles data loading, model training, evaluation,
    Auto Mode execution, deployment, and tracking.
    """
    def __init__(
        self,
        data: Optional[Union[str, Path, pd.DataFrame]] = None,
        *,
        target: Optional[str] = None,
        workspace: Optional[Union[str, Path]] = None,
        seed: int = 42,
    ) -> None:
        bootstrap_integrations()

        workspace_path = (
            Path(workspace).resolve() if workspace else Path.cwd() / "bayaml"
        )
        workspace_path.mkdir(parents=True, exist_ok=True)

        self.context = Context(workspace=workspace_path, seed=seed)
        self.logger = create_logger("bayaml")

        self.data = DataModule(self.context)
        self.clean = CleanModule(self.context)
        self.encode = EncodeModule(self.context)
        self.scale = ScaleModule(self.context)
        self.split = SplitModule(self.context)
        self.model = ModelModule(self.context)
        self.evaluate = EvaluateModule(self.context)
        self.transform = TransformModule(self.context)
        self.graph = GraphManager(self.context)

        self.pipeline = Pipeline(self.context)
        self.hooks = HookManager
        self.tracker = Tracker(workspace_path / "tracking")

        self.export = type(
            "ExportFacade",
            (),
            {
                "csv": CSVExporter(self.context),
                "json": JSONExporter(self.context),
                "excel": ExcelExporter(self.context),
                "pdf": PDFExporter(self.context),
                "docx": DOCXExporter(self.context),
                "onnx": ONNXExporter(self.context),
                "image": ImageExporter(),
                "graph": GraphExporter(self.context),
            },
        )()

        if data is not None:
            self.data.load(data)
        if target is not None and self.context.get_dataframe() is not None:
            self.context.set_target(target)

    @staticmethod
    def _coerce_config(cfg: ConfigInput) -> ConfigSchema:
        if isinstance(cfg, ConfigSchema):
            return cfg

        if isinstance(cfg, (str, Path)):
            path = Path(cfg)
            loaded = load_config(path)
            return validate_config(loaded)

        if isinstance(cfg, Mapping):
            return validate_config(dict(cfg))

        raise TypeError(
            "cfg must be ConfigSchema, mapping, or path to JSON/YAML config file."
        )

    @classmethod
    def from_config(cls, cfg: ConfigInput) -> "Project":
        resolved = cls._coerce_config(cfg)
        project = cls(data=resolved.data_path, target=resolved.target, seed=resolved.seed)
        project.split.train_test(test_size=resolved.test_size)
        project.model.create(resolved.model)
        return project

    def run(self) -> dict[str, float]:
        self.model.train()
        self.model.predict()

        task = self.context.get_task_type()
        metrics = (
            self.evaluate.classification()
            if task == "classification"
            else self.evaluate.regression()
        )

        self.tracker.log_metrics(metrics)
        self.tracker.finalize()
        return metrics

    def _export_by_path(self, path: str | Path) -> Path:
        out = Path(path)
        suffix = out.suffix.lower()
        if suffix == ".csv":
            return self.export.csv.to_csv(str(out))
        if suffix == ".json":
            return self.export.json.to_json(str(out))
        if suffix == ".xlsx":
            return self.export.excel.to_excel(str(out))
        if suffix == ".pdf":
            return self.export.pdf.to_pdf(str(out))
        if suffix == ".docx":
            return self.export.docx.to_docx(str(out))
        if suffix == ".onnx":
            return self.export.onnx.to_onnx(str(out))
        raise ValueError(f"Unsupported export format: {suffix}")

    def auto(
        self,
        instruction: str,
        preview: bool = False,
        auto_confirm: bool = True,
        mode: str = "safe",
    ) -> ExecutionPlan | dict[str, Any]:
        if mode not in {"safe", "fast", "teach", "production"}:
            raise ValueError("mode must be one of: safe, fast, teach, production")

        parser = IntentParser()
        parsed = parser.parse(instruction)
        plan = PlanBuilder().build(parsed, self)

        if preview:
            return plan
        if not auto_confirm:
            return {"plan": plan, "status": "confirmation_required"}

        PlanValidator().validate(plan)
        result = ExecutionEngine(self).execute(plan)

        if mode == "production":
            result["guardian"] = self.guardian()
            result["stability"] = self.stability()

        return result

    def deploy(self, mode: str = "rest", output_dir: str = "deployment_bundle") -> Path:
        if mode == "rest":
            return export_production_bundle(self.context, output_dir)
        if mode == "onnx":
            out = Path(output_dir)
            if out.suffix.lower() != ".onnx":
                out = out / "model.onnx"
            return self.export.onnx.to_onnx(str(out))
        raise ValueError("mode must be 'rest' or 'onnx'")

    def guardian(self) -> dict[str, Any]:
        df = self.context.ensure_dataframe()
        target = self.context.ensure_target()
        warnings: list[str] = []

        metrics: dict[str, float] = {}
        numeric = df.select_dtypes(include="number")

        if target in numeric.columns:
            corr = numeric.drop(columns=[target], errors="ignore").corrwith(numeric[target]).abs()
            max_corr = float(corr.max()) if not corr.empty else 0.0
            metrics["max_feature_target_corr"] = max_corr
            if max_corr > 0.95:
                warnings.append("Leakage risk: feature-target correlation above 0.95")

        if self.context.get_task_type() == "classification":
            imbalance = float(df[target].value_counts(normalize=True).max())
            metrics["max_class_ratio"] = imbalance
            if imbalance > 0.8:
                warnings.append("Imbalance risk: majority class ratio above 0.8")

        if self.context.is_fitted and self.context.is_split:
            model = self.context.get_model()
            X_train, X_test, y_train, y_test = self.context.get_split_data()
            if model is not None:
                train_pred = model.predict(X_train)
                test_pred = model.predict(X_test)
                if self.context.get_task_type() == "classification":
                    train_score = float(accuracy_score(y_train, train_pred))
                    test_score = float(accuracy_score(y_test, test_pred))
                else:
                    train_score = float(r2_score(y_train, train_pred))
                    test_score = float(r2_score(y_test, test_pred))
                metrics["train_score"] = train_score
                metrics["test_score"] = test_score
                metrics["overfit_gap"] = train_score - test_score
                if train_score - test_score > 0.1:
                    warnings.append("Overfitting risk: train/test gap above 0.1")

        feature_corr = numeric.drop(columns=[target], errors="ignore").corr().abs() if not numeric.empty else pd.DataFrame()
        max_pair_corr = 0.0
        if not feature_corr.empty:
            mask = np.triu(np.ones(feature_corr.shape), k=1).astype(bool)
            upper = feature_corr.where(mask).stack()
            max_pair_corr = float(upper.max()) if not upper.empty else 0.0
            if max_pair_corr > 0.9:
                warnings.append("Multicollinearity risk: pair correlation above 0.9")
        metrics["max_pair_corr"] = max_pair_corr

        samples, features = df.shape
        ratio = float(samples / max(1, features - 1))
        metrics["sample_feature_ratio"] = ratio
        if ratio < 5:
            warnings.append("Low sample-to-feature ratio (<5)")

        risk_level = "low"
        if len(warnings) >= 3:
            risk_level = "high"
        elif warnings:
            risk_level = "medium"

        return {"risk_level": risk_level, "warnings": warnings, "metrics": metrics}

    def stability(self, n_runs: int = 5) -> dict[str, float]:
        if self.context.get_dataframe() is None:
            raise RuntimeError("Load data before stability analysis.")
        if self.context.get_target() is None:
            raise RuntimeError("Set target before stability analysis.")

        model = self.context.get_model()
        if model is None:
            raise RuntimeError("Create and train a model before stability analysis.")

        model_map = {
            "LogisticRegression": "logistic_regression",
            "LinearRegression": "linear_regression",
            "RandomForestClassifier": "random_forest_classifier",
            "RandomForestRegressor": "random_forest_regressor",
        }
        model_name = model_map.get(type(model).__name__)
        if model_name is None:
            raise RuntimeError("Stability supports built-in sklearn models only.")

        base_seed = self.context.get_seed()
        task = self.context.get_task_type() or "classification"
        key = "accuracy" if task == "classification" else "r2"
        df = self.context.ensure_dataframe().copy()
        target = self.context.ensure_target()

        scores: list[float] = []
        for i in range(n_runs):
            probe = Project(df, target=target, seed=base_seed + i, workspace=self.context.get_workspace())
            probe.split.train_test(test_size=0.2)
            probe.model.create(model_name)
            probe.model.train()
            metrics = probe.evaluate.classification() if task == "classification" else probe.evaluate.regression()
            scores.append(float(metrics[key]))

        mean_metric = float(np.mean(scores))
        std_metric = float(np.std(scores))
        stability_score = 1.0 - (std_metric / (mean_metric + 1e-6))
        stability_score = float(max(0.0, min(1.0, stability_score)))

        return {
            "mean_metric": mean_metric,
            "std_metric": std_metric,
            "stability_score": stability_score,
        }

    @property
    def dataframe(self) -> Optional[pd.DataFrame]:
        return self.context.get_dataframe()

    @property
    def target(self) -> Optional[str]:
        return self.context.get_target()
