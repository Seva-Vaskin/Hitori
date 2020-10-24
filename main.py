import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)
from hitori import const


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hitori')
        height = const.BOARD_SIZE[0] * const.CELL_SIZE
        weight = const.BOARD_SIZE[1] * const.CELL_SIZE
        self.setGeometry(const.WINDOW_SIZE[0], const.WINDOW_SIZE[1],
                         height, weight)
        numbers = Window.read_field_from_file('numb.txt')

        positions = [(i, j) for i in range(const.BOARD_SIZE[0])
                     for j in range(const.BOARD_SIZE[1])]

        for pos, number in zip(positions, numbers):
            btn = Button(number, self)
            btn.setGeometry(pos[0] * const.CELL_SIZE, pos[1] * const.CELL_SIZE,
                            const.CELL_SIZE, const.CELL_SIZE)
            btn.setStyleSheet("QPushButton { background-color: %s }"
                              % const.Color.BLUE)
        self.show()

    @staticmethod
    def read_field_from_file(file_name: str):
        with open(file_name) as f:
            numbers = f.read()
            numbers = numbers.split()
        return numbers


class Button(QPushButton):

    def __init__(self, number, *args):
        super().__init__(number, *args)
        self.color = const.Color.BLUE
        self.clicked.connect(self.click)
        self.number = number

    def click(self):
        if self.color in (const.Color.BLUE, const.Color.GREY):
            self.color = const.Color.WHITE
        else:
            self.color = const.Color.GREY
        self.setStyleSheet("QPushButton { background-color: %s }" % self.color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
