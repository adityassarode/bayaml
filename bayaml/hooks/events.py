from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    BEFORE_STEP = "before_step"
    AFTER_STEP = "after_step"
    BEFORE_TRAIN = "before_train"
    AFTER_TRAIN = "after_train"
