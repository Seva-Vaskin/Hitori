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
        self.setGeometry(pos[1] * const.CELL_SIZE, pos[0] * const.CELL_SIZE,
                         const.CELL_SIZE, const.CELL_SIZE)
        self.change_color(self.board[pos].state.value)

    def click(self) -> None:
        """Вызывает change_color при нажатии на кнопку."""
        new_color = self.board.switch_cell_color(self.pos).value
        self.change_color(new_color)

    def change_color(self, color) -> None:
        """Перекрашивает кнопку в нужный цвет."""
        self.setStyleSheet("QPushButton { background-color: %s }" % color)


class Window(QWidget):
    """Класс игрового окна."""

    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.board = Board(file_name)
        self.setWindowTitle('Hitori')
        height = self.board.size[0] * const.CELL_SIZE
        weight = self.board.size[1] * const.CELL_SIZE
        self.setGeometry(const.WINDOW_POS[0], const.WINDOW_POS[1],
                         height, weight)
        self.highlighted_cells = list()
        self.buttons = [[0] * self.board.size[0] for i in range(
            self.board.size[1])]
        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                self.buttons[row][col] = Button(self.board, (row, col), self)
                self.buttons[row][col].clicked.connect(self.button_clicked)
        self.show()

    def highlight_conflict_cells(self) -> None:
        """Подсвечивает конфликтующие между собой ячейки."""
        for row, col in self.board.errors.conflicts:
            if self.board[row, col].state == const.State.WHITE:
                self.buttons[row][col].change_color(
                    const.CellColors.WHITE_CONFLICT)
            elif self.board[row, col].state == const.State.BLACK:
                self.buttons[row][col].change_color(
                    const.CellColors.BLACK_CONFLICT)
            self.highlighted_cells.append((row, col))

    def undo_highlight_conflict_cells(self) -> None:
        for row, col in self.highlighted_cells:
            color = self.board[row, col].state.value
            self.buttons[row][col].change_color(color)
        self.highlighted_cells.clear()

    def button_clicked(self) -> None:
        """Печатает 'Solved', если головоломка решена."""
        self.undo_highlight_conflict_cells()
        if self.board.is_solved():
            print('Solved')
        else:
            self.highlight_conflict_cells()
