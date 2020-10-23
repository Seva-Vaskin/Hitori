import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication)
import enum
from hitori import const


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hitori')
        height = const.BOARD_SIZE[0] * const.CELL_SIZE
        weight = const.BOARD_SIZE[1] * const.CELL_SIZE
        self.setGeometry(const.WINDOW_SIZE[0], const.WINDOW_SIZE[1],
                         height, weight)
        file_name = 'numb.txt'
        with open(file_name) as f:
            numbers = f.read()
            numbers = numbers.split()

        positions = [(i, j) for i in range(const.BOARD_SIZE[0])
                     for j in range(const.BOARD_SIZE[1])]

        for pos, number in zip(positions, numbers):
            btn = MyButton(number, self)
            btn.setGeometry(pos[0] * const.CELL_SIZE, pos[1] * const.CELL_SIZE,
                            const.CELL_SIZE, const.CELL_SIZE)
            btn.setStyleSheet("QPushButton { background-color: %s }"
                              % const.Color.BLUE)
        self.show()


class MyButton(QPushButton):

    def __init__(self, *args):
        super().__init__(*args)
        self.color = const.Color.BLUE
        self.clicked.connect(self.click)

    def click(self):
        if self.color in (const.Color.GREY, const.Color.GREY):
            self.color = const.Color.WHITE
        else:
            self.color = const.Color.GREY
        self.setStyleSheet("QPushButton { background-color: %s }" % self.color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
