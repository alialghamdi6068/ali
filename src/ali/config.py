"""Small, validated configuration model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    width: int = 20
    height: int = 14
    cell_px: int = 36
    tick_ms: int = 140

    def __post_init__(self) -> None:
        if self.width < 3 or self.height < 3:
            raise ValueError("The world must be at least 3x3 cells.")
        if not 12 <= self.cell_px <= 100:
            raise ValueError("cell_px must be between 12 and 100.")
        if not 20 <= self.tick_ms <= 2000:
            raise ValueError("tick_ms must be between 20 and 2000.")
