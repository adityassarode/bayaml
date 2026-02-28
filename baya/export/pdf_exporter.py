from __future__ import annotations

from pathlib import Path

from ..context import Context


class PDFExporter:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    @staticmethod
    def _escape(text: str) -> str:
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def to_pdf(self, path: str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        metrics = self._ctx.get_metrics()
        lines = ["Baya Report", ""]
        if metrics:
            for key, value in metrics.items():
                lines.append(f"{key}: {value}")
        else:
            lines.append("No metrics available.")

        text_ops = ["BT", "/F1 12 Tf", "50 790 Td", "14 TL"]
        for idx, line in enumerate(lines):
            escaped = self._escape(str(line))
            if idx == 0:
                text_ops.append(f"({escaped}) Tj")
            else:
                text_ops.append(f"T* ({escaped}) Tj")
        text_ops.append("ET")
        stream = "\n".join(text_ops).encode("latin-1")

        objects: list[bytes] = []
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        objects.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        )
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")

        chunks = [b"%PDF-1.4\n"]
        offsets = [0]
        for index, body in enumerate(objects, start=1):
            offsets.append(sum(len(c) for c in chunks))
            chunks.append(f"{index} 0 obj\n".encode("ascii") + body + b"\nendobj\n")

        xref_offset = sum(len(c) for c in chunks)
        xref_lines = [f"xref\n0 {len(objects) + 1}\n", "0000000000 65535 f \n"]
        for off in offsets[1:]:
            xref_lines.append(f"{off:010d} 00000 n \n")

        trailer = (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            "startxref\n"
            f"{xref_offset}\n"
            "%%EOF\n"
        )

        pdf_bytes = b"".join(chunks) + "".join(xref_lines).encode("ascii") + trailer.encode("ascii")
        out.write_bytes(pdf_bytes)
        return out
