from ..board import Board
from .. import const

from copy import deepcopy


def change(board: Board, row: int, col: int, state: const.State) -> bool:
    """Пытается изменить состояние клетки (row, col) на state. Если
    получилось возращает true, иначе false.
    !!! В случае неудачи не изменяет поле.
    """
    delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    assert board[row, col].state == const.State.NEUTRAL
    board[row, col] = state
    if state == const.State.BLACK:
        for delta_row, delta_col in delta:
            new_row = row + delta_row
            new_col = col + delta_col
            if not Board.on_board(new_row, new_col):
                continue
            if board[new_row, new_col].state == const.State.BLACK:
                board[row, col] = const.State.NEUTRAL
                return False
            if board[new_row, new_col].state == const.State.NEUTRAL:
                if not change(board, new_row, new_col, const.State.WHITE):
                    board[row, col] = const.State.NEUTRAL
                    return False
    else:
        for delta_row, delta_col in delta:
            new_row = row + delta_row
            new_col = col + delta_col
            while Board.on_board(new_row, new_col):
                if board[new_row, new_col].number != board[row, col].number:
                    continue
                if board[new_row, new_col].state == const.State.WHITE:
                    board[row, col] = const.State.NEUTRAL
                    return False
                elif board[new_row, new_col].state == const.State.NEUTRAL:
                    if not change(board, new_row, new_col, const.State.BLACK):
                        board[row, col] = const.State.NEUTRAL
                        return False
    return True


def rec(board: Board, cell_id: int) -> None:
    """???"""
    if cell_id == const.BOARD_SIZE[0] * const.BOARD_SIZE[1]:
        if board.is_solved():
            print("нашли решение")
            # TODO
    row = cell_id // const.BOARD_SIZE[1]
    col = cell_id % const.BOARD_SIZE[0]
    if board[row, col].state != const.State.NEUTRAL:
        rec(board, cell_id + 1)
    else:
        # TODO Избавиться от копирования, реализовать откат ходов
        b1 = deepcopy(board)
        if change(b1, row, col, const.State.WHITE):
            rec(b1, cell_id + 1)
        b2 = deepcopy(board)
        if change(b2, row, col, const.State.BLACK):
            rec(b2, cell_id + 1)
