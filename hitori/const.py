"""Модуль, описывающий константы, используемые в проекте."""

from enum import Enum


class State(Enum):
    """Описывает состояние клетки:
    EMPTY - клетка в нейтральном состоянии,
    BLACK - клетка закрашена,
    WHITE - клетка белая.
    """
    BLACK = 'grey'
    WHITE = 'white'
    NEUTRAL = 'lightblue'


WINDOW_SIZE = (450, 100)
# Размеры поля в клетках (высота, ширина)
BOARD_SIZE = (8, 8)

# Размер клетки в пикселях
CELL_SIZE = 100
