import pytest

from banana.reasoning.constraints import Contains


def test_invalid_letters() -> None:
    with pytest.raises(Contains.ValueError):
        Contains([])


def test_filter() -> None:
    assert list(Contains(["A"]).filter(["ABC", "DEF"])) == ["ABC"]
    assert list(Contains(["A", "B"]).filter(["ABC", "ADEF", "BDEF", "DEF"])) == ["ABC"]
