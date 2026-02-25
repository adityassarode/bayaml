from baya.reproducibility.config_freeze import freeze_config


def test_config_hash_deterministic() -> None:
    config = {"a": 1, "b": 2}

    frozen1 = freeze_config(config)
    frozen2 = freeze_config(config)

    assert frozen1["config_hash"] == frozen2["config_hash"]