from hitori.solver import hitori_solver


def test_solve_1(capsys):
    hitori_solver.solve('./resources/levels/1.txt')

    out = capsys.readouterr().out
    assert out == 'B W B W\n' \
                  'W W W W\n' \
                  'W W B W\n' \
                  'W B W W\n' \
                  '\n' \
                  'Найдено решений: 1\n'


def test_solve_6(capsys):
    hitori_solver.solve('./resources/levels/6.txt')

    out = capsys.readouterr().out
    assert len(out) == 750


def test_solve_7(capsys):
    hitori_solver.solve('./resources/levels/7.txt')

    out = capsys.readouterr().out
    assert out == 'Нет решений\n'
