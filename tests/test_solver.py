from hitori.solver import hitori_solver


def test_solve_1(capsys):
    hitori_solver.solve('./resources/levels/1.txt')

    out = capsys.readouterr().out
    assert out == 'B W B W\n' \
                  'W W W W\n' \
                  'W W B W\n' \
                  'W B W W\n'


def test_solve_7(capsys):
    hitori_solver.solve('./resources/levels/7.txt')

    out = capsys.readouterr().out
    assert out == ''
