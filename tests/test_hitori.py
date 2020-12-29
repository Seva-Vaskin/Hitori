"""Тестовый модуль файла board.py."""

from hitori import const
from hitori.board import Cell, Board, Position


def test_get_set_item():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    board[Position(0, 0)] = const.State.BLACK
    assert board[Position(0, 0)].state == const.State.BLACK
    board[Position(board.size[0] - 1, board.size[1] - 1)] = const.State.WHITE
    assert board[Position(board.size[0] - 1, board.size[1] - 1)].state == \
           const.State.WHITE
    board[Position(0, 0)] = const.State.BLACK
    assert board[Position(0, 0)].state == const.State.BLACK
    board[Position(0, 0)] = const.State.NEUTRAL
    assert board[Position(0, 0)].state == const.State.NEUTRAL


def test_read_numbers_from_file():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    assert type(board.board) == list
    assert len(board.board) == board.size[0]
    for row in range(board.size[0]):
        assert type(board.board[row]) == list
        assert len(board.board[row]) == board.size[1]
        for col in range(board.size[1]):
            assert type(board.board[row][col]) == Cell


def test_on_board():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    assert board.on_board(0, 0)
    assert not board.on_board(board.size[0], 0)
    assert not board.on_board(0, board.size[1])
    assert board.on_board(board.size[0] - 1, board.size[1] - 1)


def test_bfs():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    for row in range(board.size[0]):
        for col in range(board.size[1]):
            board[Position(row, col)] = const.State.WHITE
    assert len(board._bfs(Position(0, 0))) == board.size[0] * board.size[1]
    board[Position(0, 1)] = const.State.BLACK
    assert len(board._bfs(Position(0, 0))) == board.size[0] * board.size[1] - 1


def test_is_solved():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    assert not board.is_solved()
    for row in range(board.size[0]):
        for col in range(board.size[1]):
            board[Position(row, col)] = const.State.BLACK
    assert not board.is_solved()
    for row in range(board.size[0]):
        for col in range(board.size[1]):
            board[Position(row, col)] = const.State.WHITE
    assert not board.is_solved()
    black_cells = [Position(0, 0),
                   Position(0, 2),
                   Position(2, 2),
                   Position(3, 1)]
    for pos in black_cells:
        board[pos] = const.State.BLACK
    assert board.is_solved()
    board[Position(1, 1)] = const.State.BLACK
    assert not board.is_solved()


def test_board_to_str():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    blacks = [Position(1, 1), Position(2, 3), Position(0, 1)]
    whites = [Position(2, 2), Position(0, 0)]
    for pos in blacks:
        board[pos] = const.State.BLACK
    for pos in whites:
        board[pos] = const.State.WHITE
    s = str(board)
    rows = s.split('\n')
    for i in range(board.size[0]):
        row = rows[i].split()
        for j in range(board.size[1]):
            if Position(i, j) in blacks:
                assert row[j] == 'B'
            elif Position(i, j) in whites:
                assert row[j] == 'W'
            else:
                assert row[j] == 'N'


def test_switch_cell_color():
    numbers = [[2, 2, 2, 4],
               [1, 4, 2, 3],
               [2, 3, 2, 1],
               [3, 4, 1, 2]]
    board = Board(numbers)
    cells = [Position(1, 1), Position(2, 3), Position(0, 1)]
    for pos in cells:
        assert board.switch_cell_color(pos) == const.State.WHITE
        assert board.switch_cell_color(pos) == const.State.BLACK
        assert board.switch_cell_color(pos) == const.State.WHITE
