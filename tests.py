import const
from board import Cell, Board


def test_cell_without_same_numbers():
    full_set = set(range(10))
    neutral_cell = Cell(const.State.NEUTRAL, 0)
    black_cell = Cell(const.State.BLACK, 1)
    white_cell = Cell(const.State.WHITE, 2)
    assert not neutral_cell.cell_without_same_numbers(full_set)
    assert black_cell.cell_without_same_numbers(full_set)
    assert not white_cell.cell_without_same_numbers(full_set)
    white_nums = set()
    for i in range(10):
        cell = Cell(const.State.WHITE, i)
        assert cell.cell_without_same_numbers(white_nums)
    for i in range(10):
        cell = Cell(const.State.WHITE, i)
        assert not cell.cell_without_same_numbers(white_nums)


def test_get_set_item():
    board = Board()
    board[0, 0] = const.State.BLACK
    assert board[0, 0].state == const.State.BLACK
    board[const.BOARD_SIZE[0] - 1, const.BOARD_SIZE[1] - 1] = const.State.WHITE
    assert board[const.BOARD_SIZE[0] - 1, const.BOARD_SIZE[1] - 1].state == \
           const.State.WHITE


def test_read_numbers_from_file():
    numbers = Board.read_numbers_from_file(const.FILE)
    assert type(numbers) == list
    assert len(numbers) == const.BOARD_SIZE[0]
    for row in range(const.BOARD_SIZE[0]):
        assert type(numbers[row]) == list
        assert len(numbers[row]) == const.BOARD_SIZE[1]
        for col in range(const.BOARD_SIZE[1]):
            assert type(numbers[row][col]) == int


def test_on_board():
    assert Board.on_board(0, 0)
    assert not Board.on_board(const.BOARD_SIZE[0], 0)
    assert not Board.on_board(0, const.BOARD_SIZE[1])
    assert Board.on_board(const.BOARD_SIZE[0] - 1, const.BOARD_SIZE[1] - 1)


def test_shaded_cell_without_common_sides():
    board = Board()
    assert board.shaded_cell_without_common_sides(0, 0)
    board[0, 0] = const.State.BLACK
    assert board.shaded_cell_without_common_sides(0, 0)
    board[0, 1] = const.State.BLACK
    assert not board.shaded_cell_without_common_sides(0, 0)
    assert not board.shaded_cell_without_common_sides(0, 1)


def test_bfs():
    board = Board()
    used = [[False] * const.BOARD_SIZE[1] for i in range(const.BOARD_SIZE[0])]
    board[0, 0] = const.State.WHITE
    board[0, 1] = const.State.WHITE
    board[1, 1] = const.State.WHITE
    board[2, 0] = const.State.WHITE
    board.bfs(0, 0, used)
    for row in range(const.BOARD_SIZE[0]):
        for col in range(const.BOARD_SIZE[1]):
            if (row, col) in ((0, 0), (0, 1), (1, 1)):
                assert used[row][col]
            else:
                assert not used[row][col]


def test_is_solved():
    board = Board()
    assert not board.is_solved()
    for row in range(const.BOARD_SIZE[0]):
        for col in range(const.BOARD_SIZE[1]):
            board[row, col] = const.State.BLACK
    assert not board.is_solved()
    for row in range(const.BOARD_SIZE[0]):
        for col in range(const.BOARD_SIZE[1]):
            board[row, col] = const.State.WHITE
    assert not board.is_solved()
    numbers = [[7, 7, 4, 8, 5, 8, 3, 3],
               [2, 3, 6, 4, 7, 4, 1, 8],
               [6, 6, 4, 4, 3, 2, 2, 1],
               [6, 2, 7, 5, 1, 2, 3, 3],
               [5, 2, 1, 4, 4, 5, 6, 8],
               [7, 7, 7, 2, 4, 8, 4, 6],
               [1, 8, 2, 7, 6, 5, 4, 4],
               [3, 3, 5, 6, 6, 7, 8, 4]]
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
