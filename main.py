import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication)
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
            btn = QPushButton(number, self)
            btn.setGeometry(pos[0] * const.CELL_SIZE, pos[1] * const.CELL_SIZE,
                            const.CELL_SIZE, const.CELL_SIZE)
            btn.setStyleSheet("QPushButton { background-color: grey }"
                              "QPushButton:pressed { background-color: red }"
                              "QPushButton")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
