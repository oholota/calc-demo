"""Unit tests: the calculation logic alone, no server, run in milliseconds."""
import pytest

from calculator.engine import MAX_LENGTH, CalcError, evaluate


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2+3", 5),
        ("2+3*4", 14),
        ("(2+3)*4", 20),
        ("10-4-3", 3),
        ("-5+2", -3),
        ("7/2", 3.5),
        ("8/4", 2),
        ("0.1+0.2", 0.3),
        (" 6 * 7 ", 42),
    ],
)
def test_arithmetic(expression, expected):
    assert evaluate(expression) == expected


def test_whole_results_are_integers():
    assert isinstance(evaluate("8/4"), int)


def test_division_by_zero():
    with pytest.raises(CalcError, match="Division by zero"):
        evaluate("1/0")


@pytest.mark.parametrize("expression", ["", "   ", "2+", "2**8", "abs(-1)", "x+1", "1;2"])
def test_rejects_invalid_input(expression):
    with pytest.raises(CalcError):
        evaluate(expression)


def test_rejects_code_injection():
    # This is why the engine does not use eval().
    with pytest.raises(CalcError):
        evaluate("__import__('os').system('echo hacked')")


def test_rejects_too_long_input():
    with pytest.raises(CalcError, match="longer"):
        evaluate("1+" * MAX_LENGTH + "1")


def test_overflow_is_an_error_not_a_crash():
    with pytest.raises(CalcError, match="too large"):
        evaluate("1e308*10")
