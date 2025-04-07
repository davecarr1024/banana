from banana.board import Board
from banana.reasoning import Constraint


def test_filter() -> None:
    assert Constraint().filter(["abc", "def"]) == ["abc", "def"]


def test_create_candidates() -> None:
    assert list(Constraint().create_candidates(Board([]), "abc")) == []
