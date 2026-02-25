from __future__ import annotations

from typing import Callable, Dict, List, Set
from dataclasses import dataclass
from enum import Enum


class Phase(str, Enum):
    DATA = "data"
    TRANSFORM = "transform"
    SPLIT = "split"
    TRAIN = "train"
    EVALUATE = "evaluate"
    DEPLOY = "deploy"


@dataclass(frozen=True)
class Node:
    name: str
    phase: Phase
    func: Callable[["Context"], None]  # Forward type to avoid circular import


class DAG:
    """
    Deterministic, cycle-safe execution graph.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[str, Set[str]] = {}

    # =====================================================
    # Node Management
    # =====================================================

    def add_node(self, name: str, phase: Phase, func: Callable[["Context"], None]) -> None:
        if name in self._nodes:
            raise ValueError(f"Node '{name}' already exists.")

        self._nodes[name] = Node(name=name, phase=phase, func=func)
        self._edges.setdefault(name, set())

    def add_dependency(self, node: str, depends_on: str) -> None:
        if node not in self._nodes:
            raise ValueError(f"Node '{node}' not registered.")

        if depends_on not in self._nodes:
            raise ValueError(f"Dependency '{depends_on}' not registered.")

        self._edges[node].add(depends_on)

    # =====================================================
    # Validation
    # =====================================================

    def validate(self) -> None:
        self._detect_cycles()
        self._enforce_single_train()
        self._enforce_single_deploy()
        self._enforce_phase_progression()

    def _detect_cycles(self) -> None:
        visited: Set[str] = set()
        stack: Set[str] = set()

        def visit(n: str) -> None:
            if n in stack:
                raise RuntimeError("Cycle detected in DAG.")

            if n in visited:
                return

            stack.add(n)
            for dep in self._edges.get(n, []):
                visit(dep)
            stack.remove(n)
            visited.add(n)

        for node in sorted(self._nodes):
            visit(node)

    def _enforce_single_train(self) -> None:
        train_nodes = [
            node for node in self._nodes.values()
            if node.phase == Phase.TRAIN
        ]

        if len(train_nodes) != 1:
            raise RuntimeError("Exactly one TRAIN phase node required.")

    def _enforce_single_deploy(self) -> None:
        deploy_nodes = [
            node for node in self._nodes.values()
            if node.phase == Phase.DEPLOY
        ]

        if len(deploy_nodes) > 1:
            raise RuntimeError("Only one DEPLOY node allowed.")

    def _enforce_phase_progression(self) -> None:
        phase_order = [
            Phase.DATA,
            Phase.TRANSFORM,
            Phase.SPLIT,
            Phase.TRAIN,
            Phase.EVALUATE,
            Phase.DEPLOY,
        ]

        phase_index = {phase: i for i, phase in enumerate(phase_order)}

        for node_name, deps in self._edges.items():
            node_phase = self._nodes[node_name].phase

            for dep in deps:
                dep_phase = self._nodes[dep].phase

                if phase_index[dep_phase] > phase_index[node_phase]:
                    raise RuntimeError(
                        f"Invalid phase order: '{dep_phase}' "
                        f"cannot precede '{node_phase}'."
                    )

    # =====================================================
    # Topological Sort
    # =====================================================

    def topological_sort(self) -> List[Node]:
        self.validate()

        visited: Set[str] = set()
        order: List[Node] = []

        def visit(n: str) -> None:
            if n in visited:
                return
            for dep in sorted(self._edges.get(n, [])):
                visit(dep)
            visited.add(n)
            order.append(self._nodes[n])

        for node in sorted(self._nodes):
            visit(node)

        return order