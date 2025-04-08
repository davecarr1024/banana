import pytest

from banana.board import Board, Position
from banana.reasoning.generators import SimpleConstraintGenerator
from banana.reasoning.searches.beam_search import BeamSearch


def test_search_empty_board() -> None:
    board = Board([])
    letters = "CAB"
    words = ["CAB"]
    search = BeamSearch(
        words,
        SimpleConstraintGenerator(words),
    )

    result = search.search(board, letters)
    expected = Board.from_str("CAB")

    assert result == expected


def test_search_simple_anchor() -> None:
    # Start with "CAB" on the board, try to attach "BAD" using anchor on 'B'
    board = Board.from_str("CAB")
    letters = "AD"
    words = ["BAD", "DAD", "CAB"]
    search = BeamSearch(
        words,
        SimpleConstraintGenerator(words),
    )

    result = search.search(board, letters)

    # Should place "BAD" going down from 'B' at (2,0)
    expected = Board.from_str(
        """
        CAB
          A
          D
        """
    )

    assert result == expected


def test_search_fails_gracefully() -> None:
    board = Board.from_str("CAB")
    letters = "XYZ"
    words = ["CAB", "BAD"]
    search = BeamSearch(
        words,
        SimpleConstraintGenerator(words),
    )

    with pytest.raises(BeamSearch.SearchError):
        search.search(board, letters)


def test_search_attaches_midword() -> None:
    board = Board.from_str("ABC")
    letters = "DE"
    words = ["ABC", "DBE"]
    search = BeamSearch(
        words,
        SimpleConstraintGenerator(words),
    )

    result = search.search(board, letters)

    expected = Board.from_str(
        """
         D
        ABC
         E
        """,
        starting_pos=Position(0, -1),
    )

    assert result == expected
