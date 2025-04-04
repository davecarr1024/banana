from collections.abc import MutableMapping
from dataclasses import dataclass, field
from itertools import dropwhile, takewhile
from typing import Iterable, Iterator, override

from banana.board.direction import ACROSS, DOWN
from banana.board.position import Position
from banana.board.word import Word


@dataclass
class Board(MutableMapping[Position, str]):
    _chars: MutableMapping[Position, str] = field(default_factory=dict[Position, str])

    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    @staticmethod
    def _validate_value(value: str) -> str:
        if len(value) != 1 or not value.isalpha():
            raise Board.ValueError(f"Value must be a single character, not {value!r}")
        return value.upper()

    def __post_init__(self) -> None:
        for pos, value in dict(self._chars).items():
            if value == " ":
                del self._chars[pos]
            else:
                self._chars[pos] = Board._validate_value(value)

    @override
    def __iter__(self) -> Iterator[Position]:
        return iter(self._chars)

    @override
    def __len__(self) -> int:
        return len(self._chars)

    @override
    def __getitem__(self, key: Position) -> str:
        return self._chars.get(key, " ")

    @override
    def __setitem__(self, key: Position, value: str) -> None:
        if value == " ":
            del self._chars[key]
        else:
            self._chars[key] = Board._validate_value(value)

    @override
    def __delitem__(self, key: Position) -> None:
        del self._chars[key]

    @classmethod
    def from_str(cls, board_str: str) -> "Board":
        def trim_empty_lines(lines: Iterable[str]) -> list[str]:
            def is_empty(line: str) -> bool:
                return not line.strip()

            lines = list(dropwhile(is_empty, lines))
            return list(reversed(list(dropwhile(is_empty, reversed(lines)))))

        def trim_leading_whitespace(lines: Iterable[str]) -> list[str]:
            leading_whitespace = min(
                len(list(takewhile(str.isspace, line)))
                for line in lines
                if line.strip()
            )
            return [line[leading_whitespace:] if line.strip() else "" for line in lines]

        lines = board_str.splitlines()
        lines = trim_empty_lines(lines)
        lines = trim_leading_whitespace(lines)
        return cls(
            {
                Position(x, y): value
                for y, line in enumerate(lines)
                for x, value in enumerate(line)
                if not value.isspace()
            }
        )

    def bounds(self) -> tuple[Position, Position]:
        if len(self) == 0:
            return Position(0, 0), Position(0, 0)
        xs = [pos.x for pos in self.keys()]
        ys = [pos.y for pos in self.keys()]
        return Position(min(xs), min(ys)), Position(max(xs), max(ys))

    @override
    def __str__(self) -> str:
        min, max = self.bounds()
        return "".join(
            "".join(self[Position(x, y)] for x in range(min.x, max.x + 1)) + "\n"
            for y in range(min.y, max.y + 1)
        )

    def place_word(
        self,
        word: Word,
    ) -> None:
        position = word.position
        for char in word.value:
            self[position] = char
            position += word.direction

    def get_words(self) -> Iterable[Word]:
        for pos, char in self.items():
            for direction in (ACROSS, DOWN):
                if self[pos - direction] != " ":
                    continue
                word = ""
                position = pos
                while char != " ":
                    word += char
                    pos += direction
                    char = self[pos]
                if len(word) >= 2:
                    yield Word(word, position, direction)
