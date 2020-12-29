import sys
from PyQt5.QtWidgets import QApplication
from hitori import window
import argparse
from hitori.solver.hitori_solver import Solver
from hitori.board import Board

from pathlib import Path

LEVEL_ERROR = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--solve', help='Решает головоломку и выводит '
                                              'решение на экран',
                        action='store_true')
    parser.add_argument('level', help='Номер уровня [1-7]',
                        choices=[x for x in range(1, 8)], type=int)

    return parser.parse_args()


def run_solver(file_name: Path) -> None:
    solver = Solver()
    board = Board.from_file(file_name)
    solutions = solver.solve(board)
    if not solutions:
        print("Нет решений.")
    else:
        print("Найдено решений: %d" % len(solutions))
        for solution in solutions:
            print(solution)
            print()


def run_gui(file_name: Path) -> None:
    app = QApplication(sys.argv)
    board = Board.from_file(file_name)
    field = window.Window(board)
    field.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    args = parse_args()
    file_name = Path.cwd() / 'resources' / 'levels' / ('%d.txt' % args.level)
    if not file_name.exists() or not file_name.is_file():
        print("Уровень не найден", file=sys.stderr)
        sys.exit(LEVEL_ERROR)
    if args.solve:
        run_solver(file_name)
    else:
        run_gui(file_name)
