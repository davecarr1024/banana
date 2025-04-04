from typing import Optional

import pytest
from pytest_subtests import SubTests

from banana.board import Board, Position, Tile


def test_eq(subtests: SubTests):
    for lhs, rhs, expected in list[tuple[Board, Board, bool]](
        [
            (
                Board([]),
                Board([]),
                True,
            ),
            (
                Board([Tile("A", Position(0, 1))]),
                Board([Tile("A", Position(0, 1))]),
                True,
            ),
            (
                Board([Tile("A", Position(0, 1))]),
                Board([]),
                False,
            ),
            (
                Board([]),
                Board([Tile("A", Position(0, 1))]),
                False,
            ),
            (
                Board([Tile("A", Position(0, 1))]),
                Board([Tile("B", Position(0, 1))]),
                False,
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert (lhs == rhs) == expected
            assert (hash(lhs) == hash(rhs)) == expected


def test_contains(subtests: SubTests) -> None:
    for board, tile, expected in list[tuple[Board, Tile, bool]](
        [
            (
                Board([]),
                Tile("A", Position(0, 0)),
                False,
            ),
            (
                Board([Tile("A", Position(0, 0))]),
                Tile("A", Position(0, 0)),
                True,
            ),
            (
                Board([Tile("A", Position(0, 0))]),
                Tile("B", Position(0, 0)),
                False,
            ),
        ]
    ):
        with subtests.test(board=board, tile=tile, expected=expected):
            assert (tile in board) == expected


def test_iter() -> None:
    assert {
        tile.value
        for tile in Board(
            [
                Tile("A", Position(0, 1)),
                Tile("B", Position(1, 0)),
            ]
        )
    } == {"A", "B"}


def test_len(subtests: SubTests) -> None:
    for board, expected in list[tuple[Board, int]](
        [
            (
                Board([]),
                0,
            ),
            (
                Board([Tile("A", Position(0, 0))]),
                1,
            ),
        ]
    ):
        with subtests.test(board=board, expected=expected):
            assert len(board) == expected


def test_tiles() -> None:
    assert {
        tile.value
        for tile in Board(
            [
                Tile("A", Position(0, 1)),
                Tile("B", Position(1, 0)),
            ]
        ).tiles
    } == {"A", "B"}


def test_get_tile(subtests: SubTests) -> None:
    for board, position, expected in list[
        tuple[
            Board,
            Position,
            Optional[Tile],
        ]
    ](
        [
            (
                Board([]),
                Position(0, 0),
                None,
            ),
            (
                Board([Tile("A", Position(0, 0))]),
                Position(0, 0),
                Tile("A", Position(0, 0)),
            ),
            (
                Board([Tile("A", Position(0, 0))]),
                Position(1, 0),
                None,
            ),
        ]
    ):
        with subtests.test(
            board=board,
            position=position,
            expected=expected,
        ):
            if expected is None:
                with pytest.raises(Board.KeyError):
                    board.tile(position)
            else:
                assert board.tile(position) == expected


def test_add_tile() -> None:
    board = Board([])
    assert set(board) == set()
    with pytest.raises(Board.KeyError):
        board.tile(Position(0, 0))
    board.add_tile(Tile("A", Position(0, 0)))
    assert set(board) == {Tile("A", Position(0, 0))}
    assert board.tile(Position(0, 0)) == Tile("A", Position(0, 0))


def test_remove_tile() -> None:
    board = Board([Tile("A", Position(0, 0))])
    assert set(board) == {Tile("A", Position(0, 0))}
    assert board.tile(Position(0, 0)) == Tile("A", Position(0, 0))
    board.remove_tile(Tile("A", Position(0, 0)))
    assert set(board) == set()
    with pytest.raises(Board.KeyError):
        board.tile(Position(0, 0))


def test_remove_unknown_tile() -> None:
    board = Board([])
    assert set(board) == set()
    board.remove_tile(Tile("A", Position(0, 0)))
    assert set(board) == set()


# import pytest

# from banana.board import ACROSS, DOWN, Board, Position, Word


# def test_invalid_value():
#     with pytest.raises(Board.ValueError):
#         Board({Position(0, 0): "1"})
#     with pytest.raises(Board.ValueError):
#         Board({Position(0, 0): "abc"})


# def test_dict():
#     assert dict(Board()) == dict()
#     assert dict(Board({Position(0, 0): "A"})) == {Position(0, 0): "A"}


# def test_upper():
#     assert dict(Board({Position(0, 0): "a"})) == {Position(0, 0): "A"}


# def test_empty_ignored():
#     board = Board({Position(0, 0): " "})
#     assert board[Position(0, 0)] == " "
#     assert dict(board) == dict()


# def test_getitem():
#     assert Board({Position(0, 0): "A"})[Position(0, 0)] == "A"


# def test_setitem():
#     board = Board()
#     assert board[Position(0, 0)] == " "
#     board[Position(0, 0)] = "A"
#     assert board[Position(0, 0)] == "A"


# def test_setitem_blank():
#     board = Board({Position(0, 0): "A"})
#     assert board[Position(0, 0)] == "A"
#     board[Position(0, 0)] = " "
#     assert board[Position(0, 0)] == " "


# def test_delitem():
#     board = Board({Position(0, 0): "A"})
#     assert board[Position(0, 0)] == "A"
#     del board[Position(0, 0)]
#     assert board[Position(0, 0)] == " "


# def test_len():
#     assert len(Board()) == 0
#     assert len(Board({Position(0, 0): "A"})) == 1


# def test_from_str():
#     board_str = """
#         ABC
#         D E


#          F
#     """
#     board = Board.from_str(board_str)
#     assert dict(board) == dict(
#         {
#             Position(0, 0): "A",
#             Position(1, 0): "B",
#             Position(2, 0): "C",
#             Position(0, 1): "D",
#             Position(2, 1): "E",
#             Position(1, 4): "F",
#         }
#     )
#     assert Board.from_str(str(board)) == board


# def test_bounds():
#     assert Board(
#         {
#             Position(-1, 0): "A",
#             Position(0, -2): "B",
#             Position(3, 0): "C",
#             Position(0, 4): "D",
#         }
#     ).bounds() == (Position(-1, -2), Position(3, 4))

#     assert Board().bounds() == (Position(0, 0), Position(0, 0))


# def test_str():
#     board_str = """
#         ABC
#         D E
#          F
#     """

#     assert str(Board.from_str(board_str)) == "ABC\nD E\n F \n"


# def test_place_word():
#     board = Board()
#     board.place_word(Word("ABC", Position(0, 0), ACROSS))
#     assert board[Position(0, 0)] == "A"
#     assert board[Position(1, 0)] == "B"
#     assert board[Position(2, 0)] == "C"

#     board.place_word(Word("DEF", Position(0, 0), DOWN))
#     assert board[Position(0, 0)] == "D"
#     assert board[Position(0, 1)] == "E"
#     assert board[Position(0, 2)] == "F"


# def test_get_words():
#     board_str = """
#         ABC

#         DEF
#          G
#          HKL
#     """
#     assert set(Board.from_str(board_str).get_words()) == {
#         Word("ABC", Position(0, 0), ACROSS),
#         Word("DEF", Position(0, 2), ACROSS),
#         Word("EGH", Position(1, 2), DOWN),
#         Word("HKL", Position(1, 4), ACROSS),
#     }
