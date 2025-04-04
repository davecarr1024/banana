from typing import Iterable, Iterator, Sized, override

from banana.board.direction import ACROSS, DOWN, Direction
from banana.board.position import Position
from banana.board.tile import Tile


class Word(Sized, Iterable[Tile]):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __init__(self, tiles: Iterable[Tile]) -> None:
        self._tiles = tuple(tiles)

        if len(self._tiles) < 2:
            raise self.ValueError(f"Word must have at least two tiles, not {len(self)}")
        for direction in ACROSS, DOWN:
            if self._tiles[0].position + direction == self._tiles[1].position:
                break
        else:
            raise self.ValueError(f"Word {self!r} has invalid direction")
        if not all(
            self._tiles[i].position + direction == self._tiles[i + 1].position
            for i in range(len(self._tiles) - 1)
        ):
            raise self.ValueError(f"Word {self!r} has non-linear tiles")
        self.direction = direction
        self.value = "".join(tile.value for tile in self)
        self.position = self._tiles[0].position

    @override
    def __repr__(self) -> str:
        return f"Word({self._tiles})"

    @override
    def __str__(self) -> str:
        return (
            f"Word(value={self.value}, "
            f"position={self.position}, "
            f"direction={self.direction})"
        )

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Word) and self._tiles == other._tiles

    @override
    def __hash__(self) -> int:
        return hash(self._tiles)

    @override
    def __len__(self) -> int:
        return len(self._tiles)

    @override
    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)

    def overlaps(self, rhs: "Word") -> bool:
        return bool(set(self) & set(rhs))

    @classmethod
    def from_str(
        cls,
        word_str: str,
        position: Position,
        direction: Direction,
    ) -> "Word":
        tiles = list[Tile]()
        for char in word_str:
            tiles.append(Tile(char, position))
            position += direction
        return cls(tiles)
