import pytest

from banana.board import ACROSS, DOWN, Board, Position


def test_invalid_value():
    with pytest.raises(Board.ValueError):
        Board({Position(0, 0): "1"})
    with pytest.raises(Board.ValueError):
        Board({Position(0, 0): "abc"})


def test_dict():
    assert dict(Board()) == dict()
    assert dict(Board({Position(0, 0): "A"})) == {Position(0, 0): "A"}


def test_upper():
    assert dict(Board({Position(0, 0): "a"})) == {Position(0, 0): "A"}


def test_empty_ignored():
    board = Board({Position(0, 0): " "})
    assert board[Position(0, 0)] == " "
    assert dict(board) == dict()


def test_getitem():
    assert Board({Position(0, 0): "A"})[Position(0, 0)] == "A"


def test_setitem():
    board = Board()
    assert board[Position(0, 0)] == " "
    board[Position(0, 0)] = "A"
    assert board[Position(0, 0)] == "A"


def test_setitem_blank():
    board = Board({Position(0, 0): "A"})
    assert board[Position(0, 0)] == "A"
    board[Position(0, 0)] = " "
    assert board[Position(0, 0)] == " "


def test_delitem():
    board = Board({Position(0, 0): "A"})
    assert board[Position(0, 0)] == "A"
    del board[Position(0, 0)]
    assert board[Position(0, 0)] == " "


def test_len():
    assert len(Board()) == 0
    assert len(Board({Position(0, 0): "A"})) == 1


def test_from_str():
    board_str = """
        ABC
        D E
        

         F
    """
    board = Board.from_str(board_str)
    assert dict(board) == dict(
        {
            Position(0, 0): "A",
            Position(1, 0): "B",
            Position(2, 0): "C",
            Position(0, 1): "D",
            Position(2, 1): "E",
            Position(1, 4): "F",
        }
    )
    assert Board.from_str(str(board)) == board


def test_bounds():
    assert Board(
        {
            Position(-1, 0): "A",
            Position(0, -2): "B",
            Position(3, 0): "C",
            Position(0, 4): "D",
        }
    ).bounds() == (Position(-1, -2), Position(3, 4))

    assert Board().bounds() == (Position(0, 0), Position(0, 0))


def test_str():
    board_str = """
        ABC
        D E
         F
    """

    assert str(Board.from_str(board_str)) == "ABC\nD E\n F \n"


def test_place_word():
    board = Board()
    board.place_word("ABC", Position(0, 0), ACROSS)
    assert board[Position(0, 0)] == "A"
    assert board[Position(1, 0)] == "B"
    assert board[Position(2, 0)] == "C"

    board.place_word("DEF", Position(0, 0), DOWN)
    assert board[Position(0, 0)] == "D"
    assert board[Position(0, 1)] == "E"
    assert board[Position(0, 2)] == "F"


def test_get_words():
    board_str = """
        ABC

        DEF
         G
         HKL
    """
    assert set(Board.from_str(board_str).get_words()) == {
        "ABC",
        "DEF",
        "EGH",
        "HKL",
    }
