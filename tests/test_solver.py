"""Тестовый модуль файла hitori_solver.py."""

from hitori.solver.hitori_solver import Solver
from hitori.board import Board, Position
from hitori import const


def test_solve_1():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    solver = Solver()
    solutions = solver.solve(board)
    assert len(solutions) == 1
    black_cells = [Position(0, 0),
                   Position(0, 2),
                   Position(2, 2),
                   Position(3, 1)]
    for row in range(board.size[0]):
        for col in range(board.size[1]):
            if Position(row, col) in black_cells:
                assert solutions[0][
                           Position(row, col)].state == const.State.BLACK
            else:
                assert solutions[0][
                           Position(row, col)].state == const.State.WHITE


def test_solve_6():
    numbers = [[1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 1],
               [3, 4, 5, 6, 1, 2],
               [4, 5, 6, 1, 2, 3],
               [5, 6, 1, 6, 3, 4],
               [6, 1, 2, 3, 4, 5]]
    board = Board(numbers)
    solver = Solver()
    solutions = solver.solve(board)
    for solution in solutions:
        assert solution.is_solved()


def test_solve_7():
    numbers = [[1, 7, 1, 6, 1, 8, 1, 2],
               [2, 2, 1, 3, 5, 4, 7, 8],
               [4, 3, 7, 8, 1, 3, 2, 6],
               [3, 8, 6, 2, 4, 2, 1, 2],
               [6, 3, 2, 4, 7, 3, 8, 5],
               [4, 4, 7, 7, 8, 6, 2, 1],
               [5, 1, 8, 7, 2, 3, 6, 1],
               [2, 2, 7, 1, 1, 5, 4, 1]]
    board = Board(numbers)
    solver = Solver()
    solutions = solver.solve(board)
    assert not solutions
