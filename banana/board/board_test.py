from typing import Optional

import pytest
from pytest_subtests import SubTests

from banana.board import Board, Position, Tile, Word


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
            assert board.tile(position) == expected


def test_add_tile() -> None:
    board = Board([])
    assert set(board) == set()
    assert board.tile(Position(0, 0)) is None
    board.add_tile(Tile("A", Position(0, 0)))
    assert set(board) == {Tile("A", Position(0, 0))}
    assert board.tile(Position(0, 0)) == Tile("A", Position(0, 0))


def test_remove_tile() -> None:
    board = Board([Tile("A", Position(0, 0))])
    assert set(board) == {Tile("A", Position(0, 0))}
    assert board.tile(Position(0, 0)) == Tile("A", Position(0, 0))
    board.remove_tile(Tile("A", Position(0, 0)))
    assert set(board) == set()
    assert board.tile(Position(0, 0)) is None


def test_remove_unknown_tile() -> None:
    board = Board([])
    assert set(board) == set()
    board.remove_tile(Tile("A", Position(0, 0)))
    assert set(board) == set()


def test_place_word():
    board = Board([])
    assert set(board) == set()
    board.place_word(Word([Tile("A", Position(0, 0)), Tile("B", Position(1, 0))]))
    assert set(board) == {Tile("A", Position(0, 0)), Tile("B", Position(1, 0))}


def test_place_overlapping_word():
    board = Board([Tile("A", Position(0, 0))])
    assert set(board) == {Tile("A", Position(0, 0))}
    board.place_word(Word([Tile("A", Position(0, 0)), Tile("B", Position(1, 0))]))
    assert set(board) == {Tile("A", Position(0, 0)), Tile("B", Position(1, 0))}


def test_place_invalid_word():
    board = Board([Tile("A", Position(0, 0))])
    assert set(board) == {Tile("A", Position(0, 0))}
    with pytest.raises(Board.ValueError):
        board.place_word(Word([Tile("B", Position(0, 0)), Tile("A", Position(1, 0))]))


def test_place_invalid_word_with_no_validation():
    board = Board([Tile("A", Position(0, 0))])
    assert set(board) == {Tile("A", Position(0, 0))}
    board.place_word(
        Word([Tile("B", Position(0, 0)), Tile("A", Position(1, 0))]), validate=False
    )
    assert set(board) == {Tile("B", Position(0, 0)), Tile("A", Position(1, 0))}


def test_add_tile_overwrites_by_position():
    board = Board([])

    tile_a = Tile("A", Position(0, 0))
    tile_b = Tile("B", Position(0, 0))  # same position, different value

    board.add_tile(tile_a)
    assert board.tile(Position(0, 0)) == tile_a
    assert tile_a in board
    assert tile_b not in board  # different value

    board.add_tile(tile_b)  # should overwrite tile_a
    assert board.tile(Position(0, 0)) == tile_b
    assert tile_a not in board
    assert tile_b in board
    assert len(board) == 1


def test_remove_tile_removes_by_position_not_identity():
    board = Board([Tile("A", Position(0, 0))])

    # Removing a different Tile object with the same position should still work
    board.remove_tile(Tile("A", Position(0, 0)))
    assert board.tile(Position(0, 0)) is None
    assert len(board) == 0


def test_add_tile_does_not_affect_other_positions():
    board = Board(
        [
            Tile("A", Position(0, 0)),
            Tile("B", Position(1, 0)),
        ]
    )
    board.add_tile(Tile("C", Position(0, 0)))

    assert set(board) == {
        Tile("C", Position(0, 0)),
        Tile("B", Position(1, 0)),
    }


def test_from_str():
    board_str = """
        ABC
        D E

         F
    """
    board = Board.from_str(board_str)
    assert set(board) == {
        Tile("A", Position(0, 0)),
        Tile("B", Position(1, 0)),
        Tile("C", Position(2, 0)),
        Tile("D", Position(0, 1)),
        Tile("E", Position(2, 1)),
        Tile("F", Position(1, 3)),
    }
    assert Board.from_str(str(board)) == board


def test_get_words():
    board_str = """
        ABC

        DEF
         G
         HKL
    """
    board = Board.from_str(board_str)
    words = set(board.get_words())

    expected_words = {
        Word(
            [
                Tile("A", Position(0, 0)),
                Tile("B", Position(1, 0)),
                Tile("C", Position(2, 0)),
            ]
        ),
        Word(
            [
                Tile("D", Position(0, 2)),
                Tile("E", Position(1, 2)),
                Tile("F", Position(2, 2)),
            ]
        ),
        Word(
            [
                Tile("E", Position(1, 2)),
                Tile("G", Position(1, 3)),
                Tile("H", Position(1, 4)),
            ]
        ),
        Word(
            [
                Tile("H", Position(1, 4)),
                Tile("K", Position(2, 4)),
                Tile("L", Position(3, 4)),
            ]
        ),
    }

    assert words == expected_words


def test_bounds():
    assert Board(
        [
            Tile("A", Position(1, 0)),
            Tile("B", Position(-2, 0)),
            Tile("C", Position(0, 3)),
            Tile("D", Position(0, -4)),
        ]
    ).bounds() == (Position(-2, -4), Position(1, 3))


def test_str() -> None:
    assert (
        str(
            Board(
                [
                    Tile("A", Position(0, 0)),
                    Tile("B", Position(1, 0)),
                    Tile("C", Position(1, 1)),
                ]
            )
        )
        == "AB\n C\n"
    )


def test_empty_bounds() -> None:
    assert Board([]).bounds() == (Position(0, 0), Position(0, 0))
