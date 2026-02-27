from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Set


class Phase(str, Enum):
    DATA = "data"
    PREPROCESS = "preprocess"
    SPLIT = "split"
    TRAIN = "train"
    PREDICT = "predict"
    EVALUATE = "evaluate"
    EXPORT = "export"
    DEPLOY = "deploy"


@dataclass(frozen=True)
class Node:
    name: str
    phase: Phase
    func: Callable[[object], None]


class DAG:
    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[str, Set[str]] = {}

    def add_node(self, name: str, phase: Phase, func: Callable[[object], None]) -> None:
        if name in self._nodes:
            raise ValueError(f"Node '{name}' already exists.")
        self._nodes[name] = Node(name=name, phase=phase, func=func)
        self._edges.setdefault(name, set())

    def add_dependency(self, node: str, depends_on: str) -> None:
        if node not in self._nodes or depends_on not in self._nodes:
            raise ValueError("Both nodes must be registered before adding dependency.")
        self._edges[node].add(depends_on)

    def get_node(self, name: str) -> Node:
        return self._nodes[name]

    def _detect_cycles(self) -> None:
        visited: Set[str] = set()
        stack: Set[str] = set()

        def visit(name: str) -> None:
            if name in stack:
                raise RuntimeError("Cycle detected in DAG.")
            if name in visited:
                return
            stack.add(name)
            for dep in self._edges.get(name, set()):
                visit(dep)
            stack.remove(name)
            visited.add(name)

        for node_name in sorted(self._nodes):
            visit(node_name)

    def topological_sort(self) -> List[Node]:
        self._detect_cycles()
        visited: Set[str] = set()
        ordered: List[Node] = []

        def visit(name: str) -> None:
            if name in visited:
                return
            for dep in sorted(self._edges.get(name, set())):
                visit(dep)
            visited.add(name)
            ordered.append(self._nodes[name])

        for name in sorted(self._nodes):
            visit(name)
        return ordered
