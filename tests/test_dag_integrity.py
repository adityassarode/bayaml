from baya.orchestration.dag import DAG, Phase
import pytest


def test_cycle_detection() -> None:
    dag = DAG()

    dag.add_node("a", Phase.DATA, lambda ctx: None)
    dag.add_node("b", Phase.TRAIN, lambda ctx: None)

    dag.add_dependency("a", "b")
    dag.add_dependency("b", "a")

    with pytest.raises(RuntimeError):
        dag.topological_sort()


def test_single_train_enforced() -> None:
    dag = DAG()

    dag.add_node("a", Phase.TRAIN, lambda ctx: None)
    dag.add_node("b", Phase.TRAIN, lambda ctx: None)

    with pytest.raises(RuntimeError):
        dag.topological_sort()