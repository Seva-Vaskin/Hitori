"""Модуль, реализующий игровую логику."""

from hitori import const
from queue import Queue
from typing import Set
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Position:
    row: int
    col: int

    def __hash__(self):
        return hash((self.row, self.col))


class Cell:
    """Класс клетки."""

    def __init__(self, state: const.State, number: int) -> None:
        self.state = state
        self.number = number
        self.conflicts = 0


class Board:
    """Класс логического игрового поля."""

    def __init__(self, numbers) -> None:
        self.board = list()
        self.size = (0, 0)
        self._read_numbers(numbers)
        self.white_cells = dict()
        self.errors = RuleError(self)

    @classmethod
    def from_file(cls, file_name: Path):
        """Читает игровое поле из файла."""
        with file_name.open() as f:
            numbers = [[int(item) for item in row.split()] for row in
                       f.readlines()]
        return cls(numbers)

    def _read_numbers(self, numbers) -> None:
        self.size = (len(numbers), len(numbers[0]))
        for i in range(self.size[0]):
            self.board.append(list())
            for j in range(self.size[1]):
                self.board[i].append(Cell(const.State.NEUTRAL, numbers[i][j]))

    def __getitem__(self, pos: Position) -> Cell:
        """Возвращает клетку по её координатам."""
        return self.board[pos.row][pos.col]

    def __setitem__(self, pos: Position, new_state: const.State) -> None:
        """Устанавливает в клетку заданное значение;
        Обновляет конфликты на поле.
        """
        if self[pos].state == new_state:
            return
        # отмена конфликтов
        if self[pos].state == const.State.WHITE:
            self._update_white_errors(pos, -1)
        if self[pos].state == const.State.BLACK:
            self._update_black_errors(pos, -1)
        # добавление конфликтов
        if new_state == const.State.WHITE:
            self._update_white_errors(pos, 1)
        if new_state == const.State.BLACK:
            self._update_black_errors(pos, 1)
        # Обновление white_cells
        if new_state == const.State.WHITE:
            self.white_cells[pos] = self[pos]
        elif self[pos].state == const.State.WHITE:
            self.white_cells.pop(pos)
        # обновление количества нейтральных ячеек
        if self[pos].state == const.State.NEUTRAL:
            self.errors.neutral_cells -= 1
        if new_state == const.State.NEUTRAL:
            self.errors.neutral_cells += 1
        self.board[pos.row][pos.col].state = new_state

    def __str__(self) -> str:
        """Формирует строку, содержащую информацию о состояниях ячеек."""
        ans = []
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self[Position(row, col)].state == const.State.NEUTRAL:
                    ans.append('N')
                elif self[Position(row, col)].state == const.State.BLACK:
                    ans.append('B')
                elif self[Position(row, col)].state == const.State.WHITE:
                    ans.append('W')
                if col != self.size[1] - 1:
                    ans.append(' ')
            if row != self.size[0] - 1:
                ans.append('\n')

        return ''.join(ans)

    def _update_white_errors(self, pos: Position, sign: int) -> None:
        """Обновляет конфликты белых ячеек."""
        self._update_white_errors_row(pos, sign)
        self._update_white_errors_column(pos, sign)

    def _update_black_errors(self, pos: Position, sign: int) -> None:
        """Обновляет конфликты чёрных ячеек."""
        delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for delta_row, delta_col in delta:
            new_row = pos.row + delta_row
            new_col = pos.col + delta_col
            if not self.on_board(new_row, new_col):
                continue
            if self[Position(new_row, new_col)].state != const.State.BLACK:
                continue
            self.change_conflicts(Position(new_row, new_col), sign)
            self.change_conflicts(pos, sign)

    def switch_cell_color(self, pos: Position) -> const.State:
        """Изменяет состояние клетки:
        с нейтрального на белый, с белого на чёрный, с чёрного на белый.
        Возвращает новое состояние.
        """
        if self[pos].state == const.State.WHITE:
            self[pos] = const.State.BLACK
        else:
            self[pos] = const.State.WHITE
        return self[pos].state

    def on_board(self, row: int, col: int) -> bool:
        """Проверяет, что клетка находится в пределах игрового поля."""
        is_on_row = 0 <= row < self.size[0]
        is_on_col = 0 <= col < self.size[1]
        return is_on_row and is_on_col

    def _bfs(self, pos: Position) -> Set[Position]:
        """Реализует поиск в ширину (bfs)."""
        assert self[pos].state == const.State.WHITE
        used = set()
        used.add(pos)
        queue = Queue()
        queue.put(pos)
        delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while not queue.empty():
            pos = queue.get()
            for delta_row, delta_col in delta:
                new_row = pos.row + delta_row
                new_col = pos.col + delta_col
                if not self.on_board(new_row, new_col):
                    continue
                if self[Position(new_row, new_col)].state != \
                        const.State.WHITE:
                    continue
                if Position(new_row, new_col) in used:
                    continue
                used.add(Position(new_row, new_col))
                queue.put(Position(new_row, new_col))
        return used

    def _update_white_errors_row(self, pos: Position, sign: int) -> None:
        """Перебирает элементы строки, обновляет конфликты белых ячеек."""
        row, col = pos.row, pos.col
        for i in range(self.size[1]):
            if i == col or self[Position(row, i)].number != self[pos].number:
                continue
            if self[Position(row, i)].state != const.State.WHITE:
                continue
            self.change_conflicts(Position(row, i), sign)
            self.change_conflicts(pos, sign)

    def _update_white_errors_column(self, pos: Position, sign: int) -> None:
        """Перебирает элементы столбца, обновляет конфликты белых ячеек."""
        row, col = pos.row, pos.col
        for i in range(self.size[0]):
            if i == row or self[Position(i, col)].number != self[pos].number:
                continue
            if self[Position(i, col)].state != const.State.WHITE:
                continue
            self.change_conflicts(Position(i, col), sign)
            self.change_conflicts(pos, sign)

    def change_conflicts(self, pos: Position, value: int) -> None:
        """Увеличивает счётчик конфликтов ячейки с координатами pos
        на значение value.
        """
        if not self[pos].conflicts and self[pos].conflicts + value:
            self.errors.conflicts.add(pos)
        elif self[pos].conflicts and not self[pos].conflicts + value:
            self.errors.conflicts.remove(pos)
        self[pos].conflicts += value

    def is_solved(self) -> bool:
        """Проверяет, решена ли головоломка."""
        # Проверка наличия серых клеток или конфликтов по белым или чёрным
        # ячейкам
        if self.errors.conflicts or self.errors.neutral_cells:
            return False
        # Проверка связности графа
        bfs_start_cell = list(self.white_cells.keys())[0]
        return set(self.white_cells) == self._bfs(bfs_start_cell)


class RuleError:
    """Класс ошибок."""

    def __init__(self, board: Board) -> None:
        self.conflicts = set()
        self.neutral_cells = board.size[0] * board.size[1]
