from ali.core.models import Cell
from ali.navigation.astar import plan_path
from ali.navigation.grid import GridWorld


def test_path_includes_start_and_goal():
    world = GridWorld(8, 8)
    start, goal = Cell(0, 0), Cell(7, 7)
    path = plan_path(world, start, goal)
    assert path[0] == start
    assert path[-1] == goal
    assert len(path) == 8


def test_obstacle_forces_detour():
    world = GridWorld(5, 5, {Cell(2, 2)})
    path = plan_path(world, Cell(1, 2), Cell(3, 2))
    assert path
    assert Cell(2, 2) not in path


def test_no_path_when_goal_blocked():
    world = GridWorld(5, 5, {Cell(4, 4)})
    assert plan_path(world, Cell(0, 0), Cell(4, 4)) == []


def test_diagonal_corner_cutting_is_blocked():
    world = GridWorld(3, 3, {Cell(1, 0), Cell(0, 1)})
    assert plan_path(world, Cell(0, 0), Cell(1, 1)) == []


def test_start_equals_goal():
    cell = Cell(2, 2)
    assert plan_path(GridWorld(5, 5), cell, cell) == [cell]
