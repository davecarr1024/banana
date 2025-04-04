import pytest

from banana.board import Position, Tile


@pytest.mark.parametrize(
    "value",
    ["", "1", "abc"],
)
def test_invalid_value(value: str):
    with pytest.raises(Tile.ValueError):
        Tile(value, Position(0, 0))


def test_upper():
    assert Tile("a", Position(0, 0)).value == "A"
