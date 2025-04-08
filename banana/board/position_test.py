from banana.board import ACROSS, Offset, Position


def test_add_direction() -> None:
    assert Position(1, 1) + ACROSS == Position(2, 1)


def test_add_offset() -> None:
    assert Position(1, 2) + Offset(3, 4) == Position(4, 6)


def test_sub_direction() -> None:
    assert Position(1, 1) - ACROSS == Position(0, 1)


def test_sub_offset() -> None:
    assert Position(1, 2) - Offset(3, 4) == Position(-2, -2)
