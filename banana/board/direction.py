from dataclasses import dataclass
from typing import override


@dataclass(frozen=True)
class Direction:
    dx: int
    dy: int

    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __post_init__(self) -> None:
        if self.dx * self.dx + self.dy * self.dy != 1:
            raise self.ValueError(f"Invalid direction: {self}")

    @override
    def __str__(self) -> str:
        match (self.dx, self.dy):
            case 1, 0:
                return "ACROSS"
            case 0, 1:
                return "DOWN"
            case -1, 0:
                return "-ACROSS"
            case 0, -1:
                return "-DOWN"
            case _:
                return f"Direction({self.dx}, {self.dy})"

    def __add__(self, rhs: "position.Position") -> "position.Position":
        return position.Position(rhs.x + self.dx, rhs.y + self.dy)

    def __neg__(self) -> "Direction":
        return Direction(-self.dx, -self.dy)

    def __mul__(self, rhs: int) -> "offset.Offset":
        return offset.Offset(self.dx * rhs, self.dy * rhs)

    def orthogonal(self) -> "Direction":
        return Direction(self.dy, self.dx)


ACROSS = Direction(1, 0)
DOWN = Direction(0, 1)

from banana.board import offset, position  # noqa: E402
