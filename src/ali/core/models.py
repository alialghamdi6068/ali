"""Hardware-independent robot state and movement models."""

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, order=True, slots=True)
class Cell:
    x: int
    y: int


class RobotMode(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    MOVING = "moving"
    PAUSED = "paused"
    FAULT = "fault"


@dataclass(frozen=True, slots=True)
class MotionCommand:
    """Normalized command. Values are bounded to [-1, 1]."""

    linear: float = 0.0
    angular: float = 0.0

    def __post_init__(self) -> None:
        if not -1.0 <= self.linear <= 1.0:
            raise ValueError("linear command must be in [-1, 1].")
        if not -1.0 <= self.angular <= 1.0:
            raise ValueError("angular command must be in [-1, 1].")

    @classmethod
    def stop(cls) -> "MotionCommand":
        return cls(0.0, 0.0)
