import sys
from PyQt5.QtWidgets import QApplication
from hitori import window
import argparse
from hitori.solver import hitori_solver


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--solve', help='Решает головоломку и выводит '
                                              'решение на экран',
                        action='store_true')
    parser.add_argument('level', help='Номер уровня [1-7]',
                        choices=[x for x in range(1, 8)], type=int)

    return parser.parse_args()


def run_solver(file_name: str) -> None:
    hitori_solver.solve(file_name)


def run_gui(file_name: str) -> None:
    app = QApplication(sys.argv)
    field = window.Window(file_name)
    field.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    args = parse_args()
    file_name = "./resources/levels/%d.txt" % args.level
    if args.solve:
        run_solver(file_name)
    else:
        run_gui(file_name)
