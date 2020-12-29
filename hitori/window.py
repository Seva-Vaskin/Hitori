"""Модуль, отвечающий за игровое окно."""

from PyQt5.QtWidgets import QWidget, QPushButton

from hitori import const
from hitori.board import Board, Position


class Button(QPushButton):
    """Класс кнопки."""

    def __init__(self, board: Board, pos: Position, *args) -> None:
        super().__init__(str(board[pos].number), *args)
        self.clicked.connect(self.click)
        self.pos = pos
        self.board = board
        self.setGeometry(pos.col * const.CELL_SIZE, pos.row * const.CELL_SIZE,
                         const.CELL_SIZE, const.CELL_SIZE)
        self.change_color(self.board[pos].state.value)

    def click(self) -> None:
        """Вызывает change_color при нажатии на кнопку.
        Меняет цвет логической кнопки.
        """
        new_color = self.board.switch_cell_color(self.pos).value
        self.change_color(new_color)

    def change_color(self, color: str) -> None:
        """Перекрашивает кнопку в нужный цвет."""
        self.setStyleSheet("QPushButton { background-color: %s }" % color)


class Window(QWidget):
    """Класс игрового окна."""

    def __init__(self, board: Board) -> None:
        super().__init__()
        self.board = board
        self.setWindowTitle('Hitori')
        height = self.board.size[0] * const.CELL_SIZE
        weight = self.board.size[1] * const.CELL_SIZE
        self.setGeometry(const.WINDOW_POS[0], const.WINDOW_POS[1],
                         height, weight)
        self.highlighted_cells = list()
        self.buttons = [[Button(self.board, Position(row, col), self) for col in
                         range(self.board.size[1])]
                        for row in range(self.board.size[0])]
        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                self.buttons[row][col].clicked.connect(self.button_clicked)

    def highlight_conflict_cells(self) -> None:
        """Подсвечивает конфликтующие между собой ячейки."""
        for pos in self.board.errors.conflicts:
            if self.board[pos].state == const.State.WHITE:
                self.buttons[pos.row][pos.col].change_color(
                    const.CellColors.WHITE_CONFLICT)
            elif self.board[pos].state == const.State.BLACK:
                self.buttons[pos.row][pos.col].change_color(
                    const.CellColors.BLACK_CONFLICT)
            self.highlighted_cells.append(pos)

    def undo_highlight_conflict_cells(self) -> None:
        """Отменяет подсветку конфликтующих ячеек."""
        for pos in self.highlighted_cells:
            color = self.board[pos].state.value
            self.buttons[pos.row][pos.col].change_color(color)
        self.highlighted_cells.clear()

    def button_clicked(self) -> None:
        """Печатает 'Solved', если головоломка решена.
        Иначе вызывает подсветку конфликтующих ячеек.
        """
        self.undo_highlight_conflict_cells()
        if self.board.is_solved():
            print('Solved')
        else:
            self.highlight_conflict_cells()
