"""Реализация поиска решения головоломки."""

from ..board import Board, Position
from .. import const

from copy import deepcopy
from typing import List


class Solver:
    """Класс, реализующий поиск решения головоломки."""

    @classmethod
    def _change(cls, board: Board, row: int, col: int, state: const.State) -> \
            bool:
        """Пытается изменить состояние клетки (row, col) на state. Если
        получилось, возвращает true, иначе false.
        В случае неудачи не изменяет поле.
        """
        delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        assert board[Position(row, col)].state == const.State.NEUTRAL
        board[Position(row, col)] = state
        if state == const.State.BLACK:
            for delta_row, delta_col in delta:
                new_row = row + delta_row
                new_col = col + delta_col
                if not board.on_board(new_row, new_col):
                    continue
                if board[Position(new_row, new_col)].state == \
                        const.State.BLACK:
                    board[Position(row, col)] = const.State.NEUTRAL
                    return False
                if board[Position(new_row, new_col)].state == \
                        const.State.NEUTRAL:
                    if not cls._change(board, new_row, new_col,
                                       const.State.WHITE):
                        board[Position(row, col)] = const.State.NEUTRAL
                        return False
        else:
            for delta_row, delta_col in delta:
                new_row = row
                new_col = col
                while board.on_board(new_row + delta_row, new_col + delta_col):
                    new_row += delta_row
                    new_col += delta_col
                    if board[Position(new_row, new_col)].number != board[
                         Position(row, col)].number:
                        continue
                    if board[Position(new_row, new_col)].state == \
                            const.State.WHITE:
                        board[Position(row, col)] = const.State.NEUTRAL
                        return False
                    elif board[Position(new_row, new_col)].state == \
                            const.State.NEUTRAL:
                        if not cls._change(board, new_row, new_col,
                                           const.State.BLACK):
                            board[Position(row, col)] = const.State.NEUTRAL
                            return False
        return True

    @classmethod
    def _recursion(cls, board: Board, cell_id: int = 0,
                   max_solutions: int = const.MAX_SOLUTIONS) -> List[Board]:
        """Реализует рекурсивный перебор состояний доски для поиска решений.
        Возвращает количество найденных решений.
        """
        if max_solutions == 0:
            return list()

        row = cell_id // board.size[1]
        col = cell_id % board.size[1]

        if not board.on_board(row, col):
            if board.is_solved():
                return [board]
            return list()

        solutions = list()

        if board[Position(row, col)].state != const.State.NEUTRAL:
            solutions.extend(
                Solver._recursion(board, cell_id + 1, max_solutions))
        else:
            b1 = deepcopy(board)
            if cls._change(b1, row, col, const.State.WHITE):
                solutions.extend(
                    cls._recursion(b1, cell_id + 1, max_solutions))
            b2 = deepcopy(board)
            if cls._change(b2, row, col, const.State.BLACK):
                solutions.extend(cls._recursion(
                    b2, cell_id + 1, max_solutions - len(solutions)))

        return solutions

    @classmethod
    def solve(cls, board: Board) -> List[Board]:
        """Находит решение(-я) головоломки."""
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                board[Position(row, col)] = const.State.NEUTRAL
        solutions = cls._recursion(board)
        return solutions
