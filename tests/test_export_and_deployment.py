from __future__ import annotations

from zipfile import ZipFile

import pandas as pd

from baya.deployment import export_production_bundle
from baya.project import Project


def _trained_project(tmp_path):
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [0, 0, 0, 1, 1, 1]})
    project = Project(df, target="y", workspace=tmp_path)
    project.split.train_test(test_size=0.33)
    project.model.create("logistic_regression")
    project.model.train()
    project.evaluate.classification()
    return project


def test_pdf_export_generates_valid_header(tmp_path):
    project = _trained_project(tmp_path)
    out = project.export.pdf.to_pdf(str(tmp_path / "report.pdf"))
    assert out.read_bytes().startswith(b"%PDF-")


def test_docx_export_generates_openxml_package(tmp_path):
    project = _trained_project(tmp_path)
    out = project.export.docx.to_docx(str(tmp_path / "report.docx"))

    with ZipFile(out, "r") as archive:
        names = set(archive.namelist())

    assert "[Content_Types].xml" in names
    assert "word/document.xml" in names


def test_production_bundle_writes_fastapi_files(tmp_path):
    project = _trained_project(tmp_path)

    out = export_production_bundle(project.context, str(tmp_path / "bundle"))
    files = {p.name for p in out.iterdir()}

    assert {"model.pkl", "app.py", "requirements.txt", "README.txt"}.issubset(files)
