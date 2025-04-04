from collections.abc import Set
from typing import Iterable, Iterator, override

from banana.board.position import Position
from banana.board.tile import Tile


class Board(Set[Tile]):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    class KeyError(Error, KeyError): ...

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

    def tile(self, position: Position) -> Tile:
        try:
            return self._tiles_by_pos[position]
        except KeyError as e:
            raise self.KeyError(f"No tile at {position!r}") from e

    def add_tile(self, tile: Tile) -> None:
        self._tiles |= {tile}

    def remove_tile(self, tile: Tile) -> None:
        self._tiles -= {tile}

    # @override
    # def __str__(self) -> str:
    #     min, max = self.bounds()
    #     return "".join(
    #         "".join(self[Position(x, y)] for x in range(min.x, max.x + 1)) + "\n"
    #         for y in range(min.y, max.y + 1)
    #     )

    # @override
    # def __len__(self)->int:
    #     return len(self._tiles)

    # @override
    # def __iter__(self)->Iterator[Tile]:
    #     return iter(self._tiles)

    # @staticmethod
    # def _validate_value(value: str) -> str:
    #     if len(value) != 1 or not value.isalpha():
    #         raise Board.ValueError(f"Value must be a single character, not {value!r}")
    #     return value.upper()

    # def __post_init__(self) -> None:
    #     for pos, value in dict(self._chars).items():
    #         if value == " ":
    #             del self._chars[pos]
    #         else:
    #             self._chars[pos] = Board._validate_value(value)

    # @classmethod
    # def from_str(cls, board_str: str) -> "Board":
    #     def trim_empty_lines(lines: Iterable[str]) -> list[str]:
    #         def is_empty(line: str) -> bool:
    #             return not line.strip()

    #         lines = list(dropwhile(is_empty, lines))
    #         return list(reversed(list(dropwhile(is_empty, reversed(lines)))))

    #     def trim_leading_whitespace(lines: Iterable[str]) -> list[str]:
    #         leading_whitespace = min(
    #             len(list(takewhile(str.isspace, line)))
    #             for line in lines
    #             if line.strip()
    #         )
    #         return [line[leading_whitespace:] if


# line.strip() else "" for line in lines]

#     lines = board_str.splitlines()
#     lines = trim_empty_lines(lines)
#     lines = trim_leading_whitespace(lines)
#     return cls(
#         {
#             Position(x, y): value
#             for y, line in enumerate(lines)
#             for x, value in enumerate(line)
#             if not value.isspace()
#         }
#     )

# def bounds(self) -> tuple[Position, Position]:
#     if len(self) == 0:
#         return Position(0, 0), Position(0, 0)
#     xs = [pos.x for pos in self.keys()]
#     ys = [pos.y for pos in self.keys()]
#     return Position(min(xs), min(ys)), Position(max(xs), max(ys))

# def place_word(
#     self,
#     word: Word,
# ) -> None:
#     position = word.position
#     for char in word.value:
#         self[position] = char
#         position += word.direction

# def get_words(self) -> Iterable[Word]:
#     for pos, char in self.items():
#         for direction in (ACROSS, DOWN):
#             if self[pos - direction] != " ":
#                 continue
#             word = ""
#             position = pos
#             while char != " ":
#                 word += char
#                 pos += direction
#                 char = self[pos]
#             if len(word) >= 2:
#                 yield Word(word, position, direction)
