from .window import Window, Button
from . import const
from queue import Queue
from typing import List, Set


def check_cell(cell: Button, white_nums: Set[int]):
    if cell.state == const.State.NEUTRAL:
        return False
    if cell.state == const.State.BLACK:
        return True

    if cell.number in white_nums:
        return False
    else:
        white_nums.add(cell.number)
        return True


def on_board(row: int, col: int):
    return 0 <= row < const.BOARD_SIZE[0] and 0 <= col < const.BOARD_SIZE[1]


def check_cell2(row: int, col: int, board: List[List[Button]]):
    if board[row][col].state == const.State.WHITE:
        return True
    delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for d_row, d_col in delta:
        neighbor_row = row + d_row
        neighbor_col = col + d_col
        if not on_board(neighbor_row, neighbor_col):
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
        for dr, dc in delta:
            neighbor_r = r + dr
            neighbor_c = c + dc
            if not on_board(neighbor_r, neighbor_c):
                continue
            if board[neighbor_r][neighbor_c].state == const.State.BLACK:
                continue
            if used[neighbor_r][neighbor_c]:
                continue
            used[neighbor_r][neighbor_c] = True
            queue.put((neighbor_r, neighbor_c))


def is_solved(board: List[List[Button]]):
    # check 1st condition
    for row in range(const.BOARD_SIZE[0]):
        white_nums = set()
        for col in range(const.BOARD_SIZE[1]):
            if not check_cell(board[row][col], white_nums):
                return False

    for col in range(const.BOARD_SIZE[1]):
        white_nums = set()
        for row in range(const.BOARD_SIZE[0]):
            if not check_cell(board[row][col], white_nums):
                return False

    # check 2nd condition
    for row in range(const.BOARD_SIZE[0]):
        for col in range(const.BOARD_SIZE[1]):
            if not check_cell2(row, col, board):
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
