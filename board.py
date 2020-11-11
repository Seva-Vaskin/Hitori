"""Модуль, реализующий игровую логику."""

import const
from queue import Queue
from typing import List, Set, Tuple


class Cell:
    """Класс клетки."""

    def __init__(self, state: const.State, number: int) -> None:
        self.state = state
        self.number = number

    def cell_without_same_numbers(self, white_nums: Set[int]) -> bool:
        """Проверяет, что в каждой строке и столбце
        среди белых клеток нет одинаковых цифр.
        """
        if self.state == const.State.NEUTRAL:
            return False
        if self.state == const.State.BLACK:
            return True
        if self.number in white_nums:
            return False
        else:
            white_nums.add(self.number)
            return True


class Board:
    """Класс логического игрового поля."""

    def __init__(self) -> None:
        self.board = list()
        numbers = self.read_numbers_from_file(const.FILE)
        for i in range(const.BOARD_SIZE[0]):
            self.board.append(list())
            for j in range(const.BOARD_SIZE[1]):
                self.board[i].append(Cell(const.State.NEUTRAL, numbers[i][j]))

    def __getitem__(self, pos: Tuple[int, int]) -> Cell:
        """Возвращает клетку по её координатам."""
        return self.board[pos[0]][pos[1]]

    def __setitem__(self, pos: Tuple[int, int], state: const.State) -> None:
        """"Устанавливает в клетку заданное значение."""
        self.board[pos[0]][pos[1]].state = state

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

    def bfs(self, row: int, col: int, used: List[List[bool]]) -> None:
        """Реализует поиск в ширину (bfs)."""
        assert self[row, col].state == const.State.WHITE
        used[row][col] = True
        queue = Queue()
        queue.put((row, col))
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
                if used[neighbor_row][neighbor_col]:
                    continue
                used[neighbor_row][neighbor_col] = True
                queue.put((neighbor_row, neighbor_col))

    def is_solved(self) -> bool:
        """Проверяет, решена ли головоломка."""
        # check 1st condition
        for row in range(const.BOARD_SIZE[0]):
            white_nums = set()
            for col in range(const.BOARD_SIZE[1]):
                if not self[row, col].cell_without_same_numbers(white_nums):
                    return False

        for col in range(const.BOARD_SIZE[1]):
            white_nums = set()
            for row in range(const.BOARD_SIZE[0]):
                if not self[row, col].cell_without_same_numbers(white_nums):
                    return False

        # check 2nd condition
        for row in range(const.BOARD_SIZE[0]):
            for col in range(const.BOARD_SIZE[1]):
                if not self.shaded_cell_without_common_sides(row, col):
                    return False

        # check 3rd condition
        flag = False  # Запускался ли bfs
        used = [[False] * const.BOARD_SIZE[1] for i in range(
            const.BOARD_SIZE[0])]
        for row in range(const.BOARD_SIZE[0]):
            for col in range(const.BOARD_SIZE[1]):
                if self[row, col].state != const.State.WHITE:
                    continue
                if not flag:
                    self.bfs(row, col, used)
                    flag = True
                elif not used[row][col]:
                    return False

        return True
