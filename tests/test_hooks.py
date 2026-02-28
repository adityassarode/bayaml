from baya.hooks import EventType, HookManager


def test_hooks_emit():
    events = []
    HookManager.register(EventType.BEFORE_STEP, lambda payload: events.append(payload["step"]))
    HookManager.emit(EventType.BEFORE_STEP, {"step": "a"})
    assert events == ["a"]
