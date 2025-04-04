from dataclasses import dataclass
from typing import Iterable, Iterator, Sized, override

from banana.board.direction import Direction
from banana.board.position import Position


@dataclass(frozen=True)
class Word(Sized, Iterable[tuple[Position, str]]):
    value: str
    position: Position
    direction: Direction

    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __post_init__(self) -> None:
        if not all(char.isalpha() and char.isupper() for char in self.value):
            raise self.ValueError(f"Invalid word value {self.value!r}")

    @override
    def __len__(self) -> int:
        return len(self.value)

    @override
    def __iter__(self) -> Iterator[tuple[Position, str]]:
        pos = self.position
        for char in self.value:
            yield pos, char
            pos += self.direction

    def overlaps(self, rhs: "Word") -> bool:
        return bool(set(self) & set(rhs))
