"""Модуль, отвечающий за игровое окно."""

from PyQt5.QtWidgets import QWidget
from typing import List

from . import const, driver
from hitori.button import Button


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hitori')
        height = const.BOARD_SIZE[0] * const.CELL_SIZE
        weight = const.BOARD_SIZE[1] * const.CELL_SIZE
        self.setGeometry(const.WINDOW_POS[0], const.WINDOW_POS[1],
                         height, weight)
        numbers = Window.read_field_from_file('numb.txt')
        self.board = [[0] * const.BOARD_SIZE[0] for i in range(
            const.BOARD_SIZE[1])]
        for row in range(const.BOARD_SIZE[0]):
            for column in range(const.BOARD_SIZE[1]):
                self.board[row][column] = Button(numbers[row][column],
                                                 (column, row), self)
                self.board[row][column].clicked.connect(self.button_clicked)
        self.show()

    @staticmethod
    def read_field_from_file(file_name: str) -> List[str]:
        """Читает игровое поле из файла."""
        with open(file_name) as f:
            numbers = list(map(lambda x: x.split(), f.readlines()))
        return numbers

    def button_clicked(self) -> None:
        """Печатает 'Solved', если головоломка решена."""
        if driver.is_solved(self.board):
            print('Solved')
