"""Модуль, описывающий константы, используемые в проекте."""

from enum import Enum


class CellColors:
    """Описывает цвета, в которые может быть раскрашена клетка."""
    BLACK = 'grey'
    WHITE = 'white'
    NEUTRAL = 'lightblue'
    BLACK_CONFLICT = '#e60000'
    WHITE_CONFLICT = '#ff8080'


class State(Enum):
    """Описывает состояние клетки:
    BLACK - клетка закрашена,
    WHITE - клетка белая,
    NEUTRAL - клетка в нейтральном состоянии.
    """
    BLACK = CellColors.BLACK
    WHITE = CellColors.WHITE
    NEUTRAL = CellColors.NEUTRAL


# Позиция игрового окна на экране
WINDOW_POS = (450, 100)

# Размер клетки в пикселях
CELL_SIZE = 100

# Ограничение на количество найденных решений головоломки
MAX_SOLUTIONS = 10
