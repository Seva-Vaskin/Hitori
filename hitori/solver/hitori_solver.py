from ..board import Board
from .. import const

from copy import deepcopy


def _change(board: Board, row: int, col: int, state: const.State) -> bool:
    """Пытается изменить состояние клетки (row, col) на state. Если
    получилось, возвращает true, иначе false.
    В случае неудачи не изменяет поле.
    """
    delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    assert board[row, col].state == const.State.NEUTRAL
    board[row, col] = state
    if state == const.State.BLACK:
        for delta_row, delta_col in delta:
            new_row = row + delta_row
            new_col = col + delta_col
            if not board.on_board(new_row, new_col):
                continue
            if board[new_row, new_col].state == const.State.BLACK:
                board[row, col] = const.State.NEUTRAL
                return False
            if board[new_row, new_col].state == const.State.NEUTRAL:
                if not _change(board, new_row, new_col, const.State.WHITE):
                    board[row, col] = const.State.NEUTRAL
                    return False
    else:
        for delta_row, delta_col in delta:
            new_row = row
            new_col = col
            while board.on_board(new_row + delta_row, new_col + delta_col):
                new_row += delta_row
                new_col += delta_col
                if board[new_row, new_col].number != board[row, col].number:
                    continue
                if board[new_row, new_col].state == const.State.WHITE:
                    board[row, col] = const.State.NEUTRAL
                    return False
                elif board[new_row, new_col].state == const.State.NEUTRAL:
                    if not _change(board, new_row, new_col, const.State.BLACK):
                        board[row, col] = const.State.NEUTRAL
                        return False
    return True


def _recursion(board: Board, cell_id: int = 0,
               max_solutions: int = const.MAX_SOLUTIONS) -> int:
    """Реализует рекурсивный перебор состояний доски для поиска решений.
    Возвращает количество найденных решений.
    """
    if max_solutions == 0:
        return 0

    row = cell_id // board.size[1]
    col = cell_id % board.size[1]

    if not board.on_board(row, col):
        if board.is_solved():
            print(board)
            print()
            return 1
        return 0

    solutions = 0

    if board[row, col].state != const.State.NEUTRAL:
        solutions += _recursion(board, cell_id + 1, max_solutions)
    else:
        b1 = deepcopy(board)
        if _change(b1, row, col, const.State.WHITE):
            solutions += _recursion(b1, cell_id + 1, max_solutions)
        b2 = deepcopy(board)
        if _change(b2, row, col, const.State.BLACK):
            solutions += _recursion(b2, cell_id + 1, max_solutions - solutions)

    return solutions


def solve(file_name: str) -> None:
    """Находит решение(-я) головоломки."""
    board = Board(file_name)
    solutions = _recursion(board)
    if solutions == 0:
        print("Нет решений.")
    else:
        print("Найдено решений: %d" % solutions)
