"""Command limiter and stop-on-fault behavior."""

from ali.core.models import MotionCommand


class CommandLimiter:
    def __init__(self, max_linear: float = 0.25, max_angular: float = 0.3):
        if not 0 < max_linear <= 1 or not 0 < max_angular <= 1:
            raise ValueError("Command limits must be in (0, 1].")
        self.max_linear = max_linear
        self.max_angular = max_angular

    def apply(self, command: MotionCommand, *, emergency_stop: bool = False) -> MotionCommand:
        if emergency_stop:
            return MotionCommand.stop()
        return MotionCommand(
            linear=max(-self.max_linear, min(self.max_linear, command.linear)),
            angular=max(-self.max_angular, min(self.max_angular, command.angular)),
        )
