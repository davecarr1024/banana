from banana.board import Offset, Position


def test_add_offset() -> None:
    assert Offset(1, 2) + Offset(-3, -4) == Offset(-2, -2)


def test_add_position() -> None:
    assert Offset(1, 2) + Position(-3, -4) == Position(-2, -2)


def test_mul() -> None:
    assert Offset(1, 2) * 3 == Offset(3, 6)


def test_neg() -> None:
    assert -Offset(1, 2) == Offset(-1, -2)
