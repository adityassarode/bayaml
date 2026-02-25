from __future__ import annotations

from typing import Callable, Dict, List, Set


class DAG:
    def __init__(self) -> None:
        self._nodes: Dict[str, Callable] = {}
        self._edges: Dict[str, Set[str]] = {}

    def add_node(self, name: str, func: Callable) -> None:
        self._nodes[name] = func
        self._edges.setdefault(name, set())

    def add_dependency(self, node: str, depends_on: str) -> None:
        self._edges.setdefault(node, set()).add(depends_on)

    def topological_sort(self) -> List[str]:
        visited: Set[str] = set()
        order: List[str] = []

        def visit(n: str) -> None:
            if n in visited:
                return
            for dep in self._edges.get(n, []):
                visit(dep)
            visited.add(n)
            order.append(n)

        for node in self._nodes:
            visit(node)

        return order

    def get_callable(self, name: str) -> Callable:
        return self._nodes[name]