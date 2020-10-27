from .button import Button
from . import const
from queue import Queue
from typing import List, Set


def cell_without_same_numbers(cell: Button, white_nums: Set[int]) -> bool:
    if cell.state == const.State.NEUTRAL:
        return False
    if cell.state == const.State.BLACK:
        return True

    if cell.number in white_nums:
        return False
    else:
        white_nums.add(cell.number)
        return True


def in_field(row: int, col: int) -> bool:
    return 0 <= row < const.BOARD_SIZE[0] and 0 <= col < const.BOARD_SIZE[1]


def shaded_cell_without_common_sides(row: int, col: int,
                                     board: List[List[Button]]):
    if board[row][col].state == const.State.WHITE:
        return True
    delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for d_row, d_col in delta:
        neighbor_row = row + d_row
        neighbor_col = col + d_col
        if not in_field(neighbor_row, neighbor_col):
            continue
        if board[neighbor_row][neighbor_col].state == const.State.BLACK:
            return False
    return True


def bfs(row: int, col: int, board: List[Button], used: List[List[bool]]):
    used[row][col] = True
    queue = Queue()
    queue.put((row, col))
    delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while not queue.empty():
        r, c = queue.get()
        for d_row, d_col in delta:
            neighbor_row = r + d_row
            neighbor_col = c + d_col
            if not in_field(neighbor_row, neighbor_col):
                continue
            if board[neighbor_row][neighbor_col].state == const.State.BLACK:
                continue
            if used[neighbor_row][neighbor_col]:
                continue
            used[neighbor_row][neighbor_col] = True
            queue.put((neighbor_row, neighbor_col))


def is_solved(board: List[List[Button]]):
    # check 1st condition
    for row in range(const.BOARD_SIZE[0]):
        white_nums = set()
        for col in range(const.BOARD_SIZE[1]):
            if not cell_without_same_numbers(board[row][col], white_nums):
                return False

    for col in range(const.BOARD_SIZE[1]):
        white_nums = set()
        for row in range(const.BOARD_SIZE[0]):
            if not cell_without_same_numbers(board[row][col], white_nums):
                return False

    # check 2nd condition
    for row in range(const.BOARD_SIZE[0]):
        for col in range(const.BOARD_SIZE[1]):
            if not shaded_cell_without_common_sides(row, col, board):
                return False

    # check 3rd condition
    flag = False  # Запускался ли bfs
    used = [[False] * const.BOARD_SIZE[1] for i in range(const.BOARD_SIZE[0])]
    for row in range(const.BOARD_SIZE[0]):
        for col in range(const.BOARD_SIZE[1]):
            if board[row][col].state == const.State.BLACK:
                continue
            if not flag:
                bfs(row, col, used, board)
                flag = True
            elif not used[row][col]:
                return False

    return True
