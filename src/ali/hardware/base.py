"""Minimal hardware abstraction with a non-actuating dry-run backend."""

from abc import ABC, abstractmethod
from ali.core.models import MotionCommand


class MotorBackend(ABC):
    @abstractmethod
    def send(self, command: MotionCommand) -> None:
        """Send a bounded command to a backend."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the backend."""


class DryRunBackend(MotorBackend):
    """Logs commands in memory; never connects to GPIO, USB, or motors."""

    def __init__(self) -> None:
        self.last_command = MotionCommand.stop()
        self.history: list[MotionCommand] = []

    def send(self, command: MotionCommand) -> None:
        self.last_command = command
        self.history.append(command)

    def stop(self) -> None:
        self.send(MotionCommand.stop())
