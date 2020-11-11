"""Модуль, отвечающий за игровое окно."""

from PyQt5.QtWidgets import QWidget, QPushButton

import const
from board import Board, Cell


class Button(QPushButton):
    """Класс кнопки."""

    def __init__(self, cell: Cell, pos, *args) -> None:
        super().__init__(str(cell.number), *args)
        self.clicked.connect(self.click)
        self.cell = cell
        self.setGeometry(pos[0] * const.CELL_SIZE, pos[1] * const.CELL_SIZE,
                         const.CELL_SIZE, const.CELL_SIZE)
        self.setStyleSheet("QPushButton { background-color: %s }"
                           % self.cell.state.value)

    def click(self) -> None:
        """Меняет цвет кнопки при нажатии на неё."""
        if self.cell.state in (const.State.NEUTRAL, const.State.BLACK):
            self.cell.state = const.State.WHITE
        else:
            self.cell.state = const.State.BLACK
        self.setStyleSheet("QPushButton { background-color: %s }"
                           % self.cell.state.value)


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
                self.buttons[row][col] = Button(self.board[row, col],
                                                (col, row), self)
                self.buttons[row][col].clicked.connect(self.button_clicked)
        self.show()

    def button_clicked(self) -> None:
        """Печатает 'Solved', если головоломка решена."""
        if self.board.is_solved():
            print('Solved')
