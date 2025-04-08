from collections.abc import Set
from itertools import dropwhile, takewhile
from typing import Iterable, Iterator, Optional, override

from banana.board.direction import ACROSS, DOWN
from banana.board.position import Position
from banana.board.tile import Tile
from banana.board.word import Word


class Board(Set[Tile]):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __init__(self, tiles: Iterable[Tile]) -> None:
        self._tiles = frozenset(tiles)

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Board) and self._tiles == other._tiles

    @override
    def __hash__(self) -> int:
        return hash(self._tiles)

    @override
    def __repr__(self) -> str:
        return f"Board({self._tiles})"

    @override
    def __contains__(self, item: object) -> bool:
        return item in self._tiles

    @override
    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)

    @override
    def __len__(self) -> int:
        return len(self._tiles)

    @property
    def _tiles(self) -> frozenset[Tile]:
        return self.__tiles

    @_tiles.setter
    def _tiles(self, _tiles: frozenset[Tile]) -> None:
        self.__tiles = _tiles
        self._tiles_by_pos = {tile.position: tile for tile in self._tiles}

    @property
    def tiles(self) -> frozenset[Tile]:
        return self._tiles

    def tile(self, position: Position) -> Optional[Tile]:
        return self._tiles_by_pos.get(position, None)

    def add_tile(self, tile: Tile) -> None:
        updated = dict(self._tiles_by_pos)
        updated[tile.position] = tile
        self._tiles = frozenset(updated.values())

    def remove_tile(self, tile: Tile) -> None:
        self.remove_tile_at(tile.position)

    def remove_tile_at(self, position: Position) -> None:
        self._tiles = frozenset(t for t in self._tiles if t.position != position)

    def can_place_word(self, word: Word) -> bool:
        for word_tile in word:
            if board_tile := self.tile(word_tile.position):
                if word_tile != board_tile:
                    return False
        return True

    def place_word(self, word: Word, validate: bool = True) -> None:
        if validate and not self.can_place_word(word):
            raise self.ValueError(f"Cannot place word {word} on board {self}")
        for tile in word:
            self.add_tile(tile)

    def get_words(self) -> Iterable[Word]:
        for start_tile in self:
            for direction in ACROSS, DOWN:
                if self.tile(start_tile.position - direction):
                    continue
                tiles = list[Tile]()
                tile = start_tile
                position = tile.position
                while tile is not None:
                    tiles.append(tile)
                    position += direction
                    tile = self.tile(position)
                if len(tiles) >= 2:
                    yield Word(tiles)

    @classmethod
    def from_str(cls, board_str: str) -> "Board":
        def trim_empty_lines(lines: list[str]) -> list[str]:
            def is_empty(line: str) -> bool:
                return not line.strip()

            lines = list(dropwhile(is_empty, lines))
            return list(reversed(list(dropwhile(is_empty, reversed(lines)))))

        def trim_leading_whitespace(lines: list[str]) -> list[str]:
            leading_spaces = min(
                len(list(takewhile(str.isspace, line)))
                for line in lines
                if line.strip()
            )
            return [line[leading_spaces:] if line.strip() else "" for line in lines]

        lines = board_str.splitlines()
        lines = trim_empty_lines(lines)
        lines = trim_leading_whitespace(lines)

        tiles = [
            Tile(value, Position(x, y))
            for y, line in enumerate(lines)
            for x, value in enumerate(line)
            if not value.isspace()
        ]
        return cls(tiles)

    def bounds(self) -> tuple[Position, Position]:
        if not self:
            return Position(0, 0), Position(0, 0)
        xs = [pos.x for pos in self._tiles_by_pos.keys()]
        ys = [pos.y for pos in self._tiles_by_pos.keys()]
        return Position(min(xs), min(ys)), Position(max(xs), max(ys))

    @override
    def __str__(self) -> str:
        min, max = self.bounds()
        s = ""
        for y in range(min.y, max.y + 1):
            for x in range(min.x, max.x + 1):
                if tile := self.tile(Position(x, y)):
                    s += tile.value
                else:
                    s += " "
            s += "\n"
        return s
