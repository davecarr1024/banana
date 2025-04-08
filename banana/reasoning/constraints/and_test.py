from typing import Iterable, override

from pytest_subtests import SubTests

from banana.board import Board, Position, Tile, Word
from banana.reasoning.constraint import Constraint
from banana.reasoning.constraints.and_ import And


class MockFilterConstraint(Constraint):
    def __init__(self, suffix: str):
        self.suffix = suffix

    @override
    def __repr__(self) -> str:
        return f"MockFilterConstraint({self.suffix})"

    def filter(self, words: Iterable[str]) -> Iterable[str]:
        return (w for w in words if w.endswith(self.suffix))


class MockCandidateConstraint(Constraint):
    def __init__(self, label: str):
        self.label = label

    @override
    def __repr__(self) -> str:
        return f"MockCandidateConstraint({self.label})"

    def create_candidates(self, board: Board, word: str) -> Iterable[Word]:
        return (
            [Word([Tile(letter, Position(i, 0)) for i, letter in enumerate(word)])]
            if word.startswith(self.label)
            else []
        )


def test_len_iter() -> None:
    constraints = [MockFilterConstraint("A"), MockFilterConstraint("B")]
    c = And(constraints)
    assert len(c) == 2
    assert list(c) == constraints


def test_filter_chains_multiple_constraints() -> None:
    c = And([MockFilterConstraint("A"), MockFilterConstraint("MA")])
    words = ["MA", "PA", "MAP"]
    assert list(c.filter(words)) == ["MA"]


def test_create_candidates_merges_outputs(subtests: SubTests) -> None:
    board = Board([])
    word = "APPLE"

    c = And(
        [
            MockCandidateConstraint("A"),
            MockCandidateConstraint("APP"),
            MockCandidateConstraint("X"),  # will contribute nothing
        ]
    )

    candidates = list(c.create_candidates(board, word))

    for candidate in candidates:
        assert isinstance(candidate, Word)

    assert len(candidates) == 2
    assert {w.value for w in candidates} == {"APPLE"}


def test_repr() -> None:
    c = And([MockFilterConstraint("A"), MockCandidateConstraint("B")])
    assert repr(c) == "And([MockFilterConstraint(A), MockCandidateConstraint(B)])"
