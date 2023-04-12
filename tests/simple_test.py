import pytest

pytest.mark.parametrize("x", [1, 2, 3])
pytest.mark.parametrize("correct_anser", [1, 4, 9])
def test_simple_example(x: int = 1, correct_anser: int = 1) -> None:
    assert x ** 2 == correct_anser
