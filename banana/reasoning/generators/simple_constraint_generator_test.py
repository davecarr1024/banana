from typing import Iterable

from banana.board import ACROSS, DOWN, Board, Position, Word
from banana.reasoning import ConstraintGenerator
from banana.reasoning.generators import SimpleConstraintGenerator


def _filter_words(
    board: Board,
    cg: ConstraintGenerator,
    letters: Iterable[str],
    words: Iterable[str],
) -> Iterable[str]:
    words = list(words)
    constraints = list(cg.generate(board, letters))
    for constraint in constraints:
        yield from constraint.filter(words)


def _generate_candidates(
    board: Board,
    cg: ConstraintGenerator,
    letters: Iterable[str],
    words: Iterable[str],
) -> Iterable[Word]:
    letters = list(letters)
    words = list(words)
    constraints = list(cg.generate(board, letters))
    for constraint in constraints:
        filtered_words = list(constraint.filter(words))
        for word in filtered_words:
            yield from constraint.create_candidates(board, word)


def test_start() -> None:
    board = Board([])
    letters = "ABC"
    words = ["ABC", "DEF"]
    cg = SimpleConstraintGenerator(words)
    assert list(_filter_words(board, cg, letters, words)) == ["ABC"]
    assert list(_generate_candidates(board, cg, letters, words)) == [
        Word.from_str("ABC", Position(0, 0), ACROSS)
    ]


def test_anchor() -> None:
    board = Board.from_str("ABC")
    letters = "DE"
    words = ["ABC", "CDE", "CDF"]
    cg = SimpleConstraintGenerator(words)
    assert list(_filter_words(board, cg, letters, words)) == ["CDE"]
    assert list(_generate_candidates(board, cg, letters, words)) == [
        Word.from_str("CDE", Position(2, 0), DOWN)
    ]


def test_anchor_avoids_intersection() -> None:
    board = Board.from_str(
        """
        ABC
          D
          C
    """
    )
    letters = "EF"
    words = ["ABC", "CDC", "CEF", "CEG"]
    cg = SimpleConstraintGenerator(words)
    assert set(_filter_words(board, cg, letters, words)) == {"CEF"}
    assert list(_generate_candidates(board, cg, letters, words)) == [
        Word.from_str("CEF", Position(2, 2), ACROSS)
    ]


def test_anchor_attaches_inside_new_word() -> None:
    board = Board.from_str("ABC")
    letters = "EF"
    words = ["ABC", "EBF", "EBG"]
    cg = SimpleConstraintGenerator(words)
    assert list(_filter_words(board, cg, letters, words)) == ["EBF"]
    assert list(_generate_candidates(board, cg, letters, words)) == [
        Word.from_str("EBF", Position(1, -1), DOWN)
    ]


def test_anchor_attaches_at_end_of_new_word() -> None:
    board = Board.from_str("ABC")
    letters = "EF"
    words = ["ABC", "EFB", "EGB"]
    cg = SimpleConstraintGenerator(words)
    assert list(_filter_words(board, cg, letters, words)) == ["EFB"]
    assert list(_generate_candidates(board, cg, letters, words)) == [
        Word.from_str("EFB", Position(1, -2), DOWN)
    ]
