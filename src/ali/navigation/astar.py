"""A* shortest-path planner with octile heuristic."""

from heapq import heappop, heappush
from itertools import count
from math import hypot, sqrt

from ali.core.models import Cell
from ali.navigation.grid import GridWorld


def _heuristic(a: Cell, b: Cell) -> float:
    dx, dy = abs(a.x - b.x), abs(a.y - b.y)
    return (dx + dy) + (sqrt(2) - 2) * min(dx, dy)


def plan_path(world: GridWorld, start: Cell, goal: Cell) -> list[Cell]:
    """Return a path including start and goal, or [] when no path exists."""
    if not world.is_free(start) or not world.is_free(goal):
        return []
    if start == goal:
        return [start]

    sequence = count()
    frontier: list[tuple[float, int, Cell]] = []
    heappush(frontier, (_heuristic(start, goal), next(sequence), start))
    came_from: dict[Cell, Cell] = {}
    cost: dict[Cell, float] = {start: 0.0}

    while frontier:
        _, _, current = heappop(frontier)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))

        for neighbor in world.neighbors(current):
            step = hypot(neighbor.x - current.x, neighbor.y - current.y)
            candidate = cost[current] + step
            if candidate >= cost.get(neighbor, float("inf")):
                continue
            came_from[neighbor] = current
            cost[neighbor] = candidate
            priority = candidate + _heuristic(neighbor, goal)
            heappush(frontier, (priority, next(sequence), neighbor))
    return []
