"""Модуль, отвечающий за игровое окно."""

from PyQt5.QtWidgets import QWidget, QPushButton

from hitori import const
from hitori.board import Board


class Button(QPushButton):
    """Класс кнопки."""

    def __init__(self, board: Board, pos, *args) -> None:
        super().__init__(str(board[pos].number), *args)
        self.clicked.connect(self.click)
        self.pos = pos
        self.board = board
        self.setGeometry(pos[0] * const.CELL_SIZE, pos[1] * const.CELL_SIZE,
                         const.CELL_SIZE, const.CELL_SIZE)
        self.change_color(self.cell.state.value)
        self.highlighted_cells = list()

    def click(self) -> None:
        """Меняет цвет кнопки при нажатии на неё."""
        new_color = self.board.switch_cell_color(self.pos)
        self.change_color(new_color)

    def change_color(self, color):
        self.setStyleSheet("QPushButton { background-color: %s }" % color)


class Window(QWidget):
    """Класс игрового окна."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Hitori')
        height = const.BOARD_SIZE[0] * const.CELL_SIZE
        weight = const.BOARD_SIZE[1] * const.CELL_SIZE
        self.setGeometry(const.WINDOW_POS[0], const.WINDOW_POS[1],
                         height, weight)
        self.board = Board()
        self.buttons = [[0] * const.BOARD_SIZE[0] for i in range(
            const.BOARD_SIZE[1])]
        for row in range(const.BOARD_SIZE[0]):
            for col in range(const.BOARD_SIZE[1]):
                self.buttons[row][col] = Button(self.board, (col, row), self)
                self.buttons[row][col].clicked.connect(self.button_clicked)
        self.show()

    def highlight_conflict_cells(self):
        for row, col in self.board.errors.conflicts:
            if self.board[row, col].state == const.State.WHITE:
                self.buttons[row][col].change_color(
                    const.CellColors.WHITE_CONFLICT)
            elif self.board[row, col].state == const.State.BLACK:
                self.buttons[row][col].change_color(
                    const.CellColors.BLACK_CONFLICT)

    def button_clicked(self) -> None:
        """Печатает 'Solved', если головоломка решена."""
        for row, col in self.highlighted_cells:
            color = self.board[row, col].state.value
            self.buttons[row][col].change_color(color)

        if self.board.is_solved():
            print('Solved')
        else:
            self.highlight_conflict_cells()
