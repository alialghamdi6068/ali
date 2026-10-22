"""Grid world model used by the simulator and planner."""

from ali.core.models import Cell


class GridWorld:
    def __init__(self, width: int, height: int, obstacles: set[Cell] | None = None):
        if width < 1 or height < 1:
            raise ValueError("Grid dimensions must be positive.")
        self.width = width
        self.height = height
        self.obstacles = set(obstacles or ())

    def contains(self, cell: Cell) -> bool:
        return 0 <= cell.x < self.width and 0 <= cell.y < self.height

    def is_free(self, cell: Cell) -> bool:
        return self.contains(cell) and cell not in self.obstacles

    def set_obstacle(self, cell: Cell, blocked: bool) -> None:
        if not self.contains(cell):
            raise ValueError("Obstacle must be inside the world.")
        if blocked:
            self.obstacles.add(cell)
        else:
            self.obstacles.discard(cell)

    def neighbors(self, cell: Cell) -> list[Cell]:
        result: list[Cell] = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)):
            nxt = Cell(cell.x + dx, cell.y + dy)
            if not self.is_free(nxt):
                continue
            # Prevent diagonal movement through the corner of an obstacle.
            if dx and dy:
                if not self.is_free(Cell(cell.x + dx, cell.y)):
                    continue
                if not self.is_free(Cell(cell.x, cell.y + dy)):
                    continue
            result.append(nxt)
        return result
