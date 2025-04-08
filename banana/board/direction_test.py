import pytest
from pytest_subtests import SubTests

from banana.board import ACROSS, DOWN, Direction, Offset, Position


def test_invalid_values():
    with pytest.raises(Direction.ValueError):
        Direction(2, 0)


def test_add():
    assert Position(0, 0) + ACROSS == Position(1, 0)
    assert ACROSS + Position(0, 0) == Position(1, 0)
    assert Position(0, 0) + DOWN == Position(0, 1)
    assert DOWN + Position(0, 0) == Position(0, 1)


def test_sub():
    assert Position(0, 0) - ACROSS == Position(-1, 0)
    assert Position(0, 0) - DOWN == Position(0, -1)


def test_neg():
    assert -ACROSS == Direction(-1, 0)
    assert -DOWN == Direction(0, -1)


def test_orthogonal():
    assert ACROSS.orthogonal() == DOWN
    assert DOWN.orthogonal() == ACROSS


def test_mul() -> None:
    assert ACROSS * 2 == Offset(2, 0)


def test_str(subtests: SubTests) -> None:
    for direction, expected in list[tuple[Direction, str]](
        [
            (ACROSS, "ACROSS"),
            (DOWN, "DOWN"),
            (-ACROSS, "-ACROSS"),
            (-DOWN, "-DOWN"),
        ]
    ):
        with subtests.test(direction=direction, expected=expected):
            assert str(direction) == expected
