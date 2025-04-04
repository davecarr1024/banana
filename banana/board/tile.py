from dataclasses import dataclass

from banana.board.position import Position


@dataclass(frozen=True)
class Tile:
    value: str
    position: Position

    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __post_init__(self) -> None:
        if len(self.value) != 1 or not self.value.isalpha():
            raise self.ValueError(
                f"Value must be a single alpha character, not {self.value!r}"
            )
        object.__setattr__(self, "value", self.value.upper())
