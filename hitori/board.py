"""Модуль, реализующий игровую логику."""

from . import const
from queue import Queue
from typing import List, Set, Tuple

Pos = Tuple[int, int]


class Cell:
    """Класс клетки."""

    def __init__(self, state: const.State, number: int) -> None:
        self.state = state
        self.number = number
        self.conflicts = 0


class Board:
    """Класс логического игрового поля."""

    def __init__(self) -> None:
        self.board = list()
        numbers = self.read_numbers_from_file(const.FILE)
        for i in range(const.BOARD_SIZE[0]):
            self.board.append(list())
            for j in range(const.BOARD_SIZE[1]):
                self.board[i].append(Cell(const.State.NEUTRAL, numbers[i][j]))
        self.white_cells = dict()
        self.errors = RuleError()

    def __getitem__(self, pos: Pos) -> Cell:
        """Возвращает клетку по её координатам."""
        return self.board[pos[0]][pos[1]]

    def __setitem__(self, pos: Pos, new_state: const.State) -> None:
        """"Устанавливает в клетку заданное значение;
        Обновляет конфликты на поле.
        """
        if self[pos].state == new_state:
            return
        # отмена конфликтов
        if self[pos].state == const.State.WHITE and self[pos].conflicts != 0:
            self.update_white_errors(pos, -1)
        if self[pos].state == const.State.BLACK and self[pos].conflicts != 0:
            self.update_black_errors(pos, -1)
        # добавление конфликтов
        if new_state == const.State.WHITE:
            self.update_white_errors(pos, 1)
        if new_state == const.State.BLACK:
            self.update_black_errors(pos, 1)
        # Обновление white_cells
        if new_state == const.State.WHITE:
            self.white_cells[pos] = self[pos]
        elif self[pos].state == const.State.WHITE:
            self.white_cells.pop(pos)
        # обновление количества нейтриальных ячеек
        if self[pos].state == const.State.NEUTRAL:
            self.errors.neutral_cells -= 1
        if new_state == const.State.NEUTRAL:
            self.errors.neutral_cells += 1
        self.board[pos[0]][pos[1]].state = new_state

    def update_white_errors(self, pos: Pos, sign: int) -> None:
        """Обновляет конфликты белых ячеек."""
        self.check_row(pos, sign)
        self.check_column(pos, sign)

    def update_black_errors(self, pos: Pos, sign: int) -> None:
        """Обновляет конфликты чёрных ячеек."""
        delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for delta_row, delta_col in delta:
            new_row = pos[0] + delta_row
            new_col = pos[1] + delta_col
            if not Board.on_board(new_row, new_col):
                continue
            if self[new_row, new_col].state != const.State.BLACK:
                continue
            self.change_conflicts((new_row, new_col), sign)
            self.change_conflicts(pos, sign)

    def switch_cell_color(self, pos: Pos) -> const.State:
        """Изменяет цвет клетки."""
        if self[pos].state == const.State.WHITE:
            self[pos] = const.State.BLACK
        else:
            self[pos] = const.State.WHITE
        return self[pos].state

    @staticmethod
    def read_numbers_from_file(file_name: str) -> List[List[int]]:
        """Читает игровое поле из файла."""
        with open(file_name) as f:
            numbers = list(map(lambda x: x.split(), f.readlines()))
        for i in range(const.BOARD_SIZE[0]):
            for j in range(const.BOARD_SIZE[1]):
                numbers[i][j] = int(numbers[i][j])
        return numbers

    @staticmethod
    def on_board(row: int, col: int) -> bool:
        """Проверяет, что клетка находится в пределах игрового поля."""
        is_on_row = 0 <= row < const.BOARD_SIZE[0]
        is_on_col = 0 <= col < const.BOARD_SIZE[1]
        return is_on_row and is_on_col

    @staticmethod
    def cell_without_same_numbers(cell: Cell, white_nums: Set[int]) -> bool:
        """Проверяет, что в каждой строке и столбце
        среди белых клеток нет одинаковых цифр.
        """
        if cell.state == const.State.NEUTRAL:
            return False
        if cell.state == const.State.BLACK:
            return True
        if cell.number in white_nums:
            return False
        else:
            white_nums.add(cell.number)
            return True

    def shaded_cell_without_common_sides(self, row: int, col: int) -> bool:
        """Проверяет, что закрашенные ячейки не имеют общих сторон."""
        if self[row, col].state != const.State.BLACK:
            return True
        delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d_row, d_col in delta:
            neighbor_row = row + d_row
            neighbor_col = col + d_col
            if not Board.on_board(neighbor_row, neighbor_col):
                continue
            if self[neighbor_row, neighbor_col].state == const.State.BLACK:
                return False
        return True

    def bfs(self, pos: Pos) -> Set[Pos]:
        """Реализует поиск в ширину (bfs)."""
        assert self[pos].state == const.State.WHITE
        used = set()
        used.add(pos)
        queue = Queue()
        queue.put(pos)
        delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while not queue.empty():
            r, c = queue.get()
            for d_row, d_col in delta:
                neighbor_row = r + d_row
                neighbor_col = c + d_col
                if not Board.on_board(neighbor_row, neighbor_col):
                    continue
                if self[neighbor_row, neighbor_col].state != const.State.WHITE:
                    continue
                if (neighbor_row, neighbor_col) in used:
                    continue
                used.add((neighbor_row, neighbor_col))
                queue.put((neighbor_row, neighbor_col))
        return used

    def check_row(self, pos: Pos, sign: int) -> None:
        row, col = pos
        for i in range(const.BOARD_SIZE[1]):
            if i == col or self[row, i].number != self[pos].number:
                continue
            if self[row, i].state != const.State.WHITE:
                continue
            if self[row, i].conflicts == 1:
                self.errors.conflicts.add((row, i))
            self.change_conflicts((row, i), sign)
            self.change_conflicts(pos, sign)

    def check_column(self, pos: Pos, sign: int) -> None:
        row, col = pos
        for i in range(const.BOARD_SIZE[0]):
            if i == row or self[i, col].number != self[pos].number:
                continue
            if self[i, col].state != const.State.WHITE:
                continue
            self.change_conflicts((i, col), sign)
            self.change_conflicts(pos, sign)

    def change_conflicts(self, pos: Pos, value: int) -> None:
        """Прибавялет к self[pos].conflicts значение value."""
        if self[pos].conflicts == 0 and self[pos].conflicts + value != 0:
            self.errors.conflicts.add(pos)
        elif self[pos].conflicts != 0 and self[pos].conflicts + value == 0:
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
        if set(self.white_cells) != self.bfs(bfs_start_cell):
            return False
        return True


class RuleError:
    """Класс ошибок."""
    def __int__(self):
        self.conflicts = set()
        self.neutral_cells = const.BOARD_SIZE[0] * const.BOARD_SIZE[1]
