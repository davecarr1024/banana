import pytest

from banana.reasoning.constraints import Contains


def test_invalid_letters() -> None:
    with pytest.raises(Contains.ValueError):
        Contains([])


def test_filter() -> None:
    assert list(Contains(["a"]).filter(["abc", "def"])) == ["ABC"]
    assert list(Contains(["a", "b"]).filter(["abc", "adef", "bdef", "def"])) == ["ABC"]


def test_repr() -> None:
    assert repr(Contains(["a"])) == "Contains(frozenset({'A'}))"
