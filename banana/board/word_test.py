import pytest
from pytest_subtests import SubTests

from banana.board import ACROSS, DOWN, Position, Tile, Word


def test_too_short():
    with pytest.raises(Word.ValueError):
        Word([])
    with pytest.raises(Word.ValueError):
        Word([Tile("A", Position(0, 0))])


def test_invalid_direction():
    with pytest.raises(Word.ValueError):
        Word(
            [
                Tile("A", Position(0, 0)),
                Tile("B", Position(-1, 0)),
            ]
        )


def test_non_linear():
    with pytest.raises(Word.ValueError):
        Word(
            [
                Tile("A", Position(0, 0)),
                Tile("B", Position(1, 0)),
                Tile("C", Position(2, 1)),
            ]
        )


def test_direction():
    assert (
        Word(
            [
                Tile("A", Position(0, 0)),
                Tile("B", Position(1, 0)),
            ]
        ).direction
        == ACROSS
    )
    assert (
        Word(
            [
                Tile("A", Position(0, 0)),
                Tile("B", Position(0, 1)),
            ]
        ).direction
        == DOWN
    )


def test_value():
    assert (
        Word(
            [
                Tile("A", Position(0, 0)),
                Tile("B", Position(1, 0)),
            ]
        ).value
        == "AB"
    )


def test_position():
    assert Word(
        [
            Tile("A", Position(0, 0)),
            Tile("B", Position(1, 0)),
        ]
    ).position == Position(0, 0)


def test_eq(subtests: SubTests):
    for lhs, rhs, expected in list[tuple[Word, Word, bool]](
        [
            (
                Word(
                    [
                        Tile("A", Position(0, 0)),
                        Tile("B", Position(1, 0)),
                    ]
                ),
                Word(
                    [
                        Tile("A", Position(0, 0)),
                        Tile("B", Position(1, 0)),
                    ]
                ),
                True,
            ),
            (
                Word(
                    [
                        Tile("A", Position(0, 0)),
                        Tile("B", Position(1, 0)),
                    ]
                ),
                Word(
                    [
                        Tile("A", Position(0, 0)),
                        Tile("C", Position(1, 0)),
                    ]
                ),
                False,
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert (lhs == rhs) == expected
            assert (hash(lhs) == hash(rhs)) == expected


def test_str() -> None:
    word = Word([Tile("A", Position(0, 0)), Tile("B", Position(1, 0))])
    s = str(word)
    assert "AB" in s
    assert str(Position(0, 0)) in s
    assert str(ACROSS) in s


def test_overlaps() -> None:
    assert Word(
        [
            Tile("A", Position(0, 0)),
            Tile("B", Position(1, 0)),
        ]
    ).overlaps(
        Word(
            [
                Tile("A", Position(0, 0)),
                Tile("C", Position(0, 1)),
            ]
        )
    )
    assert not Word(
        [
            Tile("A", Position(0, 0)),
            Tile("B", Position(0, 1)),
        ]
    ).overlaps(
        Word(
            [
                Tile("A", Position(0, 1)),
                Tile("C", Position(1, 1)),
            ]
        )
    )


def test_from_str() -> None:
    assert Word.from_str("AB", Position(0, 0), ACROSS) == Word(
        [
            Tile("A", Position(0, 0)),
            Tile("B", Position(1, 0)),
        ]
    )
