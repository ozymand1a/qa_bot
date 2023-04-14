import pytest


pytest.mark.parametrize("x", [1, 2, 3])
pytest.mark.parametrize("correct_anser", [1, 4, 9])


def test_simple_example(number: int = 1, correct_answer: int = 1) -> None:
    assert number ** 2 == correct_answer
