from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)
from . import const


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hitori')
        height = const.BOARD_SIZE[0] * const.CELL_SIZE
        weight = const.BOARD_SIZE[1] * const.CELL_SIZE
        self.setGeometry(const.WINDOW_SIZE[0], const.WINDOW_SIZE[1],
                         height, weight)
        numbers = Window.read_field_from_file('numb.txt')
        for row in range(const.BOARD_SIZE[0]):
            for column in range(const.BOARD_SIZE[1]):
                Button(numbers[row][column], (row, column), self)
        self.show()

    @staticmethod
    def read_field_from_file(file_name: str):
        with open(file_name) as f:
            numbers = list(map(lambda x: x.split(), f.readlines()))
        return numbers


class Button(QPushButton):

    def __init__(self, number, pos, *args):
        super().__init__(number, *args)
        self.color = const.Color.BLUE
        self.clicked.connect(self.click)
        self.number = number
        self.setGeometry(pos[0] * const.CELL_SIZE, pos[1] * const.CELL_SIZE,
                         const.CELL_SIZE, const.CELL_SIZE)
        self.setStyleSheet("QPushButton { background-color: %s }"
                           % const.Color.BLUE)

    def click(self):
        if self.color in (const.Color.BLUE, const.Color.GREY):
            self.color = const.Color.WHITE
        else:
            self.color = const.Color.GREY
        self.setStyleSheet("QPushButton { background-color: %s }" % self.color)
