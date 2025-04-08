from banana.board import Position, Tile


def test_ctor():
    assert Tile("A", Position(0, 0)).value == "A"
