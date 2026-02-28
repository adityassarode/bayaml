from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Optional, Union

import pandas as pd

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
from .export import (
    CSVExporter,
    DOCXExporter,
    ExcelExporter,
    GraphExporter,
    ImageExporter,
    JSONExporter,
    PDFExporter,
    ONNXExporter,
)
from .hooks import HookManager
from .integrations import bootstrap_integrations
from .logging import create_logger
from .orchestration import Pipeline
from .tracking import Tracker

ConfigInput = Union[ConfigSchema, Mapping[str, Any], str, Path]


class Project:
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
            Path(workspace).resolve() if workspace else Path.cwd() / "baya_runs"
        )
        workspace_path.mkdir(parents=True, exist_ok=True)

        self.context = Context(workspace=workspace_path, seed=seed)
        self.logger = create_logger("baya")

        self.data = DataModule(self.context)
        self.clean = CleanModule(self.context)
        self.encode = EncodeModule(self.context)
        self.scale = ScaleModule(self.context)
        self.split = SplitModule(self.context)
        self.model = ModelModule(self.context)
        self.evaluate = EvaluateModule(self.context)
        self.transform = TransformModule(self.context)

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

    @property
    def dataframe(self) -> Optional[pd.DataFrame]:
        return self.context.get_dataframe()

    @property
    def target(self) -> Optional[str]:
        return self.context.get_target()
