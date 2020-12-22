"""Тестовый модуль."""

from hitori import const
from hitori.board import Cell, Board


def test_get_set_item():
    board = Board("./resources/levels/1.txt")
    board[0, 0] = const.State.BLACK
    assert board[0, 0].state == const.State.BLACK
    board[board.size[0] - 1, board.size[1] - 1] = const.State.WHITE
    assert board[board.size[0] - 1, board.size[1] - 1].state == \
           const.State.WHITE
    board[0, 0] = const.State.BLACK
    assert board[0, 0].state == const.State.BLACK
    board[0, 0] = const.State.NEUTRAL
    assert board[0, 0].state == const.State.NEUTRAL


def test_read_numbers_from_file():
    board = Board("./resources/levels/1.txt")
    assert type(board.board) == list
    assert len(board.board) == board.size[0]
    for row in range(board.size[0]):
        assert type(board.board[row]) == list
        assert len(board.board[row]) == board.size[1]
        for col in range(board.size[1]):
            assert type(board.board[row][col]) == Cell


def test_on_board():
    board = Board("./resources/levels/1.txt")
    assert board.on_board(0, 0)
    assert not board.on_board(board.size[0], 0)
    assert not board.on_board(0, board.size[1])
    assert board.on_board(board.size[0] - 1, board.size[1] - 1)


def test_bfs():
    board = Board("./resources/levels/1.txt")
    for row in range(board.size[0]):
        for col in range(board.size[1]):
            board[row, col] = const.State.WHITE
    assert len(board._bfs((0, 0))) == board.size[0] * board.size[1]
    board[0, 1] = const.State.BLACK
    assert len(board._bfs((0, 0))) == board.size[0] * board.size[1] - 1


def test_is_solved():
    board = Board("./resources/levels/3.txt")
    assert not board.is_solved()
    for row in range(board.size[0]):
        for col in range(board.size[1]):
            board[row, col] = const.State.BLACK
    assert not board.is_solved()
    for row in range(board.size[0]):
        for col in range(board.size[1]):
            board[row, col] = const.State.WHITE
    assert not board.is_solved()
    blacks = [(0, 1), (0, 5), (0, 7),
              (1, 3),
              (2, 0), (2, 2), (2, 5),
              (3, 1), (3, 6),
              (4, 3), (4, 5), (4, 7),
              (5, 0), (5, 2), (5, 4),
              (6, 6),
              (7, 1), (7, 4), (7, 7)]
    for row, col in blacks:
        board[row, col] = const.State.BLACK
    assert board.is_solved()
    board[6, 3] = const.State.BLACK
    assert not board.is_solved()


def test_board_to_str():
    board = Board("./resources/levels/3.txt")
    blacks = [(1, 1), (2, 3), (0, 1)]
    whites = [(2, 2), (0, 0)]
    for pos in blacks:
        board[pos] = const.State.BLACK
    for pos in whites:
        board[pos] = const.State.WHITE
    s = str(board)
    rows = s.split('\n')
    for i in range(board.size[0]):
        row = rows[i].split()
        for j in range(board.size[1]):
            if (i, j) in blacks:
                assert row[j] == 'B'
            elif (i, j) in whites:
                assert row[j] == 'W'
            else:
                assert row[j] == 'N'


def test_switch_cell_color():
    board = Board("./resources/levels/3.txt")
    cells = [(1, 1), (2, 3), (0, 1)]
    for pos in cells:
        assert board.switch_cell_color(pos) == const.State.WHITE
        assert board.switch_cell_color(pos) == const.State.BLACK
        assert board.switch_cell_color(pos) == const.State.WHITE
