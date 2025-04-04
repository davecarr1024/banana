import pytest

from banana.board import ACROSS, DOWN, Position, Word


@pytest.mark.parametrize(
    "value",
    [
        "a",
        "1",
    ],
)
def test_invalid_value(value: str) -> None:
    with pytest.raises(Word.ValueError):
        Word(value, Position(0, 0), ACROSS)


def test_len() -> None:
    assert len(Word("ABC", Position(0, 0), ACROSS)) == 3


def test_iter() -> None:
    assert list(Word("ABC", Position(0, 0), ACROSS)) == [
        (Position(0, 0), "A"),
        (Position(1, 0), "B"),
        (Position(2, 0), "C"),
    ]
    assert list(Word("ABC", Position(0, 0), DOWN)) == [
        (Position(0, 0), "A"),
        (Position(0, 1), "B"),
        (Position(0, 2), "C"),
    ]


def test_overlaps() -> None:
    assert Word("CAR", Position(0, 0), ACROSS).overlaps(
        Word("CAT", Position(0, 0), DOWN)
    )
    assert not Word("CAR", Position(0, 0), ACROSS).overlaps(
        Word("CAT", Position(0, 2), ACROSS)
    )
