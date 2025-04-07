from dataclasses import dataclass

from banana.board.position import Position
from banana.validation import ValueError, validate_letter


@dataclass(frozen=True)
class Tile:
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    value: str
    position: Position

    def __post_init__(self) -> None:
        try:
            object.__setattr__(self, "value", validate_letter(self.value))
        except ValueError as e:
            raise self.ValueError(e) from e
