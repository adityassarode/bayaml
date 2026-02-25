from __future__ import annotations
from typing import Dict, Set


class PipelineVisualizer:
    def adjacency_list(self, dag: Dict[str, Set[str]]) -> str:
        lines = []
        for node, deps in dag.items():
            if not deps:
                lines.append(f"{node}")
            for dep in deps:
                lines.append(f"{dep} -> {node}")
        return "\n".join(lines)