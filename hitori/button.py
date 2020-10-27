"""Модуль, отвечающий за клетку игрового поля."""

from PyQt5.QtWidgets import QPushButton
from . import const


class Button(QPushButton):
    """Класс кнопки."""

    def __init__(self, number, pos, *args):
        super().__init__(number, *args)
        self.state = const.State.NEUTRAL
        self.clicked.connect(self.click)
        self.number = number
        self.setGeometry(pos[0] * const.CELL_SIZE, pos[1] * const.CELL_SIZE,
                         const.CELL_SIZE, const.CELL_SIZE)
        self.setStyleSheet("QPushButton { background-color: %s }"
                           % self.state.value)

    def click(self) -> None:
        """Меняет цвет кнопки при нажатии на неё."""
        if self.state in (const.State.NEUTRAL, const.State.BLACK):
            self.state = const.State.WHITE
        else:
            self.state = const.State.BLACK
        self.setStyleSheet("QPushButton { background-color: %s }"
                           % self.state.value)
