from banana.board import ACROSS, Board, Position, Word
from banana.reasoning.constraints import Start


def test_create_candidates() -> None:
    assert list(Start().create_candidates(Board([]), "abc")) == [
        Word.from_str(
            "abc",
            Position(0, 0),
            ACROSS,
        )
    ]


def test_repr() -> None:
    assert repr(Start()) == "Start()"
