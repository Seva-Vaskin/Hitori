"""Модуль, описывающий константы, используемые в проекте."""

from enum import Enum


class CellColors:
    BLACK = 'grey'
    WHITE = 'white'
    NEUTRAL = 'lightblue'
    BLACK_CONFLICT = 'darkred'
    WHITE_CONFLICT = 'lightred'


class State(Enum):
    """Описывает состояние клетки:
    EMPTY - клетка в нейтральном состоянии,
    BLACK - клетка закрашена,
    WHITE - клетка белая.
    """
    BLACK = CellColors.BLACK
    WHITE = CellColors.WHITE
    NEUTRAL = CellColors.NEUTRAL


WINDOW_POS = (450, 100)
# Размеры поля в клетках (высота, ширина)
BOARD_SIZE = (8, 8)

# Размер клетки в пикселях
CELL_SIZE = 100

FILE = "../resources/levels/numb.txt"
