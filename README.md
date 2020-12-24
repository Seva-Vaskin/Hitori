# Hitori

Версия: 0.1.0

Автор: Дюндина Мария (mary.diundina@gmail.com)

## Описание

Данное приложение является реализацией головоломки "Хитори".

## Правила игры

Игровое поле сетка n на n (3 < n < 10), в каждой ячейке которой лежит одно число
от 1 до n. Нужно закрасить некоторые из них по определенным правилам:

* в каждой строке и столбце среди незакрашенных клеток не должно быть одинаковых
  цифр;
* закрашенные ячейки не могут иметь общих сторон;
* незакрашенные ячейки должны формировать связную систему
  (то есть с каждой из них можно дойти до любой другой, двигаясь по вертикали
  или горизонтали).

## Требования

* Python версии не ниже 3.8.5
* PyQt5 версии не ниже 5.15.1

## Подробности реализации

* Графическая версия: если в процессе решения головоломки пользователь совершает
  ошибку, то конфликтующие между собой ячейки подсветятся автоматически. Если
  головоломна решена верно, в консоль будет выведено "Solved".
* Консольная версия: алгоритм выводит в консоль решение головоломки в следующем
  формате: матрица n на n, заполненная буквами. W - белый цвет клетки, B -
  чёрный цвет клетки.

## Состав

* Файл запуска программы: `__main__.py`
* Модули: `solver/`, `hitori/`
* Цифры в клетках игрового поля: `resources/levels/`
* Тесты: `test_hitori.py`, `test_solver.py`

## Запуск

* python -m hitori [1-7] — сыграть в уровень с указанным номером.
* python -m hitori -s [1-7] — решить уровень с указанным номером.

## Управление

* ЛКМ — закрасить клетку в белый цвет.
* Повторное нажатие закрасит клетку в чёрный цвет.